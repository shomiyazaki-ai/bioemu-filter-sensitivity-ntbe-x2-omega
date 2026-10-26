"""P3 package/document QC, separate from arithmetic reconstruction.
Requires NumPy and PyMuPDF; reads all retained verification comparisons and final PDFs.
This is structured same-Work self-review, not an independent external audit.
"""
from pathlib import Path
import argparse,csv,json,re,hashlib,sys
import fitz

def main(root,out):
    checks=[]
    def check(name,ok,detail=None):checks.append(dict(check=name,pass_=bool(ok),detail=detail))
    j=json.loads((root/'data/results/verification.json').read_text());s=json.loads((root/'data/results/summary.json').read_text())
    check('V0-V2 complete PASS',j['status']=='PASS' and not j['failures'] and j['coverage']==dict(p=462,dg=462,ddg=336,ae=336))
    cs=list(csv.DictReader((root/'data/results/comparison_details.csv').open()))
    check('every stored comparison passes',len(cs)==sum(x['n'] for x in j['maxima'].values()) and all(x['pass_']=='True' and float(x['abs_error'])<=float(x['tolerance']) for x in cs),len(cs))
    for file,n,key in [('systems_recomputed.csv',154,'system'),('pairs_recomputed.csv',112,'mutant')]:
        r=list(csv.DictReader((root/'data/results'/file).open()));check(file+' exact unique coverage',len(r)==len({x[key] for x in r})==n)
    for file,n in [('nonlinear_intervals.csv',462),('classification_diagnostics.csv',336),('npz_member_manifest.csv',154)]:check(file+' row count',len(list(csv.DictReader((root/'data/results'/file).open())))==n)
    check('nonlinear intervals independently pass',j['nonlinear_interval_all_contained'])
    docs={k:(root/path).read_text() for k,path in [('note','manuscript/Technical_Note_v1.1.0_rc1.md'),('si','supplement/Supplementary_Information_v1.1.0_rc1.md')]}
    for key,text in docs.items():
        check(key+' all three MAE display values',all(f'{s["mae"][v]:.6f}' in text for v in ['A','B0','Bomega']))
        check(key+' all three MAE changes',all(f'{v:+.6f}' in text for v in s['delta_mae'].values()))
        check(key+' paired baseline wording','matched baseline' in text and '112' in text)
        check(key+' 0.1 descriptive, primary separate',('arbitrary' in text or 'descriptive' in text) and '0.1' in text and 'secondary' in text.lower())
        check(key+' source-coordinate limitation',('not download' in text or 'not downloaded' in text or 'without downloading' in text) and 'L2' in text and 'fingerprint' in text)
        check(key+' no replacement DOI claim','no new' in text.lower() or 'No new' in text)
    # Every stage-summary displayed in Note/SI is matched to the result object.
    for edge,row in s['stage_summaries'].items():
        for key in ['p','dg','ddg']:
            targets=[f'{row[key][v]:+.6f}' if key=='p' or v=='median' else f'{row[key][v]:+.6f}' for v in ['min','median','max']]
            text=docs['si'] if key=='p' else docs['note']
            # Minus entries retain '-', positive min/max/medians may carry explicit '+' or omit it.
            for target in targets:check(edge+': '+key+' display '+target,target in text or target.lstrip('+') in text)
    images=[];bounds=[]
    for md in [root/'manuscript/Technical_Note_v1.1.0_rc1.md',root/'supplement/Supplementary_Information_v1.1.0_rc1.md']:
        pdf=md.with_suffix('.pdf');d=fitz.open(pdf);alltext=''.join(p.get_text() for p in d)
        check(pdf.name+' pages nonempty',all(len(p.get_text())>300 for p in d),len(d))
        check(pdf.name+' text glyphs','\ufffd' not in alltext and '\u25a0' not in alltext)
        for page in d:
            for b in page.get_text('blocks'):
                if len(b)>6 and b[6]==0:
                    if b[0]<40 or b[1]<30 or b[2]>page.rect.width-35 or b[3]>page.rect.height-15:bounds.append(dict(file=pdf.name,page=page.number+1,bbox=b[:4]))
            for l in page.get_links():
                uri=l.get('uri','');check(pdf.name+' link punctuation '+uri,not uri.endswith(('.',',',';')))
        images.append(dict(file=pdf.name,pages=len(d),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest()))
    check('PDF text within page margins',not bounds,bounds)
    missing=[]
    text=(root/'README.md').read_text()
    for dest in re.findall(r'\]\(([^)]+)\)',text):
        if dest.startswith(('http:','https:','#')):continue
        if not (root/dest).exists():missing.append(dest)
    check('README local links resolve',not missing,missing)
    v=json.loads((root/'VERSION.json').read_text());check('no fabricated candidate public identity',all(v[x] is None for x in ['candidate_public_commit','candidate_public_tag','candidate_doi']) and not v['publication_operations_performed'])
    r=dict(status='PASS' if all(x['pass_'] for x in checks) else 'FAIL',scope='P3 same-Work structured self-review; visual review reported separately',checks=checks,failures=[x for x in checks if not x['pass_']],pdfs=images)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status=r['status'],checks=len(checks),failures=r['failures']),indent=2));return 0 if r['status']=='PASS' else 2
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sys.exit(main(a.root,a.out))
