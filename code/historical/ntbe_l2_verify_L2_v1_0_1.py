#!/usr/bin/env python3
"""Read-only, fixed-input NTBE/X2-omega coordinate audit. Not scientific adjudication.
All systems pre-specified; pilot/full; per-system resume only after exact input/code fingerprints.
"""
import argparse,csv,hashlib,io,json,os,platform,sys,tempfile,time,traceback,zipfile
from pathlib import Path
import numpy as np
import mdtraj as md
from scipy.special import expit
import importlib.util

R=0.001987203599772605; T=295.0
ARCHIVE_SHA='81fa710c667d29f664e378e551ee1f180975a62d8e37d859646be8b2fa9469c7'

def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def find_member(z,suffix):
 m=[s for s in z.namelist() if s.endswith(suffix)]
 if len(m)!=1:raise ValueError(f'Expected exactly 1 member matching {suffix}, found {len(m)}')
 return m[0]
def npz_mem(z,sid):
 
 hits=[n for n in z.namelist() if n==sid+'.npz' or n.endswith('/'+sid+'.npz')]
 if len(hits)!=1:raise ValueError(f'{sid} NPZ ambiguous/missing: {hits}')
 return np.load(io.BytesIO(z.read(hits[0])),allow_pickle=False)
def read_csv_bytes(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'))))
def dg(q,mask):
 if not mask.any():return None
 p=float(expit(20*(np.asarray(q,dtype=np.float64)[mask]-.5)).mean());pc=np.clip(p,1e-10,1-1e-10)
 return float(-R*T*np.log(np.clip(pc/(1-pc),1e-10,1e10)))
def wrap(a):return (a+180.)%360.-180.
def omega_plane(x):
 # 4-atom xyz: (frames, bonds, 4, 3), plane-normal based expression.
 e0=x[:,:,1]-x[:,:,0];e1=x[:,:,2]-x[:,:,1];e2=x[:,:,3]-x[:,:,2]
 n0=np.cross(e0,e1);n1=np.cross(e1,e2);nn=np.linalg.norm(e1,axis=-1)
 u=np.divide(e1,nn[...,None],out=np.zeros_like(e1),where=nn[...,None]>1e-10)
 out=np.degrees(np.arctan2(np.sum(np.cross(n0,n1)*u,axis=-1),np.sum(n0*n1,axis=-1)))
 out[(np.linalg.norm(n0,axis=-1)<1e-10)|(np.linalg.norm(n1,axis=-1)<1e-10)|(nn<1e-10)]=np.nan
 return out

def atom_indices(top):
 res=list(top.residues)
 if top.n_chains!=1:raise ValueError('not one chain')
 quadruples=[];is_pro=[]
 for a,b in zip(res[:-1],res[1:]):
  four=[]
  for rr,nm in [(a,'CA'),(a,'C'),(b,'N'),(b,'CA')]:
   hits=[x.index for x in rr.atoms if x.name==nm]
   if len(hits)!=1:raise ValueError(f'{rr.index} {nm}: number of matches {len(hits)}')
   four.append(hits[0])
  quadruples.append(four);is_pro.append(b.name=='PRO')
 return np.asarray(quadruples,np.int32),np.asarray(is_pro,bool)

def check_eq(x,y,label):
 if not np.array_equal(x,y):raise ValueError(f'{label} mismatched: {int(np.count_nonzero(x!=y))} elements')
def maxerr(x,y):
 x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
 if x.shape!=y.shape:raise ValueError(f'array shape {x.shape} != {y.shape}')
 if not np.array_equal(np.isfinite(x),np.isfinite(y)):raise ValueError('different finite masks')
 ok=np.isfinite(x)&np.isfinite(y)
 return float(np.max(np.abs(x[ok]-y[ok]))) if ok.any() else 0.

def loadmod(name,path):
 sp=importlib.util.spec_from_file_location(name,str(path));m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m

def run_system(sid,za,zb,zn,meta,core,flt,fnc,out,manifest,chunk_size):
 start=time.perf_counter(); rec=core[sid]
 xm=find_member(za,'/'+sid+'/samples.xtc');pm=find_member(za,'/'+sid+'/topology.pdb');xb=za.read(xm);pb=za.read(pm)
 if sha(xb)!=rec['sha256_xtc'] or sha(pb)!=rec['sha256_pdb']:raise ValueError('raw XTC/PDB SHA mismatch')
 refname=find_member(zb,'/'+('reference_mutants' if rec['is_mutant']=='True' else 'reference_wildtypes')+'/'+sid+'.pdb')
 rb=zb.read(refname)
 if sha(rb)!=rec['sha256_reference']:raise ValueError('reference hash mismatch')
 with tempfile.TemporaryDirectory(prefix='ntbe_l2_') as td:
  d=Path(td);(d/'t.pdb').write_bytes(pb);(d/'r.pdb').write_bytes(rb);(d/'x.xtc').write_bytes(xb)
  ref=md.load_pdb(str(d/'r.pdb'));sample_pdb=md.load_pdb(str(d/'t.pdb'))
  if sample_pdb.top.to_fasta()[0]!=ref.top.to_fasta()[0] or sample_pdb.top.to_fasta()[0]!=meta[sid]['sequence']:
   raise ValueError('reference/sample/metadata sequence mismatch')
  idx,pro=atom_indices(sample_pdb.top)
  with npz_mem(zn,sid) as z:
   # These are ONLY comparison targets, never inputs to coordinate computations.
   zfields={k:z[k].copy() for k in ['fnc','b0_mask','bomega_mask','omega_degrees','next_is_pro','omega_atom_indices','near_boundary_mask']}
  check_eq(idx,zfields['omega_atom_indices'],'atom mapping');check_eq(pro,zfields['next_is_pro'],'next-is-pro')
  qparts=[];b0parts=[];bwparts=[];omegadiffs=[];nearparts=[];nframes=0;coord_max=0.; official_fnc_diff=[]
  ca_diff=cn_diff=clash_diff=0
  for t in md.iterload(str(d/'x.xtc'),top=str(d/'t.pdb'),chunk=chunk_size):
   n=t.n_frames;first=nframes;last=first+n
   if t.n_atoms!=sample_pdb.n_atoms:raise ValueError('topology atom-count mismatch')
   if not np.isfinite(t.xyz).all():raise ValueError('nonfinite coordinates')
   a,b,c=flt.filter_unphysical_traj_masks(t)
   keep=a&b&c
   # Independent direct geometry for adjacent C-alpha and peptide C-N.
   rr=list(t.top.residues)
   ca=np.array([next(x.index for x in r.atoms if x.name=='CA') for r in rr]);cn=idx[:,[1,2]]
   da=np.linalg.norm(t.xyz[:,ca[:-1]]-t.xyz[:,ca[1:]],axis=-1)*10
   dc=np.linalg.norm(t.xyz[:,cn[:,0]]-t.xyz[:,cn[:,1]],axis=-1)*10
   check_eq((da<4.5).all(1),a,'independent CA geometry');check_eq((dc<2.).all(1),b,'independent CN geometry')
   ang=omega_plane(t.xyz[:,idx,:].astype(np.float64))
   ze=zfields['omega_degrees'][first:last]
   if ang.shape!=ze.shape:raise ValueError('omega shape mismatch')
   ad=maxerr(wrap(ang-ze),np.zeros_like(ang))
   omegadiffs.append(ad)
   # Numerical precision XTC and saved float32; fail only well outside documented tolerance.
   if ad>0.02:raise ValueError(f'omega max difference {ad} deg > 0.02')
   dev=np.abs((ang+90.)%180.-90.);known=np.isfinite(ang)
   twist=known&(dev>30.)
   bomega=keep&~twist.any(axis=1)
   near=known&(np.abs(dev-30.)<=0.02)
   check_eq(keep,zfields['b0_mask'][first:last],'B0 mask')
   check_eq(bomega,zfields['bomega_mask'][first:last],'Bomega mask')
   check_eq(near,zfields['near_boundary_mask'][first:last],'near boundary mask')
   # Official FNC with explicitly pinned Settings: historical bare defaults DIFFER.
   settings=fnc.FNCSettings
   q=fnc.get_fnc_from_samples_trajectory(t,ref,sequence_separation=settings.sequence_separation,
     contact_cutoff=settings.contact_cutoff,contact_beta=settings.contact_beta,
     contact_lambda=settings.contact_lambda,contact_delta=settings.contact_delta)
   qe=maxerr(q,zfields['fnc'][first:last]);official_fnc_diff.append(qe)
   if qe>2e-5:raise ValueError(f'FNC diff {qe} exceeds 2e-5')
   qparts.append(np.asarray(q,np.float64));b0parts.append(keep);bwparts.append(bomega);nearparts.append(near)
   nframes=last
  if nframes!=int(float(rec['n_A'])):raise ValueError(f'frames {nframes} vs Core {rec["n_A"]}')
  q=np.concatenate(qparts);b0=np.concatenate(b0parts);bw=np.concatenate(bwparts)
  da=dg(q,np.ones(nframes,bool));d0=dg(q,b0);dw=dg(q,bw)
  if da is None or d0 is None or dw is None:raise ValueError('empty population')
  if abs(da-float(rec['dg_A']))>2e-4 or abs(d0-float(rec['dg_B']))>2e-4:raise ValueError('Core dG difference > 0.0002')
  row={'system':sid,'status':'PASS','frames':nframes,'b0':int(b0.sum()),'bomega':int(bw.sum()),
       'sha_xtc':sha(xb),'sha_pdb':sha(pb),'sha_reference':sha(rb),
       'max_omega_diff_deg':max(omegadiffs),'max_official_fnc_diff':max(official_fnc_diff),
       'dg_A':da,'dg_B0':d0,'dg_Bomega':dw,'max_near_boundary_frames':int(np.concatenate(nearparts).any(1).sum()),
       'seconds':round(time.perf_counter()-start,3)}
  (out/'systems'/f'{sid}.json').write_text(json.dumps({'fingerprint':manifest,'result':row},indent=2),encoding='utf-8')
  return row

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',default='.');p.add_argument('--mode',choices=['pilot','full','aggregate'],default='pilot');p.add_argument('--chunk',type=int,default=100);p.add_argument('--out',default='NTBE_L2_output');a=p.parse_args()
 root=Path(a.root).resolve();out=(root/a.out).resolve();(out/'systems').mkdir(parents=True,exist_ok=True)
 me=Path(__file__).resolve();srcsha=filehash(me)
 def locate(stem):
  arr=sorted([x for x in root.glob(stem+'*.zip') if x.stem==stem or (x.stem.startswith(stem+'(') and x.stem.endswith(')'))]);
  if len(arr)!=1:raise ValueError(f'{stem}: expected one ZIP, found {arr}. Keep only one file, or rename to canonical {stem}.zip')
  return arr[0]
 archive=locate('samples_delta_G');bench=locate('bioemu-benchmarks_code_release');nz=locate('all_npz')
 csvpaths=list(root.glob('NTBE_systems_154_reconciled*.csv'))
 if len(csvpaths)!=1:raise ValueError('Place exactly one NTBE_systems_154_reconciled.csv in root')
 core={r['name']:r for r in read_csv_bytes(csvpaths[0].read_bytes())}
 if len(core)!=154:raise ValueError('Core table must have 154 unique systems')
 manifest={'source_zip_sha256':ARCHIVE_SHA,'benchmark_sha256':filehash(bench),'all_npz_sha256':filehash(nz),
   'core_csv_sha256':filehash(csvpaths[0]),'script_sha256':srcsha,'chunk':a.chunk}
 if filehash(archive)!=ARCHIVE_SHA:raise ValueError('official raw archive SHA mismatch')
 if a.mode=='aggregate':
  rows=[]
  for sid in core:
   fp=out/'systems'/f'{sid}.json'
   if not fp.exists():rows.append({'system':sid,'status':'NOT_RUN'});continue
   ob=json.loads(fp.read_text(encoding='utf-8'));rows.append(ob['result'] if ob['fingerprint']==manifest else {'system':sid,'status':'STALE_FINGERPRINT'})
  counts={k:sum(r['status']==k for r in rows) for k in sorted({r['status'] for r in rows})}
  pairs_path=list(root.glob('NTBE_pairs_112_reconciled*.csv'))
  pairs=[]; pair_problem=[]
  if len(pairs_path)==1 and counts.get('PASS',0)==154:
   old=read_csv_bytes(pairs_path[0].read_bytes());by={r['system']:r for r in rows}
   for rec in old:
    m,w=by[rec['mutant']],by[rec['wt']]
    dA=m['dg_A']-w['dg_A'];dB=m['dg_B0']-w['dg_B0'];dW=m['dg_Bomega']-w['dg_Bomega']
    eA=abs(dA-float(rec['ddg_A']));eB=abs(dB-float(rec['ddg_B']))
    item={'mutant':rec['mutant'],'wt':rec['wt'],'ddg_A':dA,'ddg_B0':dB,'ddg_Bomega':dW,'difference_vs_original_ddg_A':eA,'difference_vs_original_ddg_B0':eB}
    pairs.append(item)
    if max(eA,eB)>4e-4:pair_problem.append(item)
   (out/'L2_pairs.json').write_text(json.dumps({'pairs':pairs,'failures':pair_problem},indent=2),encoding='utf-8')
  report={'scope':'Full 154 coordinate QA if all PASS','counts':counts,'all_pass':counts.get('PASS',0)==154 and not pair_problem,'pairs_checked':len(pairs),'pair_failures':len(pair_problem),'fingerprint':manifest,'runtime':{'python':sys.version,'mdtraj':md.__version__,'numpy':np.__version__},'rows':rows}
  (out/'L2_aggregate.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
  print(json.dumps({'counts':counts,'all_pass':report['all_pass']},indent=2));return
 pilot=['1EM7_L7A','1TG0__D45C_N47P','4C26__K58A','2RRT__A48P']
 targets=pilot if a.mode=='pilot' else list(core)
 snap=Path(__file__).with_name('official_fnc_snapshot.py');fltpath=Path(__file__).with_name('ntbe_official_filter_snapshot.py')
 flt=loadmod('l2_filter',fltpath);fnc=loadmod('l2_fnc',snap)
 with zipfile.ZipFile(archive) as za,zipfile.ZipFile(bench) as zb,zipfile.ZipFile(nz) as zn:
  zmeta=find_member(zb,'/folding_free_energies/system_info.csv');meta={r['name']:r for r in read_csv_bytes(zb.read(zmeta))}
  if set(meta)!=set(core):raise ValueError('metadata/Core ID mismatch')
  for i,sid in enumerate(targets,1):
   fp=out/'systems'/f'{sid}.json'
   if fp.exists():
    ob=json.loads(fp.read_text(encoding='utf-8'))
    if ob.get('fingerprint')==manifest and ob.get('result',{}).get('status')=='PASS':
     print(f'{i}/{len(targets)} {sid}: SKIP verified completed',flush=True);continue
   try:
    r=run_system(sid,za,zb,zn,meta,core,flt,fnc,out,manifest,a.chunk)
    print(f'{i}/{len(targets)} {sid}: PASS {r["seconds"]} sec',flush=True)
   except Exception as e:
    err={'fingerprint':manifest,'result':{'system':sid,'status':'FAIL','error':repr(e),'traceback':traceback.format_exc(limit=8)}}
    fp.write_text(json.dumps(err,indent=2),encoding='utf-8')
    print(f'{i}/{len(targets)} {sid}: FAIL: {e}',flush=True)
    if a.mode=='pilot':break
  print('Call --mode aggregate for summary.',flush=True)
if __name__=='__main__':main()
