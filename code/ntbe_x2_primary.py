"""NT-BE-X2-omega P01 fixed-archive primary. No parameter tuning.
Requires numpy, mdtraj; reads official archive and existing 154 Session3 FNC NPZ.
Does not silently omit systems/pairs or claim successful full primary on partial runs.
"""
import argparse, csv, hashlib, io, json, math, pathlib, tempfile, time, traceback, zipfile
import numpy as np
import mdtraj as md
from ntbe_x2_omega_pilot import (wrap, deviation, four_point_degrees, classify_omega,
                                   dg, only_zip_member, npz_field, backbone_atoms, R, T, CUTOFF)

CORE_FIELDS=['name','name_wt','is_mutant','status','n_A','n_B','dg_B','p_fold_raw_B','sha256_xtc','sha256_pdb']

def readcsv(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def writecsv(p,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def getbool(x):return str(x).lower()=='true'
def sha(x):return hashlib.sha256(x).hexdigest()
def folded(q):return 1/(1+np.exp(-20*(np.asarray(q,dtype=np.float64)-.5)))
def val(v):return None if v is None else float(v)
def stats(values):
    v=np.asarray([x for x in values if x is not None and math.isfinite(x)],dtype=float)
    return {'n':len(v),'median':float(np.median(v)) if len(v) else None,
            'q25':float(np.quantile(v,.25)) if len(v) else None,
            'q75':float(np.quantile(v,.75)) if len(v) else None,
            'max_abs':float(np.max(np.abs(v))) if len(v) else None}

def calc_system(sid,rec,meta,zar,fncdir,out,diag):
    row={'name':sid,'wt':rec['name_wt'],'is_mutant':getbool(rec['is_mutant']),'status':'FAIL'}
    xtc=zar.read(only_zip_member(zar,f'/{sid}/samples.xtc'))
    pdb=zar.read(only_zip_member(zar,f'/{sid}/topology.pdb'))
    if sha(xtc)!=rec['sha256_xtc'] or sha(pdb)!=rec['sha256_pdb']:
        raise ValueError('SOURCE_HASH_MISMATCH: XTC or PDB differs from Core')
    with tempfile.TemporaryDirectory() as td:
        d=pathlib.Path(td);(d/'x.xtc').write_bytes(xtc);(d/'t.pdb').write_bytes(pdb)
        tr=md.load_xtc(str(d/'x.xtc'),top=str(d/'t.pdb'))
    n=tr.n_frames
    if n!=int(float(rec['n_A'])) or tr.top.n_chains!=1:
        raise ValueError('CORE_FRAME_OR_CHAIN_MISMATCH')
    if tr.top.to_fasta()[0]!=meta[sid]['sequence']:
        raise ValueError('SEQUENCE_MISMATCH')
    residues=list(tr.top.residues)
    if any(r.chain.index != 0 for r in residues):raise ValueError('CHAIN_MAPPING_ERROR')
    bonds,missing,is_pro=backbone_atoms(tr.top)
    # A missing residue-specific atom becomes an Unknown bond, not a false normal.
    # Ambiguous duplicates/systematic topology breaks stop the system.
    if len(missing)>=len(bonds) or not bonds:raise ValueError('SYSTEMATIC_BACKBONE_MISSING')
    validpos=[i for i,a in enumerate(bonds) if a is not None]
    arr=np.asarray([bonds[i] for i in validpos],dtype=np.int32)
    xyz=tr.xyz[:,arr,:].astype(np.float64)*10.
    calculated=four_point_degrees(xyz)
    indep=np.full((n,len(bonds)),np.nan,dtype=np.float64)
    indep[:,validpos]=calculated
    # For missing atoms, mdtraj excludes a bond. Compare only shared fully specified atom indices.
    libidx,librad=md.compute_omega(tr)
    libmap={tuple(q.tolist()):i for i,q in enumerate(libidx)}
    expected=set(map(tuple,arr.tolist()))
    if not expected.issubset(set(libmap)):
        raise ValueError('OMEGA_MAPPING_MISSING_VALID_BONDS')
    if set(libmap)!=expected:
        # Extra omega four-tuples mean topology interpretation is ambiguous.
        raise ValueError('OMEGA_MAPPING_UNEXPECTED_EXTRA_BONDS')
    ref=np.full_like(indep,np.nan)
    ref[:,validpos]=np.column_stack([np.degrees(librad[:,libmap[tuple(a)]]) for a in arr])
    same=np.isfinite(indep)&np.isfinite(ref)
    if np.any(np.isfinite(indep)^np.isfinite(ref)):
        raise ValueError('OMEGA_FINITE_DISAGREEMENT')
    dis=np.abs(wrap(indep-ref))
    maxdis=float(np.max(dis[same])) if np.any(same) else None
    if maxdis is not None and maxdis>0.02:raise ValueError('OMEGA_4POINT_VS_MDTRAJ_MISMATCH')
    # Record but do not invent bondedness from geometry or silently call chain gaps normal.
    listed_bonds={tuple(sorted((a.index,b.index))) for a,b in tr.top.bonds}
    cn_top=[]
    for b in bonds:
        if b is None:cn_top.append('MISSING_ATOMS');continue
        cn_top.append('BONDED' if tuple(sorted((b[1],b[2]))) in listed_bonds else 'NOT_LISTED')
    mixed=('BONDED' in cn_top and 'NOT_LISTED' in cn_top)
    if mixed:raise ValueError('SYSTEMATIC_TOPOLOGY_CONNECTIVITY_AMBIGUITY: inconsistent C-N connectivity')
    top_unverified='BONDED' not in cn_top
    fpath=fncdir/(sid+'.npz')
    with np.load(fpath,allow_pickle=False) as z:
        mask,key=npz_field(z,['keep','pass_all','mask','filter_mask','pass_mask','keep_mask'],(n,))
        fnc,fkey=npz_field(z,['fnc','fnc_A','fnc_all','q','fnc_per_frame'],(n,))
        if mask.dtype!=np.bool_:raise ValueError('BASELINE_MASK_NONBOOLEAN')
        mask=mask.copy();fnc=np.asarray(fnc,dtype=np.float64)
    if not np.isfinite(fnc).all() or np.any((fnc<0)|(fnc>1)):raise ValueError('FNC_INVALID')
    if int(mask.sum())!=int(float(rec['n_B'])):raise ValueError('BASELINE_COUNT_MISMATCH')
    d0,p0=dg(fnc[mask])
    if d0 is None or abs(d0-float(rec['dg_B']))>1e-5:raise ValueError('BASELINE_DG_MISMATCH')
    if abs(p0-float(rec['p_fold_raw_B']))>1e-7:raise ValueError('BASELINE_FOLDED_FRAC_MISMATCH')
    cls=classify_omega(indep,is_pro)
    twisted=cls['twisted'];unknown=cls['unknown'];known=cls['known']
    if not np.array_equal(known,same):raise ValueError('CLASSIFICATION_MDTraj_DISAGREEMENT')
    near=known & (np.abs(deviation(indep)-CUTOFF)<=0.02)
    reject=mask & np.any(twisted,axis=1)
    uw=mask & np.any(unknown,axis=1)
    keep=mask & ~reject
    keep_unknown_excluded=keep & ~uw
    low_bound=mask & ~np.any(twisted & ~near,axis=1)
    high_bound=mask & ~np.any(twisted | near,axis=1) & ~uw
    dw,pw=dg(fnc[keep]);d_unknown,p_unknown=dg(fnc[keep_unknown_excluded])
    db_lo,_=dg(fnc[low_bound]);db_hi,_=dg(fnc[high_bound])
    nrem=int(reject.sum());rem_fold=folded(fnc[reject]);prem=float(np.mean(rem_fold)) if nrem else None
    if dw is not None and nrem:
        identity=nrem*(p0-prem)/(int(keep.sum()))
        if abs((pw-p0)-identity)>1e-12:raise ValueError('FOLDED_SHIFT_IDENTITY_MISMATCH')
    n_unknown=int(np.sum(uw));n_boundary=int(np.sum(mask & np.any(near,axis=1)))
    # Clipping flags in the same formulation as Core.
    def clip(q):
        if not len(q):return None
        pf=float(np.mean(folded(q)));pc=float(np.clip(pf,1e-10,1-1e-10))
        ratio=pc/(1-pc);return (pf!=pc) or ratio!=float(np.clip(ratio,1e-10,1e10))
    row.update(status='PASS' if dw is not None else 'BOMEGA_EMPTY',n_A=n,n_B0=int(mask.sum()),n_Bomega=int(keep.sum()),
               removed_omega=nrem,removed_fraction_B0=nrem/int(mask.sum()),n_bonds=len(bonds),n_pro_bonds=int(is_pro.sum()),
               n_omega_evaluable=int(known[mask].sum()),n_omega_unknown=int(unknown[mask].sum()),
               twisted_fraction_evaluable=(int(twisted[mask].sum())/int(known[mask].sum()) if int(known[mask].sum()) else None),
               n_unknown_frames=n_unknown,n_unknown_kept=int((uw&keep).sum()),
               n_missing_topology_bonds=len(missing),missing_topology_examples=json.dumps(missing[:6],ensure_ascii=False),
               n_nonfinite_or_degenerate_omega=int(unknown[:,validpos][mask].sum()),
               topology_connectivity_unverified=top_unverified,
               twisted_bonds=int(twisted[mask].sum()),twisted_pro_bonds=int(twisted[:,is_pro][mask].sum()),
               twisted_nonpro_bonds=int(twisted[:,~is_pro][mask].sum()),
               twisted_pro_frames=int((mask & np.any(twisted[:,is_pro],axis=1)).sum()),
               twisted_nonpro_frames=int((mask & np.any(twisted[:,~is_pro],axis=1)).sum()),
               cis_pro_bonds=int(cls['cis'][:,is_pro][mask].sum()),cis_nonpro_bonds=int(cls['cis'][:,~is_pro][mask].sum()),
               trans_pro_bonds=int(cls['trans'][:,is_pro][mask].sum()),trans_nonpro_bonds=int(cls['trans'][:,~is_pro][mask].sum()),
               unknown_pro_bonds=int(unknown[:,is_pro][mask].sum()),unknown_nonpro_bonds=int(unknown[:,~is_pro][mask].sum()),
               near_boundary_bonds=int(near[mask].sum()),near_boundary_frames=n_boundary,
               omega_mdtraj_max_diff_deg=maxdis,
               top_twisted_bond_positions=json.dumps([{'i_zero_based':int(i),'next_is_pro':bool(is_pro[i]),'n_B0_twisted':int(c)} for i,c in sorted(enumerate(twisted[mask].sum(axis=0)),key=lambda a:-a[1]) if c>0][:5],ensure_ascii=False),
               dg_B0=d0,dg_Bomega=dw,delta_dg_Bomega_minus_B0=(dw-d0 if dw is not None else None),
               p_B0=p0,p_Bomega=pw,p_removed=prem,unknown_excluded_dg=d_unknown,
               boundary_conservative_dg=db_hi,boundary_permissive_dg=db_lo,
               lowN_Bomega_le10=(int(keep.sum())<=10),under70pct_Bomega=(int(keep.sum())<.7*int(float(rec['num_samples_target']))),
               clip_Bomega=clip(fnc[keep]),mask_key=key,fnc_key=fkey,sha256_xtc=rec['sha256_xtc'],
               sha256_pdb=rec['sha256_pdb'],
               omega_max_per_frame_deg=float(np.nanmax(deviation(indep))) if np.any(known) else None)
    if diag:
        np.savez_compressed(out/'omega_masks'/f'{sid}.npz',b0_mask=mask,bomega_mask=keep,
          unknown_frame_mask=uw,twisted_frame_mask=reject,near_boundary_mask=near,
          omega_degrees=indep.astype(np.float32),next_is_pro=is_pro,
          omega_atom_indices=np.asarray([b if b is not None else [-1]*4 for b in bonds],dtype=np.int32),
          fnc=fnc.astype(np.float32))
    return row

def make_pairs(system_rows,core_pairs):
    by={x['name']:x for x in system_rows};ans=[]
    for cp in core_pairs:
        mut,wt=cp['mutant'],cp['wt'];rm=by.get(mut);rw=by.get(wt)
        r={'mutant':mut,'wt':wt,'ddg_exp':cp['ddg_exp'],'status':'INCONCLUSIVE'}
        if rm is None or rw is None:
            r['reason']='MISSING_SYSTEM';ans.append(r);continue
        if rm['status']!='PASS' or rw['status']!='PASS':
            r['reason']='SYSTEM_NOT_COMPUTABLE';ans.append(r);continue
        d0=rm['dg_B0']-rw['dg_B0'];dw=rm['dg_Bomega']-rw['dg_Bomega'];D=dw-d0
        if abs(d0-float(cp['ddg_B']))>1e-5:raise ValueError('PAIR_CORE_BASELINE_MISMATCH: '+mut)
        exp=float(cp['ddg_exp']);err0=abs(d0-exp);errw=abs(dw-exp)
        u0=rm['unknown_excluded_dg']-rw['unknown_excluded_dg'] if rm['unknown_excluded_dg'] is not None and rw['unknown_excluded_dg'] is not None else None
        bcons=(rm['boundary_conservative_dg']-rw['boundary_conservative_dg']-d0 if rm['boundary_conservative_dg'] is not None and rw['boundary_conservative_dg'] is not None else None)
        bperm=(rm['boundary_permissive_dg']-rw['boundary_permissive_dg']-d0 if rm['boundary_permissive_dg'] is not None and rw['boundary_permissive_dg'] is not None else None)
        r.update(status='PASS',boundary_conservative_D=bcons,boundary_permissive_D=bperm,ddg_B0=d0,ddg_Bomega=dw,D_Bomega_minus_B0=D,abs_D=abs(D),
                 mutant_system_shift=rm['delta_dg_Bomega_minus_B0'],wt_system_shift=rw['delta_dg_Bomega_minus_B0'],
                 abs_err_B0=err0,abs_err_Bomega=errw,delta_abs_err_Bomega_minus_B0=errw-err0,
                 unknown_excluded_D=(u0-d0 if u0 is not None else None),
                 either_unknown=(rm['n_unknown_frames']>0 or rw['n_unknown_frames']>0),
                 either_boundary=(rm['near_boundary_frames']>0 or rw['near_boundary_frames']>0),
                 either_lowN=(rm['lowN_Bomega_le10'] or rw['lowN_Bomega_le10']),
                 either_under70=(rm['under70pct_Bomega'] or rw['under70pct_Bomega']),
                 either_clipped=(rm['clip_Bomega'] or rw['clip_Bomega']))
        ans.append(r)
    return ans

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True);ap.add_argument('--bench',required=True)
    ap.add_argument('--fnc-dir',required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--systems',nargs='+',default=None,help='QA subset only; no primary claims')
    ap.add_argument('--no-per-frame',action='store_true',help='omit full diagnostic NPZ outputs')
    args=ap.parse_args();start=time.time();out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    if not args.no_per_frame:(out/'omega_masks').mkdir(exist_ok=True)
    base=pathlib.Path(__file__).parent
    cr=readcsv(base/'NTBE_systems_154_reconciled.csv');cp=readcsv(base/'NTBE_pairs_112_reconciled.csv')
    if len(cr)!=154 or len(cp)!=112 or len({x['name'] for x in cr})!=154 or len({x['mutant'] for x in cp})!=112:raise ValueError('CORE_CSV_ID_INVALID')
    if not all(x['status']=='PASS' for x in cr+cp):raise ValueError('CORE_CSV_NOT_FULLY_COMPUTABLE')
    selected={x['name'] for x in cr} if args.systems is None else set(args.systems)
    if not selected.issubset({x['name'] for x in cr}) or not selected:raise ValueError('BAD_SYSTEM_SELECTION')
    rows=[]
    with zipfile.ZipFile(args.archive) as zar,zipfile.ZipFile(args.bench) as zb:
        member=only_zip_member(zb,'/folding_free_energies/system_info.csv')
        meta={x['name']:x for x in csv.DictReader(io.StringIO(zb.read(member).decode('utf-8-sig')))}
        if set(meta)!={x['name'] for x in cr}:raise ValueError('BENCHMARK_SYSTEM_ID_SET_MISMATCH')
        for i,rec in enumerate(cr,1):
            sid=rec['name']
            if sid not in selected:continue
            t=time.perf_counter()
            try:r=calc_system(sid,rec,meta,zar,pathlib.Path(args.fnc_dir),out,not args.no_per_frame)
            except Exception as ex:r={'name':sid,'wt':rec['name_wt'],'status':'FAIL','error':str(ex),'traceback':traceback.format_exc(limit=4)}
            r['seconds']=round(time.perf_counter()-t,3);rows.append(r)
            print(f'{i:3d}/154 {sid}: {r["status"]}',flush=True)
    pairs=make_pairs(rows,cp);writecsv(out/'systems_omega.csv',rows);writecsv(out/'pairs_omega.csv',pairs)
    complete=(args.systems is None and len(rows)==154 and all(x['status']=='PASS' for x in rows) and len(pairs)==112 and all(x['status']=='PASS' for x in pairs))
    succ=[x for x in rows if x['status']=='PASS'];pc=[x for x in pairs if x['status']=='PASS']
    report={'schema':'NTBE-X2-omega-primary-v1','analysis_scope':'FULL' if args.systems is None else 'SUBSET_QA_ONLY',
       'full_primary_complete':complete,'cutoff_deg':CUTOFF,'unknown_rule':'keep if no observed twist',
       'system_selected':len(rows),'system_pass':len(succ),'system_fail':len(rows)-len(succ),
       'pair_total':112,'pair_computable':len(pc),
       'frames_B0':sum(x['n_B0'] for x in succ),'frames_Bomega':sum(x['n_Bomega'] for x in succ),
       'omega_removed':sum(x['removed_omega'] for x in succ),
       'unknown_frames':sum(x['n_unknown_frames'] for x in succ),
       'near_boundary_frames':sum(x['near_boundary_frames'] for x in succ),
       'D_summary':stats([x['D_Bomega_minus_B0'] for x in pc]),
       'abs_D_ge_0p1':sum(x['abs_D']>=.1 for x in pc),
       'mae_B0':float(np.mean([x['abs_err_B0'] for x in pc])) if pc else None,
       'mae_Bomega':float(np.mean([x['abs_err_Bomega'] for x in pc])) if pc else None,
       'seconds':round(time.time()-start,2),
       'notes':['Experimental error comparison is descriptive only.','No system selection for favorable outcomes.',
                'XTC byte hash plus baseline count/energy checked; source-independent trajectory recalculation not claimed.',
                'Shared WT pairs are dependent; do not treat 112 pairs as independent replicates.']}
    (out/'report_omega.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['full_primary_complete','system_pass','pair_computable','omega_removed']},ensure_ascii=False),flush=True)
    if not complete and args.systems is None:raise SystemExit(2)

if __name__=='__main__':main()
