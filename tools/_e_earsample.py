from PIL import Image
from collections import Counter

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGB')
W, H = d0.size
p = d0.load()

# From the 4x head view (crop origin x=108,y=0, each src px = 4 view px):
# front ear interior brightest pink sits around src (x~168..186, y~18..70)
# back ear interior around src (x~272..288, y~34..74)
def sample(x0, x1, y0, y1, label):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = p[x, y]
            c[(r, g, b)] += 1
    tot = [0, 0, 0]; n = 0
    for cc, k in c.items():
        for i in range(3): tot[i] += cc[i] * k
        n += k
    print('%s avg=%s top=%s' % (label, tuple(round(t/n) for t in tot), c.most_common(3)))
    return c

sample(168, 188, 20, 68, 'front-ear-interior')
sample(270, 292, 36, 72, 'back-ear-interior')
# cream chest: lower front, near src (x~190..240, y~170..230)
sample(190, 245, 175, 235, 'chest')
# muzzle dark: src (x~150..205, y~150..210)
sample(150, 210, 150, 210, 'muzzle')
