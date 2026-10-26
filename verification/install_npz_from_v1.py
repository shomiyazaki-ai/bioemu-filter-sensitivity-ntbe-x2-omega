"""Install the exact saved NPZ from the existing published v1 archive, never regenerate it."""
from pathlib import Path
import argparse,hashlib,zipfile
ARCHIVE='91753d9a9fb2494e2619a03d9f9f1db38ac5e999f1a9661a8e592467e35c4c31'
NPZ='569a09744787d2c6c9b35e9e0cc80ce2ef4dd40d6a3f494cd45fe33bed8584b7'
def main():
 p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args()
 if hashlib.sha256(a.archive.read_bytes()).hexdigest()!=ARCHIVE:raise SystemExit('FAIL: v1 archive hash')
 with zipfile.ZipFile(a.archive) as z:
  if z.namelist().count('data/all_npz.zip')!=1:raise SystemExit('FAIL: missing/duplicate member')
  b=z.read('data/all_npz.zip')
 if hashlib.sha256(b).hexdigest()!=NPZ:raise SystemExit('FAIL: NPZ member hash')
 dst=a.root/'data/inputs/all_npz.zip'
 if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest()!=NPZ:raise SystemExit('FAIL: refusing to overwrite different file')
 dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():dst.write_bytes(b)
 print('PASS: exact published NPZ available at',dst)
if __name__=='__main__':main()
