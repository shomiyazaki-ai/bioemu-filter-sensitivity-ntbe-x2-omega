import pathlib,zipfile,json,hashlib,pandas as pd,numpy as np
R=pathlib.Path(__file__).resolve().parent.parent
s=pd.read_csv(R/'data/NTBE_systems_154_reconciled.csv');so=pd.read_csv(R/'data/systems_omega.csv');p=pd.read_csv(R/'data/NTBE_pairs_112_reconciled.csv');po=pd.read_csv(R/'data/pairs_omega.csv')
sj=s.merge(so,on='name',validate='one_to_one',suffixes=('_old','_omega'));pj=p.merge(po,on=['mutant','wt'],validate='one_to_one',suffixes=('_old','_omega'))
assert len(sj)==154 and len(pj)==112
assert (sj.n_B==sj.n_B0).all() and np.allclose(sj.dg_B,sj.dg_B0,atol=1e-10)
assert np.allclose(pj.ddg_B,pj.ddg_B0,atol=1e-10)
assert [sj.n_A_old.sum(),sj.n_B0.sum(),sj.n_Bomega.sum()]==[302800,298188,272381]
assert [(pj.delta_ddg_BminusA.abs()>=.1).sum(),(pj.D_Bomega_minus_B0.abs()>=.1).sum(),((pj.ddg_Bomega-pj.ddg_A).abs()>=.1).sum()]==[19,40,44]
assert abs(p.abs_err_A.mean()-0.702595)<1e-6 and abs(p.abs_err_B.mean()-0.696142)<1e-6 and abs(po.abs_err_Bomega.mean()-0.707681)<1e-6
z=zipfile.ZipFile(R/'data/all_npz.zip');assert len(z.namelist())==154 and z.testzip() is None
assert hashlib.sha256((R/'data/all_npz.zip').read_bytes()).hexdigest()=='569a09744787d2c6c9b35e9e0cc80ce2ef4dd40d6a3f494cd45fe33bed8584b7'
for f in z.namelist():
 with z.open(f) as g:
  a=np.load(g);q=so.loc[so.name==pathlib.Path(f).stem].iloc[0]
  assert len(a['fnc'])==int(q.n_A) and int(a['b0_mask'].sum())==int(q.n_B0) and int(a['bomega_mask'].sum())==int(q.n_Bomega)
  assert np.all(a['bomega_mask']<=a['b0_mask'])
print('PASS: 154 NPZ, 154 systems, 112 pairs, stage joins, count thresholds, three MAEs, frozen NPZ ZIP checksum')
