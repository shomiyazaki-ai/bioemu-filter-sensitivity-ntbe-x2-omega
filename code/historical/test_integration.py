import io, pathlib, tempfile, unittest, zipfile
import numpy as np
import mdtraj as md
from ntbe_x2_primary import calc_system, dg, sha

class IntegrationTest(unittest.TestCase):
 def test_real_io_and_saved_fnc(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td);fnc=root/'fnc';fnc.mkdir();out=root/'output';out.mkdir()
   (out/'omega_masks').mkdir()
   t=md.Topology();ch=t.add_chain()
   # two regular Ala-Pro/Ala links. A regular bonded C-N is explicitly present.
   residues=[];atomby=[]
   for i,name in enumerate(['ALA','PRO','ALA']):
    r=t.add_residue(name,ch,resSeq=i+1);residues.append(r)
    ats={}
    for an,e in [('N',md.element.nitrogen),('CA',md.element.carbon),('C',md.element.carbon),('O',md.element.oxygen)]:ats[an]=t.add_atom(an,e,r)
    atomby.append(ats)
   for j in range(2):t.add_bond(atomby[j]['C'],atomby[j+1]['N'])
   xyz=np.zeros((3,t.n_atoms,3),dtype=np.float32)
   for frame in range(3):
    for i in range(3):
     x=0.3*i
     xyz[frame,4*i:4*i+4,:]=[[x,0,0],[x+.11,.09,0],[x+.2,.09,.1],[x+.2,.18,.1]]
   tr=md.Trajectory(xyz,t)
   pdb=root/'topology.pdb';xtc=root/'samples.xtc';tr[0].save_pdb(str(pdb));tr.save_xtc(str(xtc))
   with zipfile.ZipFile(root/'a.zip','w') as z:z.write(pdb,'test/s/topology.pdb');z.write(xtc,'test/s/samples.xtc')
   q=np.array([.2,.5,.8],dtype=np.float32);mask=np.ones(3,dtype=bool)
   np.savez_compressed(fnc/'s.npz',pass_all=mask,fnc=q)
   d0,p0=dg(q)
   rec={'name':'s','name_wt':'s','is_mutant':'False','n_A':'3','n_B':'3','dg_B':str(d0),'p_fold_raw_B':str(p0),
        'num_samples_target':'3','sha256_xtc':sha(xtc.read_bytes()),'sha256_pdb':sha(pdb.read_bytes())}
   with zipfile.ZipFile(root/'a.zip') as z:
    result=calc_system('s',rec,{'s':{'sequence':'APA'}},z,fnc,out,True)
   self.assertEqual(result['status'],'BOMEGA_EMPTY')
   self.assertEqual(result['n_B0'],3)
   self.assertEqual(result['n_omega_unknown'],0)
   self.assertIsNone(result['dg_Bomega'])
   self.assertEqual(result['n_pro_bonds'],1)
if __name__=='__main__':unittest.main()
