from PIL import Image

dogs = [Image.open('/tmp/ev/dog_%d.png' % i).convert('RGBA') for i in range(4)]
# put each on a common bottom-anchored canvas 520x280
CW, CH = 520, 280
canvas = []
for d in dogs:
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    c.paste(d, (0, CH - d.size[1]), d)
    canvas.append(c)

def alpha(im): return im.split()[3]

def diffmask(a, b):
    pa, pb = a.load(), b.load()
    dm = Image.new('L', (CW, CH), 0)
    pd = dm.load()
    for y in range(CH):
        for x in range(CW):
            av = pa[x, y] > 100
            bv = pb[x, y] > 100
            if av != bv:
                pd[x, y] = 255
    return dm

pairs = [(0,1),(1,2),(2,3),(1,3),(0,3)]
for i,j in pairs:
    dm = diffmask(canvas[i], canvas[j])
    bbox = dm.getbbox()
    cnt = sum(1 for y in range(CH) for x in range(CW) if dm.load()[x,y]>0)
    print('pose%d vs pose%d: diff px=%d bbox=%s' % (i,j,cnt,bbox))

# row-width profile of each (breathing = width change in body rows)
print('row width profiles (every 10th row), x-extent:')
for i,c in enumerate(canvas):
    p = c.load()
    widths = []
    for y in range(0, CH, 15):
        xs = [x for x in range(CW) if p[x,y][3] > 100]
        widths.append((y, (min(xs),max(xs)) if xs else None))
    print(' pose%d' % i, widths)

from PIL import Image

dogs = [Image.open('/tmp/ev/dog_%d.png' % i).convert('RGBA') for i in range(4)]


def alpha_aware_downscale(dog, tw, th):
    sw, sh = dog.size
    px = dog.load()
    premul = Image.new('RGB', (sw, sh), (0, 0, 0))
    alpha = Image.new('L', (sw, sh), 0)
    dp, ap = premul.load(), alpha.load()
    for yy in range(sh):
        for xx in range(sw):
            r, g, b, a = px[xx, yy]
            ap[xx, yy] = a
            if a:
                f = a / 255.0
                dp[xx, yy] = (int(r * f), int(g * f), int(b * f))
    premul_r = premul.resize((tw, th), Image.Resampling.BOX)
    alpha_r = alpha.resize((tw, th), Image.Resampling.BOX)
    pr, ar = premul_r.load(), alpha_r.load()
    out = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    op = out.load()
    for yy in range(th):
        for xx in range(tw):
            a = ar[xx, yy]
            if a > 110:
                r, g, b = pr[xx, yy]
                f = a / 255.0
                op[xx, yy] = (min(255, round(r / f)), min(255, round(g / f)), min(255, round(b / f)), 255) if f > 0 else (0, 0, 0, 255)
    return out


DW, DH = 48, 26
# reduce WITHOUT quantize -> to see genuine artist variation
reduced = []
for i, d in enumerate(dogs):
    r = alpha_aware_downscale(d, DW, DH)
    frame = Image.new('RGBA', (48, 32), (0, 0, 0, 0))
    frame.alpha_composite(r, (0, 32 - DH))
    reduced.append(frame)

# genuine color variation between poses, restricted to shared opaque pixels
def shared_opaque(a, b):
    S = []
    for y in range(32):
        for x in range(48):
            if a.getpixel((x, y))[3] > 110 and b.getpixel((x, y))[3] > 110:
                S.append((x, y))
    return S

for a, b in [(0, 1), (1, 3), (0, 3), (0, 2), (1, 2)]:
    S = shared_opaque(reduced[a], reduced[b])
    rows = {}
    big = 0
    for (x, y) in S:
        ca = reduced[a].getpixel((x, y))[:3]
        cb = reduced[b].getpixel((x, y))[:3]
        d2 = sum((ca[i] - cb[i]) ** 2 for i in range(3)) ** 0.5
        if d2 > 18:  # meaningful change (not anti-alias noise)
            rows[y] = rows.get(y, 0) + 1
            big += 1
    rmin = min(rows) if rows else None
    rmax = max(rows) if rows else None
    print('f%d vs f%d: %d/%d px changed meaningfully; rows affected %s..%s' %
          (a, b, big, len(S), rmin, rmax))
    if rows:
        rr = sorted(rows.items())
        print('    row histogram:', rr[:20])
