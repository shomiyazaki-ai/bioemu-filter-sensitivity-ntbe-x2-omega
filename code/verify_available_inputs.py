import pathlib,pandas as pd,numpy as np
R=pathlib.Path(__file__).resolve().parent.parent
s=pd.read_csv(R/'data/NTBE_systems_154_reconciled.csv')
p=pd.read_csv(R/'data/NTBE_pairs_112_reconciled.csv')
assert len(s)==154 and len(p)==112
assert int(s.n_A.sum())==302800 and int(s.n_B.sum())==298188
assert int((abs(p.delta_ddg_BminusA)>=.1).sum())==19
assert np.isfinite(p[['ddg_A','ddg_B','delta_ddg_BminusA','abs_err_A','abs_err_B']].to_numpy()).all()
assert abs(p.abs_err_A.mean()-0.702595)<1e-6
assert abs(p.abs_err_B.mean()-0.696142)<1e-6
assert set(p.wt).issubset(set(s.name))
assert set(p.mutant).issubset(set(s.name))
print('PASS: available NT-BE historical tables. X2-omega outputs NOT tested.')
