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

def hsv(c):
    return colorsys.rgb_to_hsv(*[x/255 for x in c])

def band_rep(lo, hi):
    band = [(c, n) for c, n in allc.items() if lo <= hsv(c)[0]*360 < hi]
    band.sort(key=lambda t: -t[1])
    # weight-average the top cluster
    tot=[0,0,0]; n=0
    for c,k in band[:1]:
        for i in range(3): tot[i]+=c[i]*k
        n+=k
    return band[:3], (tuple(round(t/n) for t in tot) if n else None)

for name,(lo,hi) in [('PINK 345-360',(345,360)),('DARK 0-15',(0,15)),
                     ('DARK 340-360 & low val',(340,360)),
                     ('MUD 15-30',(15,30)),('ORANGE 30-45',(30,45))]:
    band, rep = band_rep(lo,hi)
    print(name, 'top:', band, 'rep=', rep)

# cream / near-neutral bright
cream = [(c,n) for c,n in allc.items() if hsv(c)[1]<0.35 and hsv(c)[2]>0.7]
cream.sort(key=lambda t:-t[1])
print('CREAM top:', cream[:4])
# outline pure dark
dark = [(c,n) for c,n in allc.items() if hsv(c)[2]<0.18]
dark.sort(key=lambda t:-t[1])
print('DARK-outline top:', dark[:4])
