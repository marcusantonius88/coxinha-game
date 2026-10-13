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

def hue(c):
    r, g, b = [v/255 for v in c]
    return colorsys.rgb_to_hsv(r, g, b)[0] * 360

# bucket by hue into 15-deg bins, count
buckets = Counter()
for c, n in allc.items():
    buckets[int(hue(c)//15)*15] += n
print('hue buckets (deg: count):')
for b in sorted(buckets):
    print('  %3d-%3d: %d' % (b, b+15, buckets[b]))

print('top 20 colors overall:')
for c, n in allc.most_common(20):
    h, s, v = colorsys.rgb_to_hsv(*[x/255 for x in c])
    print('  %s n=%-5d hue=%3.0f sat=%.2f val=%.2f' % (str(c), n, h*360, s, v))
