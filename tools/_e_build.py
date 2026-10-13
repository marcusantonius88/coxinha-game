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

if __name__=='__main__':
    base=Image.open('/tmp/ev/dog_1.png').convert('RGBA')
    q=quantize(base); q.save('/tmp/ev/base_q.png')
    tw=46; th=round(base.size[1]*tw/base.size[0])
    small=downscale_mode(q,tw,th)
    print('small size',small.size)
    small.save('/tmp/ev/base_small.png')
    view=small.resize((tw*10,th*10),Image.NEAREST)
    bgv=Image.new('RGBA',view.size,(30,32,48,255)); bgv.alpha_composite(view)
    bgv.convert('RGB').save('/tmp/ev/base_small_big.png')
    print('done')
