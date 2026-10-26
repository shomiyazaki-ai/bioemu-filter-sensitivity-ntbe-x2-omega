"""NT-BE Session 3 fixed-archive retrospective filter sensitivity, P01-P15.
Run on the user's local 1.96GB archive. Python 3.13, numpy, scipy, Biopython, mdtraj.
No fitting, tuning, bootstrap, new filter, or source file modification.
"""
import argparse,csv,hashlib,io,json,math,os,pathlib,sys,tempfile,time,traceback,warnings,zipfile
import numpy as np
import mdtraj as md
from ntbe_official_filter_snapshot import filter_unphysical_traj_masks
from official_fnc_snapshot import FNCSettings,get_fnc_from_samples_trajectory,_compute_reference_contacts,_get_sequence_index_map
R=0.001987203599772605;T=295.;P_MIN=1e-10
PREFIX='bioemu-benchmarks/bioemu_benchmarks/assets/folding_free_energies_benchmark_0.1/folding_free_energies/'
FIELDS=['name','name_wt','mutant','dg_exp','ddg_exp','dg_ci95_low','dg_ci95_high','num_samples','sequence','wt_only_reference']
def float_or_nan(x):
 try:return float(x)
 except:return float('nan')
def bval(x):return str(x).strip().lower()=='true'
def h(b):return hashlib.sha256(b).hexdigest()
def require_unique(z,ending):
 entries=[n for n in z.namelist() if n.endswith(ending)]
 if len(entries)!=1:raise ValueError(f'Expected exactly one {ending!r}, found {len(entries)}')
 return entries[0]
def dg_stats(f):
 if not len(f):return dict(p_raw=None,p_clipped=None,clipped=False,ratio_clipped=False,dg=None)
 folded=1/(1+np.exp(-20*(np.asarray(f,dtype=np.float64)-.5)))
 p=float(np.mean(folded,dtype=np.float64))
 pc=float(np.clip(p,P_MIN,1-P_MIN));ratio=pc/(1-pc);rc=float(np.clip(ratio,P_MIN,1e10))
 return dict(p_raw=p,p_clipped=pc,clipped=bool(p!=pc),ratio_clipped=bool(ratio!=rc),dg=float(-np.log(rc)*R*T))
def write_csv(path, rows):
 if not rows:return
 keys=list(dict.fromkeys(k for row in rows for k in row.keys()))
 with path.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def mean_or_none(a):return float(np.mean(a)) if len(a) else None
def median_or_none(a):return float(np.median(a)) if len(a) else None
def iqr(a):return [float(v) for v in np.percentile(a,[25,75])] if len(a) else None
def summary_group(rows,field):
 v=np.array([float(x[field]) for x in rows if x.get(field) is not None and math.isfinite(float(x[field]))]);return {'n':len(v),'median':median_or_none(v),'iqr':iqr(v),'min':float(v.min()) if len(v) else None,'max':float(v.max()) if len(v) else None}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True);ap.add_argument('--bench',required=True);ap.add_argument('--out',required=True);ap.add_argument('--step2-dir',default=None);ap.add_argument('--systems',nargs='+',default=None,help='QA only; not for final primary');ap.add_argument('--geometry',choices=['none','step2'],default='none',help='Extra structural descriptors are recorded in a separate Step2 execution');a=ap.parse_args()
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);(out/'fnc').mkdir(exist_ok=True)
 started=time.time();rows=[];audit=[]
 with zipfile.ZipFile(a.bench) as zref, zipfile.ZipFile(a.archive) as zar:
  meta_name=require_unique(zref,'/folding_free_energies/system_info.csv')
  raw=zref.read(meta_name).decode('utf-8-sig');meta=list(csv.DictReader(io.StringIO(raw)))
  if len(meta)!=154 or len(set(r['name'] for r in meta))!=154:raise ValueError('Expected 154 unique benchmark systems')
  selected=[r for r in meta if a.systems is None or r['name'] in a.systems]
  if a.systems is not None and set(a.systems)!=set(r['name'] for r in selected):raise ValueError('Unknown requested system')
  for num,rec in enumerate(selected,1):
   sid=rec['name'];base={'name':sid,'name_wt':rec['name_wt'],'is_mutant':bval(rec['mutant']),'dg_exp':float_or_nan(rec['dg_exp']),'ddg_exp':float_or_nan(rec['ddg_exp']),'num_samples_target':int(rec['num_samples']),'wt_only_reference':bval(rec['wt_only_reference'])}
   t0=time.perf_counter()
   try:
    member_xtc=require_unique(zar,f'/{sid}/samples.xtc');member_pdb=require_unique(zar,f'/{sid}/topology.pdb');member_ref=require_unique(zref,f'/{sid}.pdb')
    if not member_ref.startswith(PREFIX+'reference_'):raise ValueError('Reference provenance invalid')
    xtc=zar.read(member_xtc);pdb=zar.read(member_pdb);ref=zref.read(member_ref)
    with tempfile.TemporaryDirectory() as td:
     d=pathlib.Path(td);(d/'a.xtc').write_bytes(xtc);(d/'a.pdb').write_bytes(pdb);(d/'r.pdb').write_bytes(ref)
     traj=md.load_xtc(str(d/'a.xtc'),top=str(d/'a.pdb'));reference=md.load_pdb(str(d/'r.pdb'))
    if not traj.n_frames or traj.top.n_chains!=1 or reference.top.n_chains!=1:raise ValueError('Empty or non-single-chain structure')
    if not np.isfinite(traj.xyz).all() or not np.isfinite(reference.xyz).all():raise ValueError('Nonfinite XYZ')
    # Explicit mapping QA. Original function will perform its own identical mapping.
    ss=traj.top.to_fasta()[0];rs=reference.top.to_fasta()[0];ms=rec['sequence']
    if ss!=ms:raise ValueError(f'Sample sequence disagrees with system_info: {ss[:30]}... vs {ms[:30]}...')
    mapping=_get_sequence_index_map(ss,rs)
    rc,rd=_compute_reference_contacts(reference_conformation=reference.atom_slice(reference.top.select('name CA')),sequence_separation=FNCSettings.sequence_separation,contact_cutoff=FNCSettings.contact_cutoff)
    if len(rc)==0:raise ValueError('No native contacts')
    if rc.max()>=len(mapping) or np.any(mapping[rc]<0):raise ValueError('Official FNC contact mapping incomplete or -1')
    # The only official physical filter; A=all, B=subset.
    ca,cn,cl=filter_unphysical_traj_masks(traj)
    keep=ca & cn & cl;n=int(traj.n_frames);nb=int(keep.sum())
    fnc=get_fnc_from_samples_trajectory(traj,reference,sequence_separation=FNCSettings.sequence_separation,contact_cutoff=FNCSettings.contact_cutoff,contact_beta=FNCSettings.contact_beta,contact_lambda=FNCSettings.contact_lambda,contact_delta=FNCSettings.contact_delta)
    if fnc.shape!=(n,) or not np.isfinite(fnc).all() or np.any((fnc<0)|(fnc>1)):raise ValueError('Bad FNC array')
    dga=dg_stats(fnc);dgb=dg_stats(fnc[keep]);low=nb<=10;under70=nb<0.7*int(rec['num_samples']);clip=any((v['clipped'] or v['ratio_clipped']) for v in [dga,dgb]);combined=low or under70 or clip
    entry={**base,'status':'PASS' if nb else 'B_EMPTY','n_A':n,'n_B':nb,'excluded_n':n-nb,'excluded_frac':(n-nb)/n,
      'fail_ca':int((~ca).sum()),'fail_cn':int((~cn).sum()),'fail_clash':int((~cl).sum()),'fail_any':n-nb,
      'pass_mask_overlap_qa':bool(np.array_equal(keep,ca&cn&cl)),
      'fnc_mean_A':mean_or_none(fnc),'fnc_mean_B':mean_or_none(fnc[keep]),'fnc_mean_removed':mean_or_none(fnc[~keep]),
      'dg_A':dga['dg'],'dg_B':dgb['dg'],'abs_dg_err_A':abs(dga['dg']-base['dg_exp']) if not base['wt_only_reference'] else None,'abs_dg_err_B':abs(dgb['dg']-base['dg_exp']) if nb and not base['wt_only_reference'] else None,'delta_dg_BminusA':dgb['dg']-dga['dg'] if dgb['dg'] is not None else None,
      'p_fold_raw_A':dga['p_raw'],'p_fold_raw_B':dgb['p_raw'],'p_fold_clipped_A':dga['p_clipped'],'p_fold_clipped_B':dgb['p_clipped'],
      'lowN_B_le10':low,'under70pct_B':under70,'clipping_any_AB':clip,'any_reliability_flag':combined,
      'ca_only_fail':int((~ca & cn & cl).sum()),'cn_only_fail':int((ca & ~cn & cl).sum()),'clash_only_fail':int((ca & cn & ~cl).sum()),
      'two_or_three_fail':int(((~ca).astype(int)+(~cn).astype(int)+(~cl).astype(int)>=2).sum()),
      'seq_sample_equals_meta':ss==ms,'sequence_reference':rs,'reference_contact_pairs':len(rc),
      'sha256_xtc':h(xtc),'sha256_pdb':h(pdb),'sha256_reference':h(ref),'reference_member':member_ref,'elapsed_sec':round(time.perf_counter()-t0,3)}
    np.savez_compressed(out/'fnc'/f'{sid}.npz',fnc=fnc.astype('float32'),pass_ca=ca,pass_cn=cn,pass_clash=cl,pass_all=keep)
    if a.step2_dir and (pathlib.Path(a.step2_dir)/f'{sid}.npz').exists():
     with np.load(pathlib.Path(a.step2_dir)/f'{sid}.npz') as old:
      entry['step2_mask_match']=all(np.array_equal(old[k],val) for k,val in [('pass_ca',ca),('pass_cn',cn),('pass_clash',cl),('pass_all',keep)])
      if not entry['step2_mask_match']:raise ValueError('Step2 mask mismatch')
    print(f'[{num}/{len(selected)}] {sid}: A={n},B={nb},dG(A)={dga["dg"]:.4f},dG(B)={dgb["dg"] if nb else "NA"}',flush=True)
   except Exception as e:
    entry={**base,'status':'FAIL_QA','error':str(e),'traceback':traceback.format_exc(),'elapsed_sec':round(time.perf_counter()-t0,3)};print(f'[{num}/{len(selected)}] {sid}: FAIL_QA {e}',flush=True)
   rows.append(entry);write_csv(out/'systems.csv',rows)
  by={x['name']:x for x in rows};pairs=[]
  for m in [r for r in selected if bval(r['mutant'])]:
   mut=by[m['name']];wt=by.get(m['name_wt']);p={'mutant':m['name'],'wt':m['name_wt'],'ddg_exp':float_or_nan(m['ddg_exp'])}
   if wt is None or any(v.get('dg_B') is None for v in [mut,wt]):p['status']='NOT_COMPARABLE';p['reason']='WT missing or A/B dG unavailable'
   else:
    a_ddg=mut['dg_A']-wt['dg_A'];b_ddg=mut['dg_B']-wt['dg_B'];ex=p['ddg_exp'];ea=abs(a_ddg-ex);eb=abs(b_ddg-ex)
    p.update(status='PASS',ddg_A=a_ddg,ddg_B=b_ddg,delta_ddg_BminusA=b_ddg-a_ddg,abs_err_A=ea,abs_err_B=eb,delta_abs_err_BminusA=eb-ea,
      flag_lowN=mut['lowN_B_le10'] or wt['lowN_B_le10'],flag_under70=mut['under70pct_B'] or wt['under70pct_B'],flag_clip=mut['clipping_any_AB'] or wt['clipping_any_AB'],flag_any=mut['any_reliability_flag'] or wt['any_reliability_flag'])
   pairs.append(p)
  write_csv(out/'pairs.csv',pairs)
  valid_sys=[x for x in rows if x.get('dg_B') is not None];valid_pairs=[p for p in pairs if p['status']=='PASS']
  sensitivities=[]
  for label,key in [('S0_all',None),('S1_no_lowN','lowN_B_le10'),('S2_no_under70','under70pct_B'),('S3_no_clipping','clipping_any_AB'),('S4_no_flags','any_reliability_flag')]:
   sysrows=[r for r in valid_sys if key is None or not r[key]]
   keypair={None:None,'lowN_B_le10':'flag_lowN','under70pct_B':'flag_under70','clipping_any_AB':'flag_clip','any_reliability_flag':'flag_any'}[key]
   pairrows=[p for p in valid_pairs if keypair is None or not p[keypair]]
   delta_dgs=[r['delta_dg_BminusA'] for r in sysrows];delta_ddgs=[p['delta_ddg_BminusA'] for p in pairrows]
   e_a=[p['abs_err_A'] for p in pairrows];e_b=[p['abs_err_B'] for p in pairrows]
   sensitivities.append({'analysis':label,'n_system':len(sysrows),'n_pair':len(pairrows),'dg_delta_median':median_or_none(delta_dgs),'dg_delta_iqr':iqr(delta_dgs),'ddg_delta_median':median_or_none(delta_ddgs),'ddg_delta_iqr':iqr(delta_ddgs),'mae_A':mean_or_none(e_a),'mae_B':mean_or_none(e_b),'delta_mae_BminusA':(float(np.mean(e_b)-np.mean(e_a)) if e_a else None),'improved_n':sum(p['delta_abs_err_BminusA']<0 for p in pairrows),'worsened_n':sum(p['delta_abs_err_BminusA']>0 for p in pairrows),'unchanged_n':sum(p['delta_abs_err_BminusA']==0 for p in pairrows)})
  write_csv(out/'sensitivity.csv',sensitivities)
  complete=(a.systems is None and len(rows)==154 and len(pairs)==112)
  report={'protocol':'NT-BE P01–P15 v1.0','analysis_scope':'FULL' if complete else 'SUBSET_QA_ONLY','system_total':len(rows),'system_computable':len(valid_sys),'system_failed':sum(x['status']=='FAIL_QA' for x in rows),'pair_total':len(pairs),'pair_computable':len(valid_pairs),'system_delta_dg':summary_group(valid_sys,'delta_dg_BminusA'),'pair_delta_ddg':summary_group(valid_pairs,'delta_ddg_BminusA'),'dg_mae_A_nonreference':mean_or_none([x['abs_dg_err_A'] for x in valid_sys if x['abs_dg_err_A'] is not None]),'dg_mae_B_nonreference':mean_or_none([x['abs_dg_err_B'] for x in valid_sys if x['abs_dg_err_B'] is not None]),'sensitivity':sensitivities,'caution':'Archived XTC A may already have undergone generation filtering. P15 changes sample composition, not dG calculation. No independent experimental validation or generalizable improvement claimed.','benchmark_sha256':h(pathlib.Path(a.bench).read_bytes()),'elapsed_wall_sec':round(time.time()-started,2)}
  (out/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False),encoding='utf-8');print('OUTPUT:',out.resolve(),'full:',complete)
  if not complete or report['system_failed']>0 or report['system_computable']<154 or report['pair_computable']<112:sys.exit(2)
if __name__=='__main__':main()
