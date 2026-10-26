"""Independent arithmetic, no historical or official analysis imports. Version 1.0.0."""
import csv, math
import numpy as np
R = 0.001987203599772605
T = 295.0

def unique(rows, key, count=None):
    ans={}
    for row in rows:
        name=row[key]
        if not name or name in ans: raise ValueError('missing/duplicate ID: '+name)
        ans[name]=row
    if count is not None and len(ans)!=count: raise ValueError('wrong row count')
    return ans

def read_csv(path):
    with open(path,encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def soft(q):
    q=np.asarray(q,dtype=np.float64)
    if q.ndim!=1 or not np.isfinite(q).all() or np.any((q<0)|(q>1)):raise ValueError('invalid FNC')
    return 1.0/(1.0+np.exp(10.0-20.0*q))

def transform(p):
    if not math.isfinite(p) or not 0<=p<=1: raise ValueError('invalid probability')
    pc=min(max(p,1e-10),1-1e-10)
    odds=pc/(1-pc); oc=min(max(odds,1e-10),1e10)
    return -R*T*math.log(oc), pc!=p or oc!=odds

def estimate(q):
    s=soft(q)
    if len(s)==0:return None
    p=math.fsum(map(float,s))/len(s)
    dg,clipped=transform(p)
    return dict(p=p,dg=dg,clipped=clipped,n=len(s))

def validate_masks(b0,bw,n):
    for a in (b0,bw):
        if a.dtype!=np.bool_ or a.shape!=(n,):raise ValueError('nonboolean/wrong shape mask')
    if np.any(bw & ~b0):raise ValueError('mask not nested')

def omega_deviation(a):
    # Distance to multiples of 180 degrees, using modulo without the historical wrap helper.
    a=np.asarray(a,dtype=np.float64)
    return np.abs((a+90.0)%180.0-90.0)

def omega_masks(angles,b0):
    angles=np.asarray(angles,dtype=np.float64)
    if angles.ndim!=2 or angles.shape[0]!=len(b0):raise ValueError('omega shape')
    known=np.isfinite(angles)
    with np.errstate(invalid='ignore'):d=omega_deviation(angles)
    twisted=known & (d>30.0)
    unknown=b0 & np.any(~known,axis=1)
    reject=b0 & np.any(twisted,axis=1)
    near=known & (np.abs(d-30.0)<=0.02)
    return twisted,unknown,reject,near

def pair(mutant,baseline,reference):
    vals=[mutant,baseline,reference]
    if not all(math.isfinite(x) for x in vals):raise ValueError('nonfinite pair')
    ddg=mutant-baseline
    return ddg,abs(ddg-reference)

def mean(x):
    if not x or not all(math.isfinite(v) for v in x):raise ValueError('invalid mean')
    return math.fsum(x)/len(x)

def classification(delta,tolerance):
    if not math.isfinite(delta):raise ValueError('nonfinite classification')
    return dict(sign=-1 if delta<0 else 1 if delta>0 else 0,ge_0p1=abs(delta)>=0.1,
                near_zero=abs(delta)<=tolerance,near_0p1=abs(abs(delta)-0.1)<=tolerance)

def dg_interval(p,eps):
    lo=max(0.0,p-eps);hi=min(1.0,p+eps)
    # The transform is decreasing, including flat clipping intervals.
    a=transform(hi)[0];b=transform(lo)[0]
    pad=16*max(math.ulp(a),math.ulp(b))
    return math.nextafter(a-pad,-math.inf),math.nextafter(b+pad,math.inf)
