"""Local packaging only. No GitHub/Zenodo API, upload, push or release action.
Builds two distributions and an external audit to avoid circular archive hashes.
"""
from pathlib import Path
import csv,hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent
EXCLUDED={'FILE_MANIFEST.csv','SHA256SUMS.txt'}
def digest(b):return hashlib.sha256(b).hexdigest()
def manifest(root,kind):
    (root/'DISTRIBUTION.json').write_text(json.dumps(dict(candidate_version='1.1.0-rc1',kind=kind,npz_included=kind=='complete_zenodo_candidate',status='UNPUBLISHED',manifest_rules='FILE_MANIFEST.csv excludes itself and SHA256SUMS.txt; SHA256SUMS includes the CSV manifest and every other file except itself; archive hashes supplied externally.'),indent=2)+'\n')
    files=[p for p in sorted(root.rglob('*')) if p.is_file() and p.relative_to(root).as_posix() not in EXCLUDED]
    rows=[dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size,sha256=digest(p.read_bytes())) for p in files]
    with (root/'FILE_MANIFEST.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(rows)
    files.append(root/'FILE_MANIFEST.csv')
    (root/'SHA256SUMS.txt').write_text(''.join(f'{digest(p.read_bytes())}  {p.relative_to(root).as_posix()}\n' for p in sorted(files)))

def pack(root,dst):
    with zipfile.ZipFile(dst,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                rel=p.relative_to(root).as_posix();info=zipfile.ZipInfo(ROOT.name+'/'+rel,date_time=(2026,10,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())

def audit_zip(path):
    problems=[]
    with zipfile.ZipFile(path) as z:
        names=z.namelist();prefix=ROOT.name+'/'
        if len(names)!=len(set(names)):problems.append('duplicate ZIP member')
        sums=z.read(prefix+'SHA256SUMS.txt').decode().splitlines()
        expected={}
        for ln in sums:
            h,rel=ln.split('  ',1);expected[prefix+rel]=h
        if set(names)!=(set(expected)|{prefix+'SHA256SUMS.txt'}):problems.append('checksum coverage mismatch')
        for name,h in expected.items():
            if digest(z.read(name))!=h:problems.append('SHA mismatch: '+name)
        inventory=list(csv.DictReader(z.read(prefix+'FILE_MANIFEST.csv').decode().splitlines()))
        inv={prefix+x['path']:x for x in inventory}
        if set(inv)!=(set(names)-{prefix+'FILE_MANIFEST.csv',prefix+'SHA256SUMS.txt'}):problems.append('inventory coverage mismatch')
        for name,r in inv.items():
            b=z.read(name)
            if len(b)!=int(r['bytes']) or digest(b)!=r['sha256']:problems.append('inventory mismatch: '+name)
    return dict(file=path.name,bytes=path.stat().st_size,sha256=digest(path.read_bytes()),member_count=len(names),hash_checked_count=len(expected),inventory_count=len(inventory),status='PASS' if not problems else 'FAIL',failures=problems)

def main():
    for p in ROOT.rglob('__pycache__'):shutil.rmtree(p)
    manifest(ROOT,'complete_zenodo_candidate')
    stage=OUT/'github_staging'
    if stage.exists():shutil.rmtree(stage)
    shutil.copytree(ROOT,stage,ignore=shutil.ignore_patterns('all_npz.zip','__pycache__'))
    manifest(stage,'github_staging_without_large_npz')
    zfull=OUT/'NTBE_X2_omega_v1.1.0_rc1_Zenodo_candidate.zip';zgit=OUT/'NTBE_X2_omega_v1.1.0_rc1_GitHub_staging.zip'
    pack(ROOT,zfull);pack(stage,zgit)
    results=[audit_zip(zfull),audit_zip(zgit)]
    with zipfile.ZipFile(zfull) as a,zipfile.ZipFile(zgit) as b:
        aset=set(a.namelist());bset=set(b.namelist());onlyfull=sorted(aset-bset);onlygit=sorted(bset-aset)
        changed=[x for x in sorted(aset&bset) if a.read(x)!=b.read(x)]
    check=dict(only_complete=onlyfull,only_github=onlygit,changed_shared=changed)
    prefix=ROOT.name+'/'
    expected_changed={prefix+x for x in ['DISTRIBUTION.json','FILE_MANIFEST.csv','SHA256SUMS.txt']}
    cross=onlyfull==[prefix+'data/inputs/all_npz.zip'] and not onlygit and set(changed)==expected_changed
    audit=dict(candidate_version='1.1.0-rc1',status='PASS' if all(x['status']=='PASS' for x in results) and cross else 'FAIL',archives=results,cross_distribution=dict(pass_=cross,**check),scope='All ZIP members and inventories hashed; all shared scientific payloads identical. Exact NPZ extraction and lightweight verification tested separately.',independence='Same Work self-review; not independent human/model audit',publication_operations_performed=False)
    (OUT/'NTBE_P2P3_Delivery_QC.json').write_text(json.dumps(audit,indent=2)+'\n')
    (OUT/'NTBE_P2P3_DELIVERY_SHA256SUMS.txt').write_text(''.join(f'{digest(p.read_bytes())}  {p.name}\n' for p in [zfull,zgit,OUT/'NTBE_P2P3_Delivery_QC.json']))
    print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
