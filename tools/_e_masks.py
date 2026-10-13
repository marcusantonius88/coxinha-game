from PIL import Image
import colorsys

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

def hue(c):
    return colorsys.rgb_to_hsv(*[v/255 for v in c])[0]*360

# Mask A: PINK ear interior = hue 330-360, moderate val, decent sat
A = Image.new('RGBA', (W, H), (0,0,0,0)); pa = A.load()
# Mask B: DARK muzzle/black areas = val < 0.35
B = Image.new('RGBA', (W, H), (0,0,0,0)); pb = B.load()
for y in range(H):
    for x in range(W):
        r,g,b,a = p[x,y]
        if a < 150: continue
        h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
        hu=h*360
        if 325 <= hu <= 360 and v>0.35 and s>0.15:
            pa[x,y]=(255,80,120,255)
        if v < 0.38:
            pb[x,y]=(255,255,255,255)

for name, M in [('pink',A),('dark',B)]:
    bg = Image.new('RGBA',(W,H),(20,20,30,255)); bg.alpha_composite(M)
    vw=320; vh=round(H*vw/W)
    bg.convert('RGB').resize((vw,vh),Image.NEAREST).save('/tmp/ev/mask_%s.png'%name)
print('masks saved; pink bbox=',A.getbbox(),'dark bbox=',B.getbbox())
