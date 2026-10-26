#!/usr/bin/env python3
"""NT-BE/X2-omega L1 provenance and input QA. Read-only, no scientific reanalysis.
Uses Python standard library; optional MDTraj for selected physical XTC/PDB inspection.
"""
import argparse,csv,hashlib,io,json,os,platform,sys,time,zipfile,tempfile,shutil,traceback
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone

EXPECTED_ARCHIVE_SIZE=1959113732
EXPECTED_ARCHIVE_MD5='30c285d2a503fb3436cefda86c75a5c6'
EXPECTED_ARCHIVE_SHA256='81fa710c667d29f664e378e551ee1f180975a62d8e37d859646be8b2fa9469c7'
FILES=('samples.xtc','topology.pdb')

def digest_stream(fp, alg='sha256'):
 h=hashlib.new(alg)
 for chunk in iter(lambda:fp.read(8*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def digest_path(path,alg='sha256'):
 with open(path,'rb') as f:return digest_stream(f,alg)
def member_hash(z,n):
 with z.open(n) as f:return digest_stream(f)
def report_csv(path, rows):
 fields=['system','is_mutant','wt','status','expected_frames','xtc_bytes','pdb_bytes','xtc_member','pdb_member','reference_member','reference_status','reason']
 with open(path,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([{k:r.get(k,'') for k in fields} for r in rows])
def parse_args():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
 p.add_argument('--archive',type=Path,default=None)
 p.add_argument('--benchmark',type=Path,default=None)
 p.add_argument('--all-npz',type=Path,default=None)
 p.add_argument('--core',type=Path,default=None)
 p.add_argument('--recovery',type=Path,default=None)
 p.add_argument('--systems',type=Path,default=None)
 p.add_argument('--out',type=Path,default=None)
 p.add_argument('--selected',default='1EM7_L7A,1TG0__D45C_N47P,1A0N_L7S',help='Comma-separated IDs: non-benchmark IDs are informative only')
 p.add_argument('--coordinate-qa',action='store_true',help='Optional MDTraj read of selected benchmark XTCs and PDBs')
 p.add_argument('--full-member-hashes',action='store_true',help='Hash all 154*2 uncompressed members (extra I/O)')
 p.add_argument('--full-crc',action='store_true',help='Read all archive members for CRC (slow, optional)')
 p.add_argument('--skip-whole-hash',action='store_true',help='Skip reading 1.96GB file to verify full SHA256/MD5 (default hashes it)')
 return p.parse_args()
def run(a):
 root=a.root.resolve();src=(a.archive or root/'samples_delta_G.zip').resolve()
 bench=(a.benchmark or root/'bioemu-benchmarks_code_release.zip').resolve()
 out=(a.out or root/'NTBE_L1_output').resolve();out.mkdir(parents=True,exist_ok=True)
 for p in [src,bench]:
  if not p.is_file():raise FileNotFoundError('Missing required input: '+str(p))
 started=time.monotonic();summary={'version':'L1-v1.0','timestamp_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'input':{},'checks':{},'warnings':[],'limitations':['No B0/omega/FNC geometry scientific rerun','No claim of historical environment equivalence','Reference sequence matching checks apply only to selected coordinates if --coordinate-qa']}
 def check(key,predicate):summary['checks'][key]=bool(predicate)
 summary['input']['archive']={'path':str(src),'bytes':src.stat().st_size,'md5':None,'sha256':None}
 check('archive_byte_size',src.stat().st_size==EXPECTED_ARCHIVE_SIZE)
 if not a.skip_whole_hash:
  for algo in ['md5','sha256']:summary['input']['archive'][algo]=digest_path(src,algo)
  check('archive_official_md5',summary['input']['archive']['md5']==EXPECTED_ARCHIVE_MD5)
  check('archive_previous_local_sha256',summary['input']['archive']['sha256']==EXPECTED_ARCHIVE_SHA256)
 else:summary['warnings'].append('Whole ZIP hashes SKIPPED at user option')
 summary['input']['benchmark']={'path':str(bench),'bytes':bench.stat().st_size,'sha256':digest_path(bench)}
 with zipfile.ZipFile(bench) as bz:
  candidates=[n for n in bz.namelist() if n.endswith('/folding_free_energies/system_info.csv')]
  if len(candidates)!=1:raise ValueError('Benchmark metadata ambiguous: '+str(candidates))
  source_rows=list(csv.DictReader(io.StringIO(bz.read(candidates[0]).decode('utf-8-sig'))))
  ids=[r['name'] for r in source_rows]; idset=set(ids)
  check('metadata_154_unique_systems',len(ids)==154 and len(idset)==154)
  wt={r['name'] for r in source_rows if r['mutant'].strip().lower()=='false'}
  mutants=[r for r in source_rows if r['mutant'].strip().lower()=='true']
  check('metadata_42WT_112mutants',len(wt)==42 and len(mutants)==112 and all(r['name_wt'] in wt for r in mutants))
  refs={}
  for r in source_rows:
   sub='reference_mutants' if r['mutant'].strip().lower()=='true' else 'reference_wildtypes'
   m=[n for n in bz.namelist() if n.endswith('/'+sub+'/'+r['name']+'.pdb')]
   refs[r['name']]=m
  check('all_154_unique_reference_pdb',all(len(v)==1 for v in refs.values()))
  refsha={k:member_hash(bz,v[0]) for k,v in refs.items() if len(v)==1}
 with zipfile.ZipFile(src) as z:
  allmembers=z.infolist(); matched=defaultdict(lambda:defaultdict(list)); extra=Counter()
  for f in allmembers:
   if f.is_dir():continue
   parts=f.filename.replace('\\','/').strip('/').split('/')
   if len(parts)<2:continue
   sid,fn=parts[-2:]
   if fn in FILES:
    if sid in idset:matched[sid][fn].append(f)
    else:extra[sid]+=1
  records=[]
  for r in source_rows:
   sid=r['name'];mf=matched[sid];missing=[fn for fn in FILES if not mf[fn]];duplicate=[fn for fn in FILES if len(mf[fn])>1]
   empty=[fn for fn in FILES if len(mf[fn])==1 and mf[fn][0].file_size==0]
   status='DUPLICATE' if duplicate else 'MISSING' if missing else 'EMPTY' if empty else 'PRESENT'
   reason=';'.join(['missing:'+','.join(missing)] if missing else [] + [])
   if duplicate:reason+=';duplicate:'+','.join(duplicate)
   if empty:reason+=';empty:'+','.join(empty)
   xt=mf['samples.xtc'][0] if mf['samples.xtc'] else None; pd=mf['topology.pdb'][0] if mf['topology.pdb'] else None
   records.append({'system':sid,'is_mutant':r['mutant'],'wt':r['name_wt'],'status':status,'expected_frames':r['num_samples'],'xtc_bytes':xt.file_size if xt else '', 'pdb_bytes':pd.file_size if pd else '', 'xtc_member':xt.filename if xt else '', 'pdb_member':pd.filename if pd else '', 'reference_member':refs[sid][0] if len(refs[sid])==1 else '', 'reference_status':'UNIQUE' if len(refs[sid])==1 else 'MISSING_OR_AMBIGUOUS','reason':reason,'reference_sha256':refsha.get(sid)})
  status_counts=dict(Counter(r['status'] for r in records));check('154_complete_zip_pairs',status_counts.get('PRESENT',0)==154)
  check('112_complete_WT_mutant_pairs',all(next(s for s in records if s['system']==r['name'])['status']=='PRESENT' and next(s for s in records if s['system']==r['name_wt'])['status']=='PRESENT' for r in mutants))
  summary['archive_inventory']={'total_members':len(allmembers),'status_counts':status_counts,'outside_benchmark_system_count':len(extra),'outside_benchmark_examples':sorted(extra)[:20],'selected_example_outside_benchmark':{n:n in extra for n in a.selected.split(',') if n not in idset}}
  if a.full_crc:
   summary['archive_inventory']['crc_bad_member']=z.testzip();check('full_archive_crc',summary['archive_inventory']['crc_bad_member'] is None)
  selected=[i.strip() for i in a.selected.split(',') if i.strip()]; chosen=[i for i in selected if i in idset]
  per={k:{'benchmark_member':k in idset,'archive_member':k in extra or k in matched} for k in selected}
  for sid in chosen:
   row=next(r for r in records if r['system']==sid)
   if row['status']!='PRESENT':continue
   per[sid].update({'xtc_sha256':member_hash(z,row['xtc_member']),'pdb_sha256':member_hash(z,row['pdb_member']),'ref_sha256':refsha.get(sid),'status':'HASHED'})
  if a.full_member_hashes:
   with open(out/'all_154_member_hashes.csv','w',encoding='utf-8-sig',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=['system','xtc_sha256','pdb_sha256','ref_sha256']);wr.writeheader()
    for row in records:
     if row['status']=='PRESENT':wr.writerow({'system':row['system'],'xtc_sha256':member_hash(z,row['xtc_member']),'pdb_sha256':member_hash(z,row['pdb_member']),'ref_sha256':row['reference_sha256']})
  if a.coordinate_qa:
   try:import mdtraj as md
   except ImportError:
    summary['warnings'].append('Optional --coordinate-qa requested, but mdtraj unavailable')
   else:
    with zipfile.ZipFile(bench) as bz,tempfile.TemporaryDirectory(prefix='ntbe_L1_') as tmp:
     for sid in chosen:
      row=next(r for r in records if r['system']==sid)
      if row['status']!='PRESENT':continue
      try:
       folder=Path(tmp)/sid;folder.mkdir()
       paths=[]
       for member,fn in [(row['xtc_member'],'samples.xtc'),(row['pdb_member'],'topology.pdb')]:
        dest=folder/fn
        with z.open(member) as inf, open(dest,'wb') as outf:shutil.copyfileobj(inf,outf)
        paths.append(dest)
       ref=folder/'reference.pdb'
       with open(ref,'wb') as f:f.write(bz.read(row['reference_member']))
       traj=md.load_xtc(str(paths[0]),top=str(paths[1])); reftr=md.load_pdb(str(ref))
       observed=traj.top.to_fasta(); reference_seq=reftr.top.to_fasta()
       official_seq=next(r['sequence'] for r in source_rows if r['name']==sid)
       per[sid]['coordinate_qa']={'status':'PASS' if observed==reference_seq and observed==[official_seq] else 'FAIL','frames':int(traj.n_frames),'atoms':int(traj.n_atoms),'residues':int(traj.n_residues),'chains':int(traj.top.n_chains),'sequence_sample':observed,'sequence_reference':reference_seq,'sequence_metadata':official_seq,'frame_count_matches_metadata':int(traj.n_frames)==int(next(r['num_samples'] for r in source_rows if r['name']==sid)),'finite_first_frame':bool(__import__('numpy').isfinite(traj.xyz[0]).all())}
      except Exception as ex:per[sid]['coordinate_qa']={'status':'ERROR','detail':repr(ex)}
  summary['selected']=per
 report_csv(out/'inventory_154.csv',records)
 # Optional historical outputs are checked by ID/schema only; they are not sources for physical coordinates.
 optional={'all_npz':a.all_npz or root/'all_npz(1).zip','core':a.core or root/'NTBE_Session3_output_new.zip','recovery':a.recovery or root/'NTBE_Session3_recovery.zip','systems':a.systems or root/'NTBE_systems_154_reconciled.csv'}
 opt={}
 for label,p in optional.items():
  p=Path(p)
  if not p.exists():opt[label]={'status':'NOT_SUPPLIED'};continue
  entry={'status':'PRESENT','sha256':digest_path(p),'bytes':p.stat().st_size}
  if p.suffix.lower()=='.zip':
   with zipfile.ZipFile(p) as q:
    m=[Path(n).stem for n in q.namelist() if n.endswith('.npz')];entry['npz_count']=len(m);entry['unique_npz_ids']=len(set(m));entry['benchmark_npz_ids']=len(set(m)&idset);entry['nonbenchmark_npz_ids']=sorted(set(m)-idset);entry['missing_benchmark_ids']=sorted(idset-set(m))
    entry['crc_bad_member']=q.testzip();
  elif p.suffix.lower()=='.csv':
   with open(p,encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f);columns=reader.fieldnames;rr=list(reader)
   k='name' if 'name' in columns else 'system' if 'system' in columns else None
   entry['rows']=len(rr);entry['id_column']=k;entry['unique_systems']=len(set(x[k] for x in rr)) if k else None;entry['id_matches_benchmark']=set(x[k] for x in rr)==idset if k else None
  opt[label]=entry
 summary['historical_outputs']=opt
 if opt.get('all_npz',{}).get('status')=='PRESENT':check('all_154_omega_npz_present',opt['all_npz'].get('benchmark_npz_ids')==154 and opt['all_npz'].get('unique_npz_ids')==154)
 if opt.get('systems',{}).get('status')=='PRESENT':check('final_system_table_ids_match',opt['systems'].get('id_matches_benchmark') is True)
 summary['elapsed_sec']=round(time.monotonic()-started,3)
 summary['overall_status']='PASS' if all(summary['checks'].values()) and all(v.get('coordinate_qa',{}).get('status','PASS')=='PASS' for v in per.values()) else 'ATTENTION'
 with open(out/'L1_report.json','w',encoding='utf-8') as f:json.dump(summary,f,indent=2,ensure_ascii=False)
 with open(out/'L1_manifest_sha256.txt','w',encoding='utf-8') as f:
  for p in sorted(out.iterdir()):
   if p.is_file() and p.name!='L1_manifest_sha256.txt':f.write(f'{digest_path(p)}  {p.name}\n')
 print(json.dumps({'overall_status':summary['overall_status'],'checks':summary['checks'],'inventory':summary['archive_inventory'],'selected':{k:v.get('coordinate_qa',v.get('status','NOT_IN_BENCHMARK')) for k,v in per.items()},'output_folder':str(out),'elapsed_sec':summary['elapsed_sec']},indent=2,ensure_ascii=False))
 return 0 if summary['overall_status']=='PASS' else 2
if __name__=='__main__':
 try:sys.exit(run(parse_args()))
 except Exception as exc:
  print('L1_FATAL:',repr(exc),file=sys.stderr);traceback.print_exc();sys.exit(1)
