from PIL import Image

base = Image.open('/tmp/ev/red_0.png').convert('RGBA')  # earlier full-res reduced (has pink)
p = base.load()
# ear region top-left of head: sample head band y=6..17
from collections import Counter
head = Counter()
for y in range(6, 18):
    for x in range(20, 40):
        r, g, b, a = p[x, y]
        if a > 110:
            head[(r, g, b)] += 1
print('--- head/ear band colors (top 12) ---')
for c, n in head.most_common(12):
    print('  %s  x%d' % (c, n))

# find likely pink: r>g and r>b significantly, mid brightness
pinks = [(c, n) for c, n in head.items() if c[0] > c[1] + 25 and c[0] > c[2] + 25 and 90 < c[0] < 245]
print('pink-ish in head:', pinks[:8])

# eye region: dark pixels surrounded by tan, around y=13..16, x=26..32
print('--- eye scan y=11..17 x=24..34 ---')
for y in range(11, 18):
    row = []
    for x in range(24, 35):
        r, g, b, a = p[x, y]
        if a > 110:
            lum = (r + g + b) // 3
            row.append('%3d' % lum)
        else:
            row.append('  .')
    print('y=%2d ' % y, ' '.join(row))
