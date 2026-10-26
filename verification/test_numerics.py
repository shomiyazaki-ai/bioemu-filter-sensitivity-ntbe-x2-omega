"""Artificial inputs only; no study file is read by these tests."""
import unittest,math
import numpy as np
from numerics import *
class Controls(unittest.TestCase):
    def test_nested(self):
        validate_masks(np.array([1,1,0],bool),np.array([0,1,0],bool),3)
        with self.assertRaises(ValueError):validate_masks(np.array([0],bool),np.array([1],bool),1)
    def test_mask_type(self):
        with self.assertRaises(ValueError):validate_masks(np.array([1]),np.array([1]),1)
    def test_mask_shape(self):
        with self.assertRaises(ValueError):validate_masks(np.array([1],bool),np.array([1],bool),2)
    def test_sigmoid(self):
        np.testing.assert_allclose(soft([0,.5,1]),[1/(1+math.exp(10)),.5,1/(1+math.exp(-10))],rtol=0,atol=2e-16)
    def test_transform_after_average(self):
        self.assertAlmostEqual(estimate([0,1])['p'],.5,places=15)
        self.assertAlmostEqual(estimate([0,1])['dg'],0,places=14)
        self.assertGreater(abs(estimate([0,.5])['p']-float(soft([.25])[0])),.1)
    def test_logit_sign(self):
        self.assertAlmostEqual(transform(.8)[0],-R*T*math.log(4),places=14)
        self.assertGreater(transform(.2)[0],0)
    def test_clipping(self):
        self.assertTrue(transform(0)[1]);self.assertTrue(transform(1)[1]);self.assertFalse(transform(.5)[1])
        self.assertTrue(math.isfinite(transform(1)[0]))
    def test_empty(self):self.assertIsNone(estimate([]))
    def test_nan_fnc(self):
        with self.assertRaises(ValueError):estimate([np.nan])
    def test_inf_fnc(self):
        with self.assertRaises(ValueError):estimate([np.inf])
    def test_fnc_range(self):
        with self.assertRaises(ValueError):estimate([1.01])
    def test_nonfinite_probability(self):
        for p in (math.nan,math.inf,-.1,1.1):
            with self.assertRaises(ValueError):transform(p)
    def test_pair_sign_baseline(self):
        self.assertEqual(pair(-1,-3,1),(2,1));self.assertEqual(pair(-3,-1,1),(-2,3))
    def test_mae(self):self.assertEqual(mean([pair(2,0,1)[1],pair(3,0,-2)[1]]),3)
    def test_nonfinite_pair_mean(self):
        with self.assertRaises(ValueError):pair(math.nan,0,0)
        with self.assertRaises(ValueError):mean([])
        with self.assertRaises(ValueError):mean([math.inf])
    def test_stage_difference(self):
        self.assertEqual((3-1)-(2-1),1)
        self.assertEqual((3-2)+(2-1),3-1)
    def test_duplicate(self):
        with self.assertRaises(ValueError):unique([{'id':'a'},{'id':'a'}],'id')
    def test_missing(self):
        with self.assertRaises(ValueError):unique([{'id':''}],'id')
        with self.assertRaises(ValueError):unique([{'id':'a'}],'id',2)
    def test_omega_boundary(self):
        a=np.array([[0,180,-180,30,-30,150,-150],[31,149,np.nan,0,0,0,0]])
        t,u,r,n=omega_masks(a,np.array([1,1],bool))
        self.assertFalse(r[0]);self.assertTrue(r[1]);self.assertTrue(u[1]);self.assertEqual(t.sum(),2)
    def test_unknown_retained(self):
        t,u,r,n=omega_masks(np.array([[np.nan,0]]),np.array([1],bool))
        self.assertTrue(u[0]);self.assertFalse(r[0])
    def test_threshold_boundary(self):
        self.assertTrue(classification(.1,4e-9)['ge_0p1']);self.assertTrue(classification(-.1,4e-9)['near_0p1'])
        self.assertFalse(classification(math.nextafter(.1,0),4e-9)['ge_0p1'])
        self.assertEqual(classification(0,4e-9)['sign'],0)
    def test_nonlinear_intervals(self):
        for p in [0,.00001,.5,.99999,1]:
            lo,hi=dg_interval(p,1e-10)
            for q in [max(0,p-1e-10),p,min(1,p+1e-10)]:self.assertTrue(lo<=transform(q)[0]<=hi)
        self.assertGreater(dg_interval(.99999,1e-10)[1]-dg_interval(.99999,1e-10)[0],1000*(dg_interval(.5,1e-10)[1]-dg_interval(.5,1e-10)[0]))
if __name__=='__main__':unittest.main(verbosity=2)
