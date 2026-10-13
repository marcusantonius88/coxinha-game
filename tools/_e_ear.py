from PIL import Image
from collections import Counter

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

# ear pink family: r high, g moderate(95-140), b moderate(70-120), big r-g gap but b NOT tiny
ear = Counter()
for y in range(0, H):
    for x in range(0, W):
        r, g, b, a = p[x, y]
        if a > 100 and r > 205 and 92 <= g <= 140 and 68 <= b <= 125 and (r - g) > 85:
            ear[(r, g, b)] += 1
print('ear-pink total:', sum(ear.values()))
for c, n in ear.most_common(6):
    print('  ', c, 'x%d' % n)
if ear:
    tot = [0, 0, 0]; n = 0
    for c, k in ear.items():
        for i in range(3): tot[i] += c[i] * k
        n += k
    print('avg ear-pink =', tuple(round(t / n) for t in tot))
    xs, ys = [], []
    for y in range(0, H):
        for x in range(0, W):
            r, g, b, a = p[x, y]
            if a > 100 and r > 205 and 92 <= g <= 140 and 68 <= b <= 125 and (r - g) > 85:
                xs.append(x); ys.append(y)
    print('ear bbox full x=%d..%d y=%d..%d' % (min(xs), max(xs), min(ys), max(ys)))
    print('  -> reduced x~%d..%d y~%d..%d' % (min(xs)*48//W, max(xs)*48//W, 6+min(ys)*26//H, 6+max(ys)*26//H))
