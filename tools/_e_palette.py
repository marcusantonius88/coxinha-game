from PIL import Image
from collections import Counter
import colorsys

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()
allc = Counter()
for y in range(H):
    for x in range(W):
        r, g, b, a = p[x, y]
        if a < 150: continue
        allc[(r, g, b)] += 1

def hsv(c): return colorsys.rgb_to_hsv(*[x/255 for x in c])

brown = [(c,n) for c,n in allc.items()
         if 0.02 < hsv(c)[0] < 0.06 and 0.25 < hsv(c)[2] < 0.65 and hsv(c)[1] > 0.3]
brown.sort(key=lambda t:-t[1])
print('MUZZLE brown top:', brown[:5])

sh = [(c,n) for c,n in allc.items()
      if 0.07 < hsv(c)[0] < 0.11 and 0.55 < hsv(c)[2] < 0.8 and hsv(c)[1] > 0.5]
sh.sort(key=lambda t:-t[1])
print('SHADE orange top:', sh[:5])

pink = [(c,n) for c,n in allc.items()
        if hsv(c)[2] > 0.8 and 0.30 < hsv(c)[1] < 0.62 and 80 < c[2] < 135 and c[0] > 210]
pink.sort(key=lambda t:-t[1])
print('PINK ear top:', pink[:5])

hi = [(c,n) for c,n in allc.items() if 0.08 < hsv(c)[0] < 0.10 and hsv(c)[2] > 0.82 and hsv(c)[1] > 0.5]
hi.sort(key=lambda t:-t[1])
print('FUR HIGHLIGHT top:', hi[:3])

from PIL import Image
from collections import Counter

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

salmon = Counter(); cream = Counter(); dark = Counter(); orange = Counter()
sx=[]; sy=[]
for y in range(H):
    for x in range(W):
        r, g, b, a = p[x, y]
        if a < 120: continue
        lum = 0.3*r+0.6*g+0.1*b
        if r>=200 and 100<g<180 and b<g and (r-g)>=40 and (g-b)>=15:
            salmon[(r,g,b)]+=1; sx.append(x); sy.append(y)
        elif lum>200 and (max(r,g,b)-min(r,g,b))<55:
            cream[(r,g,b)]+=1
        elif lum<90 and r>b:
            dark[(r,g,b)]+=1
        elif r>190 and g>110 and g<170 and b<110 and (r-g)<50:
            orange[(r,g,b)]+=1

def show(name, c):
    tot=[0,0,0]; n=0
    for cc,k in c.items():
        for i in range(3): tot[i]+=cc[i]*k
        n+=k
    avg = tuple(round(t/n) for t in tot) if n else None
    print('%s n=%d avg=%s top=%s' % (name, n, avg, c.most_common(4)))

show('SALMON(ear-interior)', salmon)
if sx: print('   bbox x=%d..%d y=%d..%d  ->reduced x%d..%d y%d..%d' %
            (min(sx),max(sx),min(sy),max(sy), min(sx)*48//W,max(sx)*48//W, 6+min(sy)*26//H,6+max(sy)*26//H))
show('CREAM', cream)
show('DARK-muzzle', dark)
show('ORANGE-fur', orange)
