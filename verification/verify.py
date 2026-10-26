"""V0-V2 read-only independent verifier, v1.0.0. Never imports the primary code.
Run test_numerics.py first. Input numerical CSVs are opened only AFTER NPZ computation.
"""
import argparse,csv,hashlib,io,json,math,platform,sys,time,zipfile
from pathlib import Path
import numpy as np
from numerics import *
VERSION='1.0.0'
STAGES=['A','B0','Bomega']
EDGES=[('A','B0'),('B0','Bomega'),('A','Bomega')]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def write_csv(path,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def boolean(s):
    if str(s).lower() not in ('true','false'):raise ValueError('bad boolean')
    return str(s).lower()=='true'

def main(root,out):
    start=time.time();out.mkdir(parents=True,exist_ok=False)
    spec=json.loads((root/'verification/acceptance_spec.json').read_text());tol=spec['tolerances']
    checks=[];errors=[];comparisons=[];intervals=[];members=[];thresholds=[]
    def check(label,condition,detail=None):
        r=dict(check=label,pass_=bool(condition),detail=detail);checks.append(r)
        if not condition:errors.append(r)
    def compare(group,id,computed,saved,tolerance):
        saved=float(saved);error=abs(computed-saved)
        ok=math.isfinite(computed) and math.isfinite(saved) and error<=tolerance
        r=dict(group=group,id=id,computed=computed,saved=saved,abs_error=error,tolerance=tolerance,pass_=ok)
        comparisons.append(r)
        if not ok:errors.append(r)
    manifest=json.loads((root/'verification/input_manifest.json').read_text())
    for r in manifest:
        p=root/r['path'];check('input_sha256:'+r['path'],p.is_file() and sha(p)==r['sha256'])
    if errors:
        dump(out/'verification.json',dict(status='FAIL',version=VERSION,failures=errors));return 2
    meta=unique(read_csv(root/'sources/official/system_info.csv'),'name',154)
    baselines={k for k,v in meta.items() if not boolean(v['mutant'])}
    mutants=set(meta)-baselines
    check('42 baselines / 112 mutants',len(baselines)==42 and len(mutants)==112)
    check('matched baseline mapping',all(meta[k]['name_wt'] in baselines for k in mutants) and all(meta[k]['name_wt']==k for k in baselines))
    # Original geometry NPZs, including the single recovered member. No result CSV read yet.
    core={}
    for arc in ['NTBE_Session3_output_new.zip','NTBE_Session3_recovery.zip']:
        with zipfile.ZipFile(root/'data/inputs'/arc) as z:
            for name in z.namelist():
                if not name.endswith('.npz'):continue
                sid=Path(name).stem
                with np.load(io.BytesIO(z.read(name)),allow_pickle=False) as d:incoming={k:d[k] for k in d.files}
                if sid in core:
                    if arc!='NTBE_Session3_recovery.zip' or sid!='1TG0__D45C_N47P':raise ValueError('unexpected duplicate original FNC member')
                    check('documented recovery overlap exact',set(core[sid])==set(incoming) and all(np.array_equal(core[sid][k],incoming[k]) for k in incoming))
                core[sid]=incoming
    check('original 153+1 NPZ IDs',set(core)==set(meta))
    systems={};frames=[];boundary=[]
    with zipfile.ZipFile(root/'data/inputs/all_npz.zip') as z:
        names=[n for n in z.namelist() if not n.endswith('/')]
        check('154 unique NPZ members',len(names)==154 and len(set(names))==154 and {Path(n).stem for n in names}==set(meta) and all(n.endswith('.npz') for n in names))
        for name in sorted(names):
            sid=Path(name).stem;raw=z.read(name);members.append(dict(system=sid,member=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
            with np.load(io.BytesIO(raw),allow_pickle=False) as d:data={k:d[k] for k in d.files}
            q=np.asarray(data['fnc'],dtype=np.float64);n=len(q);b0=data['b0_mask'];bw=data['bomega_mask']
            validate_masks(b0,bw,n)
            check(sid+': fnc exact original',np.array_equal(data['fnc'],core[sid]['fnc']))
            check(sid+': geometry mask exact original',np.array_equal(b0,core[sid]['pass_all']))
            check(sid+': original geometry conjunction',np.array_equal(b0,core[sid]['pass_ca'] & core[sid]['pass_cn'] & core[sid]['pass_clash']))
            twist,unknown,reject,near=omega_masks(data['omega_degrees'],b0)
            check(sid+': omega mask exact',np.array_equal(bw,b0 & ~reject))
            check(sid+': stored rejected/unknown masks',np.array_equal(reject,data['twisted_frame_mask']) and np.array_equal(unknown,data['unknown_frame_mask']))
            check(sid+': stored near mask',np.array_equal(near,data['near_boundary_mask']))
            est={s:estimate(q[mask]) for s,mask in [('A',np.ones(n,bool)),('B0',b0),('Bomega',bw)]}
            check(sid+': nonempty all stages',all(v is not None for v in est.values()))
            row=dict(system=sid,matched_baseline=meta[sid]['name_wt'],is_mutant=boolean(meta[sid]['mutant']),target_frames=int(meta[sid]['num_samples']))
            for s,v in est.items():
                for key in ['n','p','dg','clipped']:row[key+'_'+s]=v[key]
            for a,b in EDGES:
                for key in ['p','dg']:row['delta_'+key+'_'+a+'_to_'+b]=est[b][key]-est[a][key]
                mask0=np.ones(n,bool) if a=='A' else b0
                mask1=b0 if b=='B0' else bw
                removed=mask0 & ~mask1
                row['removed_n_'+a+'_to_'+b]=int(removed.sum())
                if removed.any():
                    pr=estimate(q[removed])['p'];identity=int(removed.sum())*(est[a]['p']-pr)/est[b]['n']
                    check(sid+': foldedness removal identity '+a+'_'+b,abs(identity-(est[b]['p']-est[a]['p']))<=tol['delta_p'])
            row.update(twisted_bond_frames=int(twist[b0].sum()),evaluable_bond_frames=int(np.isfinite(data['omega_degrees'][b0]).sum()),unknown_frames=int(unknown.sum()),near_A=int(np.any(near,axis=1).sum()),near_B0=int((b0 & np.any(near,axis=1)).sum()),near_bonds_B0=int(near[b0].sum()))
            known=np.isfinite(data['omega_degrees']);dev=omega_deviation(data['omega_degrees'])
            row['min_omega_threshold_gap_deg']=float(np.min(np.abs(dev[known]-30)))
            # The two already-defined boundary scenarios, not new thresholds or error bounds.
            permissive=b0 & ~np.any(twist & ~near,axis=1)
            conservative=b0 & ~np.any(twist | near,axis=1) & ~unknown
            row['dg_boundary_permissive']=estimate(q[permissive])['dg']
            row['dg_boundary_conservative']=estimate(q[conservative])['dg']
            systems[sid]=row
    # Only now open historical numerical outputs for direct comparison.
    old=unique(read_csv(root/'data/frozen/NTBE_systems_154_reconciled.csv'),'name',154)
    omega=unique(read_csv(root/'data/frozen/systems_omega.csv'),'name',154)
    published_s=unique(read_csv(root/'data/frozen/Table_S2_S3_system_foldedness_dG.csv'),'name',154)
    check('system result ID sets',set(old)==set(meta)==set(omega)==set(published_s))
    for sid,row in systems.items():
        c=old[sid];w=omega[sid];ps=published_s[sid]
        check(sid+': old status/mapping',c['status']=='PASS' and w['status']=='PASS' and c['name_wt']==row['matched_baseline']==w['wt'] and boolean(c['is_mutant'])==row['is_mutant'])
        for key in ['dg_exp','ddg_exp']:compare('metadata_'+key,sid,float(meta[sid][key]),c[key],0)
        check(sid+': metadata target',int(float(c['num_samples_target']))==row['target_frames'])
        for s,pkey,gkey,source in [('A','p_fold_raw_A','dg_A',c),('B0','p_fold_raw_B','dg_B',c),('Bomega','p_Bomega','dg_Bomega',w)]:
            compare('p',sid+':'+s,row['p_'+s],source[pkey],tol['p'])
            compare('dg',sid+':'+s,row['dg_'+s],source[gkey],tol['dg'])
            lo,hi=dg_interval(row['p_'+s],tol['p']);saved=float(source[gkey]);ok=lo<=saved<=hi
            intervals.append(dict(id=sid,stage=s,p=row['p_'+s],epsilon_p=tol['p'],dg_lower=lo,dg_upper=hi,width=hi-lo,saved_dg=saved,contained=ok))
            check(sid+': nonlinear interval '+s,ok)
            published_p={'A':'p_fold_raw_A','B0':'p_fold_raw_B','Bomega':'p_Bomega'}[s]
            compare('published_p',sid+':'+s,row['p_'+s],ps[published_p],tol['p'])
            compare('published_dg',sid+':'+s,row['dg_'+s],ps['dg_'+s],tol['dg'])
        for a,b in EDGES:
            val=row['delta_dg_'+a+'_to_'+b]
            original=(float(c['dg_B'])-float(c['dg_A']) if b=='B0' else float(w['dg_Bomega'])-(float(c['dg_A']) if a=='A' else float(w['dg_B0'])))
            compare('delta_dg',sid+':'+a+'_'+b,val,original,tol['delta_dg'])
            original_p=(float(c['p_fold_raw_B'])-float(c['p_fold_raw_A']) if b=='B0' else float(w['p_Bomega'])-(float(c['p_fold_raw_A']) if a=='A' else float(w['p_B0'])))
            compare('delta_p',sid+':'+a+'_'+b,row['delta_p_'+a+'_to_'+b],original_p,tol['delta_p'])
        for key,expected in [('n_A',int(float(c['n_A']))),('n_B0',int(float(c['n_B']))),('n_Bomega',int(w['n_Bomega'])),('twisted_bond_frames',int(w['twisted_bonds'])),('evaluable_bond_frames',int(w['n_omega_evaluable'])),('unknown_frames',int(w['n_unknown_frames'])),('near_B0',int(w['near_boundary_frames'])),('near_bonds_B0',int(w['near_boundary_bonds']))]:check(sid+': exact '+key,row[key]==expected)
        for key in ['sha256_xtc','sha256_pdb']:check(sid+': source recorded hash '+key,c[key]==w[key])
        compare('stored_delta_dg',sid+':A_B0',row['delta_dg_A_to_B0'],c['delta_dg_BminusA'],tol['delta_dg'])
        compare('stored_delta_dg',sid+':B0_Bomega',row['delta_dg_B0_to_Bomega'],w['delta_dg_Bomega_minus_B0'],tol['delta_dg'])
        for scenario in ['permissive','conservative']:compare('boundary_dg',sid+':'+scenario,row['dg_boundary_'+scenario],w['boundary_'+scenario+'_dg'],tol['dg'])
    cp=unique(read_csv(root/'data/frozen/NTBE_pairs_112_reconciled.csv'),'mutant',112)
    wp=unique(read_csv(root/'data/frozen/pairs_omega.csv'),'mutant',112)
    pp=unique(read_csv(root/'data/frozen/Table_S4_cross_stage_112_pairs.csv'),'mutant',112)
    check('112 exact pair ID sets',set(cp)==mutants==set(wp)==set(pp))
    pairs=[]
    for sid in sorted(mutants):
        m=systems[sid];base=meta[sid]['name_wt'];w=systems[base];ex=float(meta[sid]['ddg_exp']);c=cp[sid];x=wp[sid];p=pp[sid]
        check(sid+': pair mapping/status',all(r['wt']==base for r in [c,x,p]) and c['status']=='PASS' and x['status']=='PASS')
        for r in [c,x]:compare('reference_ddg',sid,ex,r['ddg_exp'],0)
        row=dict(mutant=sid,matched_baseline=base,ddg_exp=ex)
        for s in STAGES:
            ddg,ae=pair(m['dg_'+s],w['dg_'+s],ex);row['ddg_'+s]=ddg;row['ae_'+s]=ae
            src=c if s=='A' else x;label=s
            compare('ddg',sid+':'+s,ddg,src['ddg_'+s],tol['ddg'])
            compare('ae',sid+':'+s,ae,src['abs_err_'+s],tol['ae'])
            compare('published_ddg',sid+':'+s,ddg,p['ddg_'+s],tol['ddg'])
            compare('published_ae',sid+':'+s,ae,p['abs_err_'+s],tol['ae'])
        for a,b in EDGES:
            edge=a+'_to_'+b;D=row['ddg_'+b]-row['ddg_'+a];E=row['ae_'+b]-row['ae_'+a]
            dm=m['delta_dg_'+edge];db=w['delta_dg_'+edge]
            row.update({ 'delta_ddg_'+edge:D,'delta_ae_'+edge:E,'mutant_dg_shift_'+edge:dm,'baseline_dg_shift_'+edge:db,
              'opposite_system_signs_'+edge:dm*db<0,'opposite_stage_signs':False})
            check(sid+': pair decomposition '+edge,abs(D-(dm-db))<=tol['delta_ddg'])
            original_D=(float(c['ddg_B'])-float(c['ddg_A']) if b=='B0' else float(x['ddg_Bomega'])-(float(c['ddg_A']) if a=='A' else float(x['ddg_B0'])))
            original_E=(float(c['abs_err_B'])-float(c['abs_err_A']) if b=='B0' else float(x['abs_err_Bomega'])-(float(c['abs_err_A']) if a=='A' else float(x['abs_err_B0'])))
            compare('delta_ddg',sid+':'+edge,D,original_D,tol['delta_ddg']);compare('delta_ae',sid+':'+edge,E,original_E,tol['delta_ae'])
            cl=classification(D,tol['delta_ddg']);ec=classification(E,tol['delta_ae'])
            thresholds.append(dict(mutant=sid,edge=edge,delta_ddg=D,delta_ae=E,threshold_ge_0p1=cl['ge_0p1'],near_0p1=cl['near_0p1'],near_ae_tie=ec['near_zero'],ae_sign=ec['sign'],ddg_threshold_distance=abs(abs(D)-.1),ae_zero_distance=abs(E)))
            check(sid+': threshold classification '+edge,cl['ge_0p1']==(abs(original_D)>=.1))
            check(sid+': AE classification '+edge,ec['sign']==(-1 if original_E<0 else 1 if original_E>0 else 0))
        for key,source,field,kind in [('delta_ddg_A_to_B0',c,'delta_ddg_BminusA','delta_ddg'),('delta_ddg_B0_to_Bomega',x,'D_Bomega_minus_B0','delta_ddg'),('delta_ddg_A_to_Bomega',p,'D_A_to_Bomega','delta_ddg'),('delta_ae_A_to_B0',c,'delta_abs_err_BminusA','delta_ae'),('delta_ae_B0_to_Bomega',x,'delta_abs_err_Bomega_minus_B0','delta_ae')]:compare('stored_'+kind,sid+':'+key,row[key],source[field],tol[kind])
        for edge,flag in [('A_to_B0','A_B0_flag'),('B0_to_Bomega','B0_Bomega_flag')]:check(sid+': stored threshold flag '+edge,(abs(row['delta_ddg_'+edge])>=.1)==boolean(p[flag]))
        row['opposite_stage_signs']=row['delta_ddg_A_to_B0']*row['delta_ddg_B0_to_Bomega']<0
        for scenario in ['conservative','permissive']:
            row['boundary_D_'+scenario]=m['dg_boundary_'+scenario]-w['dg_boundary_'+scenario]-row['ddg_B0']
            compare('boundary_pair',sid+':'+scenario,row['boundary_D_'+scenario],x['boundary_'+scenario+'_D'],tol['delta_ddg'])
        pairs.append(row)
    summary=dict(system_count=154,baseline_count=42,mutant_count=112,pair_count=112,frames={s:sum(r['n_'+s] for r in systems.values()) for s in STAGES},twisted_bond_frames=sum(r['twisted_bond_frames'] for r in systems.values()),evaluable_bond_frames=sum(r['evaluable_bond_frames'] for r in systems.values()),unknown_frames=sum(r['unknown_frames'] for r in systems.values()),near_A=sum(r['near_A'] for r in systems.values()),near_B0=sum(r['near_B0'] for r in systems.values()),clipped_stage_values=sum(r['clipped_'+s] for r in systems.values() for s in STAGES),min_Bomega=min(r['n_Bomega'] for r in systems.values()),stage_summaries={})
    for a,b in EDGES:
        edge=a+'_to_'+b;values={key:[r['delta_'+key+'_'+edge] for r in systems.values()] for key in ['p','dg']}
        values['ddg']=[r['delta_ddg_'+edge] for r in pairs]
        es={}
        for key,arr in values.items():
            es[key]=dict(min=min(arr),q25=float(np.quantile(arr,.25)),median=float(np.median(arr)),q75=float(np.quantile(arr,.75)),max=max(arr),positive=sum(v>0 for v in arr),negative=sum(v<0 for v in arr),zero=sum(v==0 for v in arr))
        es['ge_0p1']=sum(abs(r['delta_ddg_'+edge])>=.1 for r in pairs)
        es['ae_improved']=sum(r['delta_ae_'+edge]<0 for r in pairs);es['ae_worsened']=sum(r['delta_ae_'+edge]>0 for r in pairs);es['ae_tied']=sum(r['delta_ae_'+edge]==0 for r in pairs)
        summary['stage_summaries'][edge]=es
    summary['mae']={s:mean([r['ae_'+s] for r in pairs]) for s in STAGES}
    for s in STAGES:
        original=mean([float(cp[k]['abs_err_A']) if s=='A' else float(wp[k]['abs_err_'+s]) for k in sorted(mutants)])
        compare('mae',s,summary['mae'][s],original,tol['mae'])
    summary['delta_mae']={a+'_to_'+b:summary['mae'][b]-summary['mae'][a] for a,b in EDGES}
    for a,b in EDGES:
        def old_mae(s):return mean([float(cp[k]['abs_err_A']) if s=='A' else float(wp[k]['abs_err_'+s]) for k in sorted(mutants)])
        compare('delta_mae',a+'_to_'+b,summary['delta_mae'][a+'_to_'+b],old_mae(b)-old_mae(a),tol['delta_mae'])
    flags0={r['mutant'] for r in pairs if abs(r['delta_ddg_A_to_B0'])>=.1};flags1={r['mutant'] for r in pairs if abs(r['delta_ddg_B0_to_Bomega'])>=.1}
    summary.update(threshold_intersection=len(flags0 & flags1),threshold_union=len(flags0 | flags1),unstable_threshold_rows=sum(r['near_0p1'] for r in thresholds),unstable_ae_rows=sum(r['near_ae_tie'] for r in thresholds),boundary_scenario_ge_0p1={s:sum(abs(r['boundary_D_'+s])>=.1 for r in pairs) for s in ['conservative','permissive']},under70_Bomega=[r['system'] for r in systems.values() if r['n_Bomega']<.7*r['target_frames']])
    summary['boundary_not_bracketed']=[r['mutant'] for r in pairs if not min(r['boundary_D_conservative'],r['boundary_D_permissive'])-1e-12<=r['delta_ddg_B0_to_Bomega']<=max(r['boundary_D_conservative'],r['boundary_D_permissive'])+1e-12]
    maxima={g:dict(n=sum(r['group']==g for r in comparisons),max_abs_error=max(r['abs_error'] for r in comparisons if r['group']==g),tolerance=next(r['tolerance'] for r in comparisons if r['group']==g),failures=sum(not r['pass_'] for r in comparisons if r['group']==g)) for g in sorted({r['group'] for r in comparisons})}
    coverage={g:sum(r['group']==g for r in comparisons) for g in ['p','dg','ddg','ae']}
    check('full numerical coverage',coverage==dict(p=462,dg=462,ddg=336,ae=336),coverage)
    write_csv(out/'systems_recomputed.csv',list(systems.values()));write_csv(out/'pairs_recomputed.csv',pairs);write_csv(out/'comparison_details.csv',comparisons);write_csv(out/'nonlinear_intervals.csv',intervals);write_csv(out/'classification_diagnostics.csv',thresholds);write_csv(out/'npz_member_manifest.csv',members)
    dump(out/'summary.json',summary)
    result=dict(status='PASS' if not errors else 'FAIL',version=VERSION,scope='V0-V2 saved-input arithmetic; no raw-coordinate replay',environment=dict(python=sys.version,platform=platform.platform(),numpy=np.__version__),acceptance_spec_sha256=sha(root/'verification/acceptance_spec.json'),verifier_sha256=sha(Path(__file__)),numerics_sha256=sha(root/'verification/numerics.py'),input_hashes=manifest,coverage=coverage,maxima=maxima,checks=checks,failures=errors,nonlinear_interval_all_contained=all(r['contained'] for r in intervals),elapsed_seconds=time.time()-start)
    dump(out/'verification.json',result)
    print(json.dumps(dict(status=result['status'],coverage=coverage,failures=len(errors),mae=summary['mae'],maxima=maxima),indent=2))
    return 0 if not errors else 2
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    if any(args.out.resolve().is_relative_to((args.root/d).resolve()) for d in ['data/inputs','data/frozen','sources','code','verification']):raise SystemExit('Output must not be inside an input/code directory')
    try:sys.exit(main(args.root.resolve(),args.out.resolve()))
    except Exception as e:
        if args.out.is_dir():dump(args.out/'fatal.json',dict(status='FAIL',error=type(e).__name__,message=str(e),version=VERSION))
        raise
