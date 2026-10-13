from PIL import Image
from collections import Counter

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

# TRUE pink: bright, red~green >> blue  (orange has LOW green)
pink = Counter()
for y in range(0, H // 2):
    for x in range(0, W):
        r, g, b, a = p[x, y]
        if a > 110 and r > 200 and g > 150 and b < 200 and (r - b) > 40 and (g - b) > 40:
            pink[(r, g, b)] += 1
print('TRUE pink (bright, g high) count:', sum(pink.values()))
for c, n in pink.most_common(10):
    print('  ', c, 'x%d' % n)
if pink:
    tot = [0, 0, 0]; n = 0
    for c, k in pink.items():
        for i in range(3): tot[i] += c[i] * k
        n += k
    avg = tuple(round(t / n) for t in tot)
    print('avg pink =', avg)

# where is it? bounding box of true-pink
if pink:
    xs, ys = [], []
    for y in range(0, H // 2):
        for x in range(0, W):
            r, g, b, a = p[x, y]
            if a > 110 and r > 200 and g > 150 and b < 200 and (r - b) > 40 and (g - b) > 40:
                xs.append(x); ys.append(y)
    print('pink bbox x=%d..%d y=%d..%d' % (min(xs), max(xs), min(ys), max(ys)))
    # map to reduced coords (dog placed at (0,6), dog w=48 of full ~518, h=26 of full ~275)
    print('  -> reduced x~%d..%d y~%d..%d' % (min(xs)*48//W, max(xs)*48//W, 6+min(ys)*26//H, 6+max(ys)*26//H))
