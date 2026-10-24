"""NT-BE-X2-omega: limited preflight/pilot only; no full-population inference.
Requires: Python, numpy, mdtraj. Benchmark reference CSV is read from benchmark ZIP.
Uses raw XTC for omega; reuses official baseline mask and FNC in Session3 NPZ.
"""
import argparse, csv, hashlib, io, json, math, pathlib, tempfile, zipfile
import numpy as np
import mdtraj as md

R=0.001987203599772605; T=295.; CUTOFF=30.0

def wrap(a): return (a+180.)%360.-180.
def deviation(a):
    a=wrap(a)
    return np.minimum(np.abs(a), np.abs(wrap(a-180.)))
def four_point_degrees(x):
    # x shape: (frames,bonds,4,3), reference-independent torsion computation
    b0=-(x[:,:,1]-x[:,:,0]);b1=x[:,:,2]-x[:,:,1];b2=x[:,:,3]-x[:,:,2]
    norm=np.linalg.norm(b1,axis=-1)
    valid=np.isfinite(x).all(axis=(-1,-2)) & (norm>1e-9)
    u=np.divide(b1,norm[...,None],out=np.zeros_like(b1),where=(norm[...,None]>1e-9))
    v=b0-np.sum(b0*u,axis=-1)[...,None]*u
    w=b2-np.sum(b2*u,axis=-1)[...,None]*u
    nv=np.linalg.norm(v,axis=-1);nw=np.linalg.norm(w,axis=-1)
    valid &= (nv>1e-9)&(nw>1e-9)
    out=np.degrees(np.arctan2(np.sum(np.cross(u,v)*w,axis=-1),np.sum(v*w,axis=-1)))
    out[~valid]=np.nan
    return out

def classify_omega(angles, is_pro):
    """Mutually exclusive cis / trans / twisted / unknown; Pro is NEXT residue."""
    angles=np.asarray(angles,dtype=np.float64)
    is_pro=np.asarray(is_pro,dtype=bool)
    if angles.ndim!=2 or is_pro.shape!=(angles.shape[1],):
        raise ValueError("omega and next-is-Pro shape mismatch")
    d=deviation(angles); known=np.isfinite(angles)
    twisted=known&(d>CUTOFF)
    cis=known&~twisted&(np.abs(wrap(angles))<=CUTOFF)
    trans=known&~twisted&(np.abs(wrap(angles-180.))<=CUTOFF)
    unknown=~known
    if not np.array_equal(known,cis|trans|twisted) or np.any(cis&trans):
        raise ValueError("omega category partition invalid")
    return dict(known=known,twisted=twisted,cis=cis,trans=trans,unknown=unknown)

def dg(q):
    if not len(q):return None,None
    f=1/(1+np.exp(-20*(np.asarray(q,dtype=np.float64)-.5)))
    p=float(np.mean(f))
    pc=float(np.clip(p,1e-10,1-1e-10)); ratio=float(np.clip(pc/(1-pc),1e-10,1e10))
    return float(-R*T*np.log(ratio)),p

def only_zip_member(z,suffix):
    paths=[x for x in z.namelist() if x.endswith(suffix)]
    if len(paths)!=1:raise ValueError(f'{suffix}: expected unique ZIP member; got {len(paths)}')
    return paths[0]

def npz_field(z, choices, shape):
    candidates=[k for k in choices if k in z.files and z[k].shape==shape]
    if len(candidates)!=1: raise ValueError(f'NPZ keys {z.files}; expected one of {choices} shape {shape}')
    return z[candidates[0]], candidates[0]

def backbone_atoms(top):
    residues=list(top.residues)
    if top.n_chains!=1 or len(residues)<2:raise ValueError('SYSTEM_QA_FAIL: chain count or length')
    bond_array=[]; problems=[]; pro=[]
    for i in range(len(residues)-1):
        a,b=residues[i:i+2]; atom_indices=[]
        for res,atom_name in [(a,'CA'),(a,'C'),(b,'N'),(b,'CA')]:
            hits=[atom.index for atom in res.atoms if atom.name==atom_name]
            if len(hits)!=1:
                if len(hits)>1: raise ValueError('SYSTEM_QA_FAIL: ambiguous duplicate backbone atoms')
                problems.append({'bond_start_residue_index':i,'reason':f'{res.index}:{atom_name} count=0'})
                atom_indices=None;break
            atom_indices.append(hits[0])
        bond_array.append(atom_indices)
        pro.append(b.name.upper()=='PRO')
    return bond_array, problems, np.asarray(pro,dtype=bool)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--archive',required=True);ap.add_argument('--bench',required=True)
    ap.add_argument('--fnc-dir',required=True);ap.add_argument('--systems',nargs='+',required=True)
    ap.add_argument('--out',required=True);ap.add_argument('--step2-dir',default='')
    args=ap.parse_args();out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    core={r['name']:r for r in csv.DictReader(open(pathlib.Path(__file__).with_name('NTBE_systems_154_reconciled.csv'),encoding='utf-8-sig'))}
    results=[]
    with zipfile.ZipFile(args.archive) as zar,zipfile.ZipFile(args.bench) as zref:
        metaname=only_zip_member(zref,'/folding_free_energies/system_info.csv')
        meta={r['name']:r for r in csv.DictReader(io.StringIO(zref.read(metaname).decode('utf-8-sig')))}
        for sid in args.systems:
            row={'system':sid,'status':'ERROR'}
            try:
                if sid not in core or sid not in meta: raise ValueError('system ID not in benchmark and core')
                rec=core[sid]; xtc=zar.read(only_zip_member(zar,f'/{sid}/samples.xtc'))
                pdb=zar.read(only_zip_member(zar,f'/{sid}/topology.pdb'))
                if hashlib.sha256(xtc).hexdigest()!=rec['sha256_xtc']:raise ValueError('XTC SHA-256 mismatch Core')
                if hashlib.sha256(pdb).hexdigest()!=rec['sha256_pdb']:raise ValueError('PDB SHA-256 mismatch Core')
                with tempfile.TemporaryDirectory() as td:
                    td=pathlib.Path(td);(td/'a.xtc').write_bytes(xtc);(td/'a.pdb').write_bytes(pdb)
                    traj=md.load_xtc(str(td/'a.xtc'),top=str(td/'a.pdb'))
                n=traj.n_frames
                if traj.top.to_fasta()[0]!=meta[sid]['sequence']:raise ValueError('SYSTEM_QA_FAIL: sequence mismatch')
                bonds,missing,is_pro=backbone_atoms(traj.top)
                if all(a is None for a in bonds):raise ValueError('SYSTEM_QA_FAIL: no evaluable peptide bonds')
                valid_positions=[i for i,a in enumerate(bonds) if a is not None]
                arr=np.asarray([bonds[i] for i in valid_positions],dtype=np.int32)
                xyz=traj.xyz[:,arr,:].astype(np.float64)*10 # mdtraj xyz in nm -> Angstrom
                sub_independent=four_point_degrees(xyz)
                independent=np.full((n,len(bonds)),np.nan,dtype=np.float64)
                independent[:,valid_positions]=sub_independent
                lib_idx,lib_rad=md.compute_omega(traj)
                lib_map={tuple(q.tolist()):i for i,q in enumerate(lib_idx)}
                if set(map(tuple,arr.tolist()))!=set(lib_map):raise ValueError('SYSTEM_QA_FAIL: omega atom index mapping differs')
                reference=np.full_like(independent,np.nan)
                reference[:,valid_positions]=np.column_stack([np.degrees(lib_rad[:,lib_map[tuple(a)]]) for a in arr])
                valid=np.isfinite(independent)&np.isfinite(reference)
                disagreement=np.abs(wrap(independent-reference))
                if np.any(valid) and np.max(disagreement[valid])>0.02:
                    raise ValueError('SYSTEM_QA_FAIL: independent-vs-MDTraj omega mismatch max='+str(np.max(disagreement[valid])))
                fnc_file=pathlib.Path(args.fnc_dir)/(sid+'.npz')
                with np.load(fnc_file,allow_pickle=False) as z:
                    mask,mask_key=npz_field(z,['keep','pass_all','mask','filter_mask','pass_mask','keep_mask'],(n,))
                    fnc,fnc_key=npz_field(z,['fnc','fnc_A','fnc_all','q','fnc_per_frame'],(n,))
                    mask=np.asarray(mask,dtype=bool);fnc=np.asarray(fnc,dtype=np.float64)
                if not np.isfinite(fnc).all() or np.any((fnc<0)|(fnc>1)):raise ValueError('bad FNC')
                if n!=int(float(rec['n_A'])) or int(mask.sum())!=int(float(rec['n_B'])):
                    raise ValueError('baseline frame count mismatch Core')
                d0,p0=dg(fnc[mask]);baseline_diff=d0-float(rec['dg_B'])
                if abs(baseline_diff)>1e-5:raise ValueError('baseline ΔG mismatch Core '+str(baseline_diff))
                if args.step2_dir:
                    sf=pathlib.Path(args.step2_dir)/(sid+'.npz')
                    if sf.exists():
                        with np.load(sf,allow_pickle=False) as z:
                            if not np.array_equal(mask,z['pass_all']):raise ValueError('Step2 mask mismatch')
                            # Compare omega to Step2 (first-residue index, same direction convention), if full matrix present
                            if 'omega_deg' in z.files and z['omega_deg'].shape==independent.shape:
                                delta=np.abs(wrap(independent-z['omega_deg']))
                                if np.any(np.isfinite(delta)) and np.nanmax(delta)>0.02:raise ValueError('Step2 omega mismatch')
                classes=classify_omega(independent,is_pro)
                unknown=classes['unknown'];twisted=classes['twisted']
                if not np.array_equal(classes['known'],valid):raise ValueError('omega known disagrees with MDTraj validity')
                # Values within numerical margin of threshold are separately recorded and NOT silently reclassified
                near=valid&(np.abs(deviation(independent)-CUTOFF)<=0.02)
                reject=np.any(twisted,axis=1)&mask
                unknown_frames=np.any(unknown,axis=1)&mask
                newmask=mask & ~reject
                dw,pw=dg(fnc[newmask]);nremove=int(reject.sum())
                # identity p_w-p_0 = r*(p_0-p_removed)/(n0-r) for removable frames
                removed_fold=1/(1+np.exp(-20*(fnc[reject]-.5)))
                p_rem=float(np.mean(removed_fold)) if nremove else None
                identity=(nremove*(p0-p_rem)/int(newmask.sum())) if nremove and len(fnc[newmask]) else 0.
                if pw is not None and abs((pw-p0)-identity)>1e-12:raise ValueError('folded fraction shift identity mismatch')
                row.update(status='PILOT_PASS',n_A=n,n_B0=int(mask.sum()),n_Bomega=int(newmask.sum()),removed=nremove,
                  evaluated_bonds=int(valid[mask].sum()),unknown_bonds=int(unknown[mask].sum()),unknown_frames=int(unknown_frames.sum()),missing_topology_bond_count=len(missing),missing_topology_examples=missing[:8],
                  unknown_kept_frames=int(np.sum(unknown_frames&newmask)),
                  twisted_bonds=int(twisted[mask].sum()),twisted_frames=nremove,
                  twisted_pro_bonds=int((twisted[:,is_pro]&mask[:,None]).sum()),
                  twisted_nonpro_bonds=int((twisted[:,~is_pro]&mask[:,None]).sum()),
                  cis_pro_bonds=int((classes['cis'][:,is_pro]&mask[:,None]).sum()),
                  cis_nonpro_bonds=int((classes['cis'][:,~is_pro]&mask[:,None]).sum()),
                  trans_pro_bonds=int((classes['trans'][:,is_pro]&mask[:,None]).sum()),
                  trans_nonpro_bonds=int((classes['trans'][:,~is_pro]&mask[:,None]).sum()),
                  unknown_pro_bonds=int((unknown[:,is_pro]&mask[:,None]).sum()),
                  unknown_nonpro_bonds=int((unknown[:,~is_pro]&mask[:,None]).sum()),
                  cis_pro_frames=int(np.sum(np.any(classes['cis'][:,is_pro],axis=1)&mask)),
                  cis_nonpro_frames=int(np.sum(np.any(classes['cis'][:,~is_pro],axis=1)&mask)),
                  trans_pro_frames=int(np.sum(np.any(classes['trans'][:,is_pro],axis=1)&mask)),
                  trans_nonpro_frames=int(np.sum(np.any(classes['trans'][:,~is_pro],axis=1)&mask)),
                  twisted_pro_frames=int(np.sum(np.any(twisted[:,is_pro],axis=1)&mask)),
                  twisted_nonpro_frames=int(np.sum(np.any(twisted[:,~is_pro],axis=1)&mask)),
                  near_boundary_bonds=int(near[mask].sum()),near_boundary_frames=int(np.sum(np.any(near,axis=1)&mask)),
                  omega_mdtraj_max_diff_deg=float(np.max(disagreement[valid])) if valid.any() else None,
                  baseline_core_delta_dg=baseline_diff,dg_B0=d0,dg_Bomega=dw,delta_dg_Bomega_minus_B0=(dw-d0 if dw is not None else None),
                  p_B0=p0,p_Bomega=pw,p_removed=p_rem,identity_error=(pw-p0-identity if pw is not None else None),
                  mask_key=mask_key,fnc_key=fnc_key,sha256_xtc=rec['sha256_xtc'])
                np.savez_compressed(out/(sid+'_omega_pilot.npz'),baseline_mask=mask,omega_mask=newmask,omega_degrees=independent.astype(np.float32),
                   twisted_mask=twisted,unknown_mask=unknown,cis_mask=classes["cis"],trans_mask=classes["trans"],near_boundary_mask=near,omega_atom_indices=np.asarray([a if a is not None else [-1,-1,-1,-1] for a in bonds],dtype=np.int32),next_is_pro=is_pro,fnc=fnc.astype(np.float32))
            except Exception as exc:
                row['status']='PILOT_FAIL';row['error']=repr(exc)
            results.append(row)
            print(sid,row['status'],row.get('error',''))
    report={'schema':'NTBE-X2-omega-pilot-v0.2','research_stage':'PREFLIGHT_ONLY','cutoff_deg':30.,'unknown_policy':'unknown retained and separately counted; systematic topology failure stops system', 'results':results,'all_pass':all(r['status']=='PILOT_PASS' for r in results)}
    (out/'omega_pilot_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    if not report['all_pass']:raise SystemExit(2)
if __name__=='__main__':main()
