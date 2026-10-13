from PIL import Image

dogs = [Image.open('/tmp/ev/dog_%d.png' % i).convert('RGBA') for i in range(4)]
W = min(d.size[0] for d in dogs); H = min(d.size[1] for d in dogs)
print('common compare box', W, H)

def op(im, x, y):
    return im.getpixel((x, y))[3] > 120

def diff(a, b):
    n = 0
    for y in range(H):
        for x in range(W):
            if op(dogs[a], x, y) != op(dogs[b], x, y):
                n += 1
    return n

for (i, j) in [(0,1),(1,3),(0,3),(1,2),(2,3),(0,2)]:
    print('alpha-diff pose%d vs pose%d = %d px (%.2f%%)'
          % (i, j, diff(i, j), 100*diff(i, j)/(W*H)))

for i in range(4):
    widths = [sum(1 for x in range(W) if op(dogs[i], x, y)) for y in range(H)]
    lastop = max(y for y in range(H) if widths[y] > 0)
    top = min(y for y in range(H) if widths[y] > 0)
    print('pose%d: toprow=%d feetrow=%d maxw=%d' % (i, top, lastop, max(widths)))
