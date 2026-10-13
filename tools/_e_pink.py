from PIL import Image
from collections import Counter

# high-res pose0 dog (has true pink before any quantization)
d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

# ears: the tall structures at top. In full-res the dog spans ~518x275.
# Ear interiors sit near the top. Scan the whole top third for pink.
pink = Counter()
for y in range(0, H // 3):
    for x in range(0, W):
        r, g, b, a = p[x, y]
        if a > 110 and r > g + 25 and r > b + 25 and r > 150:
            pink[(r, g, b)] += 1
print('pink pixels in top third:', sum(pink.values()))
for c, n in pink.most_common(8):
    print('  ', c, 'x%d' % n)

# average pink
if pink:
    tot = [0, 0, 0]
    n = 0
    for c, k in pink.items():
        for i in range(3):
            tot[i] += c[i] * k
        n += k
    print('avg pink =', tuple(round(t / n) for t in tot))

# Also find cream chest (low-sat high-lum) and confirm counts
cream = Counter()
for y in range(H // 2, H):
    for x in range(0, W):
        r, g, b, a = p[x, y]
        if a > 110 and r > 200 and g > 170 and b < 190 and r > b + 20:
            cream[(r, g, b)] += 1
print('cream-ish pixels lower half:', sum(cream.values()))
for c, n in cream.most_common(4):
    print('  cream', c, 'x%d' % n)
