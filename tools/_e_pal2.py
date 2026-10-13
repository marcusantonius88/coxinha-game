from PIL import Image
from collections import Counter
import colorsys

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

def hsv(c):
    return colorsys.rgb_to_hsv(*[v/255 for v in c])

pink = Counter(); cream = Counter(); dark = Counter()
for y in range(H):
    for x in range(W):
        r, g, b, a = p[x, y]
        if a < 150: continue
        h, s, v = hsv((r, g, b)); hd = h*360
        if 0 <= hd < 22 and 0.35 <= s <= 0.80 and 0.70 <= v <= 1.0:
            pink[(r, g, b)] += 1
        if s <= 0.35 and v >= 0.80:
            cream[(r, g, b)] += 1
        if v <= 0.35:
            dark[(r, g, b)] += 1

def avg(cnt):
    if not cnt: return None
    t=[0,0,0]; n=0
    for c,k in cnt.items():
        for i in range(3): t[i]+=c[i]*k
        n+=k
    return tuple(round(z/n) for z in t)

print('PINK ear  n=%d avg=%s' % (sum(pink.values()), avg(pink)))
print('  pink modes:', pink.most_common(3))
print('CREAM      n=%d avg=%s' % (sum(cream.values()), avg(cream)))
print('  cream modes:', cream.most_common(3))
print('DARK/muzzle n=%d avg=%s' % (sum(dark.values()), avg(dark)))
print('  dark modes:', dark.most_common(3))
