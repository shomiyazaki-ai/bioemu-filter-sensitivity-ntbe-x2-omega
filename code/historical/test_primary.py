import unittest, tempfile, pathlib, csv
import numpy as np
from ntbe_x2_primary import stats, make_pairs, writecsv, readcsv, folded, dg
from ntbe_x2_omega_pilot import classify_omega

class PrimaryTests(unittest.TestCase):
 def test_classes_pro_and_nonpro(self):
  angles=np.array([[0.,180.,90.,np.nan],[180.,0.,149.,20.]])
  cats=classify_omega(angles,np.array([True,False,True,False]))
  self.assertEqual(cats['twisted'].sum(),2)
  self.assertEqual(cats['unknown'].sum(),1)
  self.assertTrue(cats['cis'][0,0])
  self.assertFalse(cats['twisted'][0,0])
 def test_fractions_and_clipping(self):
  q=np.array([.1,.7,.9]); f=folded(q)
  a,p=dg(q)
  self.assertAlmostEqual(p,f.mean())
  self.assertTrue(np.isfinite(a))
 def test_pairs_shared_wt_and_descriptive_error(self):
  d={'wt':dict(name='wt',status='PASS',dg_B0=-3.,dg_Bomega=-3.2,delta_dg_Bomega_minus_B0=-.2,
       unknown_excluded_dg=-3.2,n_unknown_frames=0,near_boundary_frames=0,lowN_Bomega_le10=False,
       under70pct_Bomega=False,clip_Bomega=False),
    'mut':dict(name='mut',status='PASS',dg_B0=-2.,dg_Bomega=-2.4,delta_dg_Bomega_minus_B0=-.4,
       unknown_excluded_dg=-2.4,n_unknown_frames=0,near_boundary_frames=0,lowN_Bomega_le10=False,
       under70pct_Bomega=False,clip_Bomega=False)}
  for v in d.values():v['boundary_conservative_dg']=v['dg_Bomega'];v['boundary_permissive_dg']=v['dg_Bomega']
  core=[dict(mutant='mut',wt='wt',ddg_exp='1.4',ddg_B='1.0')]
  r=make_pairs(list(d.values()),core)[0]
  self.assertAlmostEqual(r['D_Bomega_minus_B0'],-.2)
  self.assertAlmostEqual(r['delta_abs_err_Bomega_minus_B0'],.2)
 def test_missing_system_is_inconclusive(self):
  r=make_pairs([{'name':'mut','status':'FAIL'}],[dict(mutant='mut',wt='wt',ddg_exp='1',ddg_B='0')])[0]
  self.assertEqual(r['status'],'INCONCLUSIVE')
 def test_csv_and_summary(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td)/'out.csv';writecsv(p,[{'a':1,'b':3},{'a':2,'c':4}]);self.assertEqual(len(readcsv(p)),2)
  self.assertEqual(stats([-.2,.1,.3])['n'],3)
if __name__=='__main__':unittest.main()
