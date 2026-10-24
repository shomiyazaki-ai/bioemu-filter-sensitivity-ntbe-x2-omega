"""Pro/non-Pro omega QA including exact boundary and real MDTraj PRO topology."""
import unittest
import numpy as np
import mdtraj as md
from ntbe_x2_omega_pilot import backbone_atoms, four_point_degrees, classify_omega, wrap

class ProlineTests(unittest.TestCase):
    def test_proline_classification(self):
        # Two peptide bonds: ALA->PRO (True), PRO->ALA (False)
        angles=np.array([[0.,0.],[180.,180.],[90.,90.],
                         [30.,-30.],[150.,-150.],[31.,149.],
                         [np.nan,np.nan]])
        c=classify_omega(angles,np.array([True,False]))
        for k,expected in {'cis':[0,3],'trans':[1,4],'twisted':[2,5],'unknown':[6]}.items():
            mask=c[k]
            self.assertEqual(np.flatnonzero(mask[:,0]).tolist(),expected)
            self.assertEqual(np.flatnonzero(mask[:,1]).tolist(),expected)
        self.assertFalse(c['twisted'][0,0]) # cis-Pro retained
        self.assertFalse(c['twisted'][1,0]) # trans-Pro retained
        self.assertTrue(c['twisted'][2,0]) # distorted Pro eliminated
        self.assertFalse(c['twisted'][3,0]) # exact 30 degrees retained
        self.assertFalse(c['twisted'][4,0]) # exact 30 degrees from trans retained

    def test_real_proline_topology_and_dihedral(self):
        top=md.Topology();ch=top.add_chain()
        for name in ['ALA','PRO','ALA']:
            res=top.add_residue(name,ch)
            for atom,elem in [('N',md.element.nitrogen),('CA',md.element.carbon),('C',md.element.carbon),('O',md.element.oxygen)]:
                top.add_atom(atom,elem,res)
        bonds,issues,is_pro=backbone_atoms(top)
        self.assertEqual(issues,[])
        np.testing.assert_array_equal(is_pro,[True,False])
        self.assertEqual(bonds,[[1,2,4,5],[5,6,8,9]])
        xyz=np.zeros((1,top.n_atoms,3))
        for i in range(3):
            xyz[0,4*i:4*i+4]=[[i*3.,0.,0.],[i*3.+1.,1.,0.],[i*3.+2.,1.,1.],[i*3.+2.,2.,1.]]
        traj=md.Trajectory(xyz.astype('float32')/10,top)
        indices,radians=md.compute_omega(traj)
        self.assertEqual(set(map(tuple,indices)),set(map(tuple,bonds)))
        independent=four_point_degrees(traj.xyz[:,np.array(bonds),:].astype(float)*10)
        ref=np.column_stack([np.degrees(radians[:,next(j for j,v in enumerate(indices) if list(v)==a)]) for a in bonds])
        self.assertLess(float(np.max(abs(wrap(independent-ref)))),.02)

    def test_missing_pro_atom_unknown_not_normal(self):
        top=md.Topology();ch=top.add_chain()
        for name in ['ALA','PRO']:
            r=top.add_residue(name,ch)
            for atom in (['N','CA','C'] if name=='ALA' else ['N','C']):
                top.add_atom(atom,md.element.nitrogen if atom=='N' else md.element.carbon,r)
        bonds,issues,pro=backbone_atoms(top)
        self.assertEqual(bonds,[None]);self.assertTrue(issues)
        self.assertTrue(pro[0])
        c=classify_omega(np.array([[float('nan')]]),pro)
        self.assertTrue(c['unknown'][0,0]);self.assertFalse(c['cis'][0,0]);self.assertFalse(c['twisted'][0,0])

if __name__=='__main__':unittest.main()
