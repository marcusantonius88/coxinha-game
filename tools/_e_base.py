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


DW, DH, FW, FH = 48, 26, 48, 32
base_raw = None
reduced = []
for i, d in enumerate(dogs):
    r = alpha_aware_downscale(d, DW, DH)
    frame = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    frame.alpha_composite(r, (0, FH - DH))
    reduced.append(frame)

# --- build raw palette from pose0 (base) only, quantize generously then dedupe ---
strip = Image.new('RGBA', (dogs[0].width, dogs[0].height), (0, 0, 0, 0))
strip.alpha_composite(dogs[0])
pal_img = strip.convert('RGB').quantize(colors=24, method=Image.MEDIANCUT, dither=Image.NONE)
raw_pal = pal_img.getpalette()[:24 * 3]
cols = [tuple(raw_pal[i*3:i*3+3]) for i in range(24)]
# drop pure black (transparent compositing artifact)
cols = [c for c in cols if sum(c) > 12]
# dedupe: merge colors within euclidean 26
deduped = []
for c in cols:
    if all(sum((c[i] - e[i]) ** 2 for i in range(3)) ** 0.5 >= 26 for e in deduped):
        deduped.append(c)
print('deduped palette (%d):' % len(deduped))
for c in deduped:
    print('  ', c)

# --- alpha row profile of base (to find feet baseline) ---
base = reduced[0]
print('--- base alpha row profile (count opaque, xmin..xmax) ---')
for y in range(FH):
    cnt, xmin, xmax = 0, 99, -1
    for x in range(FW):
        if base.getpixel((x, y))[3] > 110:
            cnt += 1
            xmin = min(xmin, x)
            xmax = max(xmax, x)
    if cnt:
        print('  y=%2d  n=%2d  x=%2d..%2d' % (y, cnt, xmin, xmax))
