from PIL import Image
from collections import Counter
import os

PAL = [
    (0,0,0),(27,17,16),(54,34,30),(228,151,63),(200,124,44),(244,181,96),
    (237,113,90),(210,92,72),(244,230,195),(222,203,165),(255,255,255),(60,60,66),
]

def nearest(c):
    r,g,b=c; best,bi=1e18,0
    for i,(pr,pg,pb) in enumerate(PAL):
        d=(r-pr)**2+(g-pg)**2+(b-pb)**2
        if d<best: best,bi=d,i
    return bi

def quantize(im):
    im=im.convert('RGBA'); w,h=im.size; p=im.load()
    out=Image.new('RGBA',(w,h)); op=out.load()
    for y in range(h):
        for x in range(w):
            r,g,b,a=p[x,y]
            op[x,y]=(0,0,0,0) if a<128 else PAL[nearest((r,g,b))]+(255,)
    return out

def downscale_mode(im,tw,th):
    w,h=im.size; p=im.load()
    out=Image.new('RGBA',(tw,th)); op=out.load()
    for ty in range(th):
        sy0=ty*h//th; sy1=max(sy0+1,(ty+1)*h//th)
        for tx in range(tw):
            sx0=tx*w//tw; sx1=max(sx0+1,(tx+1)*w//tw)
            cnt=Counter(); acov=0; atot=0
            for sy in range(sy0,sy1):
                for sx in range(sx0,sx1):
                    r,g,b,a=p[sx,sy]; atot+=1
                    if a>=128: acov+=1; cnt[(r,g,b)]+=1
            if acov*2<atot: op[tx,ty]=(0,0,0,0)
            elif cnt: op[tx,ty]=cnt.most_common(1)[0][0]+(255,)
            else: op[tx,ty]=(0,0,0,0)
    return out

CW,CH=48,32
CONTENT_W=46

def build_frame(dog):
    q=quantize(dog)
    th=round(dog.size[1]*CONTENT_W/dog.size[0])
    small=downscale_mode(q,CONTENT_W,th)
    # place centered-x, bottom-aligned (feet at y=CH-1)
    canvas=Image.new('RGBA',(CW,CH),(0,0,0,0))
    ox=(CW-CONTENT_W)//2
    oy=CH-th
    canvas.alpha_composite(small,(ox,oy))
    return canvas, small

OUT='assets/coxinha/idle-revision-e'
os.makedirs(OUT,exist_ok=True)

frames=[]
smalls=[]
for i in range(4):
    dog=Image.open('/tmp/ev/dog_%d.png'%i).convert('RGBA')
    fr,sm=build_frame(dog)
    fr.save(os.path.join(OUT,'idle_%02d.png'%i))
    frames.append(fr); smalls.append(sm)
    print('frame %d placed content %s at oy=%d'%(i,sm.size,CH-sm.size[1]))

# ---- diffs between consecutive frames (breathing/blink magnitude) ----
def alpha(im):
    a=im.split()[3]; return a.tobytes()
for i in range(4):
    j=(i+1)%4
    A=smalls[i].getbbox(); B=smalls[j].getbbox()
    # count differing opaque px (pad to same size by top-left align on feet)
    ai=frames[i].convert('RGBA'); aj=frames[j].convert('RGBA')
    pa=ai.load(); pj=aj.load(); diff=0; total=0
    for y in range(CH):
        for x in range(CW):
            if pa[x,y][3]>0 or pj[x,y][3]>0:
                total+=1
                if pa[x,y][:3]!=pj[x,y][:3] or (pa[x,y][3]>0)!=(pj[x,y][3]>0):
                    diff+=1
    print('diff f%d->f%d: %d/%d opaque px differ'%(i,j,diff,total))

# ---- palette used across all frames ----
allc=Counter()
for fr in frames:
    p=fr.load()
    for y in range(CH):
        for x in range(CW):
            r,g,b,a=p[x,y]
            if a>0: allc[(r,g,b)]+=1
print('TOTAL palette colors used:',len(allc))
for c,n in allc.most_common():
    print('   ',c,'x%d'%n)
