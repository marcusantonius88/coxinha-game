from PIL import Image
from collections import Counter

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

salmon = Counter()
for y in range(0, H):
    for x in range(0, W):
        r, g, b, a = p[x, y]
        if a > 100 and r > 210 and 90 <= g <= 160 and b < 130 and (r - g) > 40:
            salmon[(r, g, b)] += 1
print('salmon-pink total:', sum(salmon.values()))
for c, n in salmon.most_common(10):
    print('  ', c, 'x%d' % n)
if salmon:
    tot = [0, 0, 0]; n = 0
    for c, k in salmon.items():
        for i in range(3): tot[i] += c[i] * k
        n += k
    print('avg salmon =', tuple(round(t / n) for t in tot))
    # bbox
    xs, ys = [], []
    for y in range(0, H):
        for x in range(0, W):
            r, g, b, a = p[x, y]
            if a > 100 and r > 210 and 90 <= g <= 160 and b < 130 and (r - g) > 40:
                xs.append(x); ys.append(y)
    print('salmon bbox full x=%d..%d y=%d..%d' % (min(xs), max(xs), min(ys), max(ys)))
    print('  -> reduced x~%d..%d y~%d..%d' % (min(xs)*48//W, max(xs)*48//W, 6+min(ys)*26//H, 6+max(ys)*26//H))
