from PIL import Image
from collections import Counter

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
    w,h=im.size; p=im.load(); out=Image.new('RGBA',(tw,th)); op=out.load()
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

dog=Image.open('/tmp/ev/dog_3.png').convert('RGBA')
q=quantize(dog); tw=46; th=round(dog.size[1]*tw/dog.size[0])
sm=downscale_mode(q,tw,th)
p=sm.load(); w,h=sm.size
idx={c:i for i,c in enumerate(PAL)}; chars='0123456789ab'
print('size',sm.size)
print('     '+''.join(str(x%10) for x in range(w)))
for y in range(h):
    row=''
    for x in range(w):
        r,g,b,a=p[x,y]
        row+= ('.' if a==0 else chars[idx.get((r,g,b),0)])
    print('%2d   %s'%(y,row))
print('legend: 0=blk 1=dark 2=dkmid 3=orange 4=oshadow 5=ohigh 6=pink 7=pshadow 8=cream 9=cshadow a=white b=eyegray')
