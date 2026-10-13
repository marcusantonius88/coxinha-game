from PIL import Image
import os

def is_bg(r, g, b):
    return (b > r + 22) and (b > g + 12)

ref = Image.open('assets/coxinha/idle-reference.png').convert('RGB')
px = ref.load()
runs = [(17, 543), (563, 1077), (1105, 1620), (1648, 2162)]
YTOP, YBOT = 50, 328

dogs = []
for i, (x0, x1) in enumerate(runs):
    crop = ref.crop((x0, YTOP, x1 + 1, YBOT)).convert('RGBA')
    op = crop.load()
    for yy in range(crop.size[1]):
        for xx in range(crop.size[0]):
            r, g, b, a = op[xx, yy]
            if is_bg(r, g, b):
                op[xx, yy] = (0, 0, 0, 0)
    dogs.append(crop.crop(crop.getbbox()))

# normalize each dog to 48x26 by BOX (area avg) - same footprint for all
def norm(dog):
    return dog.resize((48, 26), Image.BOX)

N = [norm(d) for d in dogs]

# measure vertical displacement of body vs base using column-centroid of alpha above feet
def coltop(im, x):
    p = im.load()
    for y in range(26):
        if p[x, y][3] > 40:
            return y
    return 26

print('per-column top-y (body top) for each pose, rows where they differ:')
for x in range(48):
    tops = [coltop(N[i], x) for i in range(4)]
    if len(set(tops)) > 1:
        print('  x=%2d tops=%s (spread=%d)' % (x, tops, max(tops) - min(tops)))

# measure where body differs excluding feet (rows<22) and eye, count + max row-shift
def loadq(im):
    p = im.load()
    return [[(p[x,y][:3] if p[x,y][3]>40 else None) for x in range(48)] for y in range(26)]

Q = [loadq(n) for n in N]
for i in [1,2,3]:
    body = sum(1 for y in range(22) for x in range(48)
               if Q[0][y][x] != Q[i][y][x] and (Q[0][y][x] is not None or Q[i][y][x] is not None))
    print('pose0 vs pose%d body(rows<22) diffs=%d' % (i, body))
