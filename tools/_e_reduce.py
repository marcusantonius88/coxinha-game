from PIL import Image

PAL_K = 15          # closed palette size
FW, FH = 48, 32     # frame
DW, DH = 48, 26     # dog fit (aspect 1.87 preserved, feet at bottom)

dogs = [Image.open('/tmp/ev/dog_%d.png' % i).convert('RGBA') for i in range(4)]

# --- shared palette from all 4 dogs ---
strip = Image.new('RGBA', (sum(d.width for d in dogs), max(d.height for d in dogs)), (0, 0, 0, 0))
x = 0
for d in dogs:
    strip.alpha_composite(d)
    x += d.width
pal_img = strip.convert('RGB').quantize(colors=PAL_K, method=Image.MEDIANCUT, dither=Image.NONE)
palette = pal_img.getpalette()[:PAL_K * 3]
PALETTE = [tuple(palette[i*3:i*3+3]) for i in range(PAL_K)]
print('shared palette (%d):' % PAL_K)
for c in PALETTE:
    print('  ', c)


def alpha_aware_downscale(dog, tw, th):
    """Box/area downscale with premultiplied alpha to avoid dark fringes."""
    sw, sh = dog.size
    # scale factor
    px = dog.load()
    # build premultiplied RGB image and separate alpha, then resize both with BOX
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
            if a > 110:                       # binary-ish alpha for crisp pixel art
                r, g, b = pr[xx, yy]
                f = a / 255.0
                if f > 0:
                    op[xx, yy] = (min(255, round(r / f)), min(255, round(g / f)), min(255, round(b / f)), 255)
                else:
                    op[xx, yy] = (0, 0, 0, 255)
            # else leave transparent
    return out


def quantize_to_palette(im, palette):
    q = im.convert('RGB').quantize(palette=Image.new('P', (0, 0)).putpalette(
        [ch for c in palette for ch in c]) if False else im.convert('RGB').quantize(
        colors=len(palette), method=Image.MEDIANCUT, dither=Image.NONE))
    return q.convert('RGBA')


# reduce each dog
reduced = []
for i, d in enumerate(dogs):
    r = alpha_aware_downscale(d, DW, DH)
    # place into 48x32 with feet at bottom
    frame = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    frame.alpha_composite(r, (0, FH - DH))
    reduced.append(frame)

# quantize each frame to the SHARED palette by nearest match (so all frames identical palette)
def nearest_map(im, palette):
    im = im.convert('RGB')
    src = im.load()
    w, h = im.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    op = out.load()
    # only quantize opaque pixels; keep alpha from original
    a_img = im.convert('RGBA').split()[3]
    for yy in range(h):
        for xx in range(w):
            a = a_img.getpixel((xx, yy))
            if a > 110:
                r, g, b = src[xx, yy]
                best, bd = None, 1e9
                for c in palette:
                    d2 = (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2
                    if d2 < bd:
                        bd, best = d2, c
                op[xx, yy] = (best[0], best[1], best[2], 255)
    return out

quant = [nearest_map(f, PALETTE) for f in reduced]

# --- diffs between frames (after quantize) ---
def mask(fr):
    return set((x, y) for y in range(fr.height) for x in range(fr.width)
               if fr.getpixel((x, y))[3] > 110)

masks = [mask(f) for f in quant]
for a in range(4):
    for b in range(a + 1, 4):
        diff = masks[a] ^ masks[b]
        color_diff = 0
        for (x, y) in (masks[a] & masks[b]):
            if quant[a].getpixel((x, y))[:3] != quant[b].getpixel((x, y))[:3]:
                color_diff += 1
        print('f%d vs f%d: alpha-xor=%d  color-diff(shared)=%d' % (a, b, len(diff), color_diff))

# save quantized frames to /tmp for viewing
for i, f in enumerate(quant):
    f.save('/tmp/ev/red_%d.png' % i)
print('saved /tmp/ev/red_*.png')
