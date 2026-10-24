import unittest
import numpy as np
import mdtraj as md
from ntbe_x2_omega_pilot import four_point_degrees,deviation,wrap,backbone_atoms,dg

class OmegaTests(unittest.TestCase):
 def test_angles_and_strict_threshold(self):
  # 4 atoms with the central bond along the x axis
  def pts(a):
   rad=np.deg2rad(a)
   return [[0.,1.,0.],[0.,0.,0.],[1.,0.,0.],[1.,np.cos(rad),np.sin(rad)]]
  a=np.array([[pts(0),pts(180),pts(31),pts(-31),pts(29),pts(150),pts(149),pts(30)]],float)
  ang=four_point_degrees(a)
  self.assertTrue(np.allclose(deviation(ang)[0],[0,0,31,31,29,30,31,30],atol=1e-9))
  self.assertEqual((deviation(ang)>30).tolist(),[[False,False,True,True,False,False,True,False]])
  self.assertAlmostEqual(float(deviation(np.array([180.,-180.,360.,0.]))[0]),0.)
 def test_nonfinite_unknown(self):
  x=np.array([[[[0.,1.,0.],[0.,0.,0.],[1.,0.,0.],[1.,1.,0.]]]],float)
  x[0,0,0,0]=np.nan
  self.assertTrue(np.isnan(four_point_degrees(x)[0,0]))
 def test_topology_mapping_and_mdtraj(self):
  top=md.Topology(); ch=top.add_chain()
  for i in range(3):
   r=top.add_residue('ALA',ch,resSeq=i+1)
   for name in ['N','CA','C','O']:
    top.add_atom(name, {'N':md.element.nitrogen,'CA':md.element.carbon,'C':md.element.carbon,'O':md.element.oxygen}[name],r)
  bonds,errors,pro=backbone_atoms(top)
  self.assertEqual(len(bonds),2);self.assertEqual(errors,[])
  xyz=np.zeros((1,top.n_atoms,3),float)
  # Noncollinear, arbitrary 3D positions for torsions
  for i in range(3):
   xyz[0,4*i+0]=[i*3+0,0,0]
   xyz[0,4*i+1]=[i*3+1,1,0]
   xyz[0,4*i+2]=[i*3+2,1,1]
   xyz[0,4*i+3]=[i*3+2,2,1]
  traj=md.Trajectory(xyz/10,top)
  inds,rads=md.compute_omega(traj)
  self.assertEqual(set(map(tuple,bonds)),set(map(tuple,inds.tolist())))
  ind=four_point_degrees((traj.xyz[:,np.array(bonds),:].astype(float))*10)
  lib=np.array([np.rad2deg(rads[:,next(j for j,b in enumerate(inds) if list(b)==a)]) for a in bonds]).T
  self.assertLess(np.max(abs(wrap(ind-lib))),0.02)
 def test_dg(self):
  dgval,p=dg(np.array([.5,.5]));self.assertAlmostEqual(p,.5);self.assertAlmostEqual(dgval,0.,places=10)

if __name__=='__main__':unittest.main()
