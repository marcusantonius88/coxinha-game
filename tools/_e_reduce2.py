from PIL import Image
from collections import Counter

# Locked identity palette measured from the high-res reference (dog_0 head zoom + hue scan)
PAL = {
    'black':    (15, 12, 12),    # outline + eye
    'muzdark':  (50, 33, 29),    # deep muzzle
    'muzmid':   (78, 47, 40),    # muzzle mid
    'rose':     (150, 70, 55),   # ear interior (dusty rose)
    'oranged':  (198, 118, 48),  # shaded fur
    'orange':   (228, 151, 63),  # body base
    'orangel':  (242, 192, 120), # top highlight
    'cream':    (245, 231, 203), # chest
}
NAMES = list(PAL.keys())
VALS = [PAL[n] for n in NAMES]

def nearest(c):
    r, g, b = c
    best, bd = 0, 1e9
    for i, (pr, pg, pb) in enumerate(VALS):
        d = (r-pr)*(r-pr)+(g-pg)*(g-pg)+(b-pb)*(b-pb)
        if d < bd:
            bd, best = d, i
    return best

def reduce_dog(src, TW, TH):
    W, H = src.size
    p = src.load()
    out = [[-1]*TW for _ in range(TH)]
    for cy in range(TH):
        ys0 = cy*H//TH; ys1 = (cy+1)*H//TH
        for cx in range(TW):
            xs0 = cx*W//TW; xs1 = (cx+1)*W//TW
            cnt = Counter(); opaque = 0
            for y in range(ys0, ys1):
                for x in range(xs0, xs1):
                    r, g, b, a = p[x, y]
                    if a < 128: continue
                    opaque += 1
                    idx = nearest((r, g, b))
                    nm = NAMES[idx]
                    w = 3 if nm == 'black' else 2 if nm in ('muzdark','muzmid','rose') else 1
                    cnt[idx] += w
            area = (ys1-ys0)*(xs1-xs0)
            if opaque >= max(2, area//8):
                best, bn = 0, -1
                for idx in range(len(VALS)):
                    n = cnt.get(idx, 0)
                    if n > bn or (n == bn and idx < best):
                        bn, best = n, idx
                out[cy][cx] = best
    return out

TW, TH = 48, 26
labels = {i: reduce_dog(Image.open('/tmp/ev/dog_%d.png' % i).convert('RGBA'), TW, TH) for i in (0,1,2,3)}

def render(grid, ox, oy, CW=48, CH=32):
    im = Image.new('RGBA', (CW, CH), (0,0,0,0)); q = im.load()
    for cy, row in enumerate(grid):
        for cx, idx in enumerate(row):
            if idx >= 0: q[cx+ox, cy+oy] = VALS[idx] + (255,)
    return im

for i in (0,1,2,3):
    c = Counter(v for row in labels[i] for v in row if v>=0)
    print('pose%d:' % i, {NAMES[k]: c.get(k,0) for k in range(len(NAMES)) if c.get(k,0)})

def bigview(im, sc=10):
    bg = Image.new('RGBA', im.size, (24,26,38,255)); bg.alpha_composite(im)
    return bg.convert('RGB').resize((im.size[0]*sc, im.size[1]*sc), Image.NEAREST)

strip = Image.new('RGB', (TW*10*4+8*3, TH*10+20), (10,10,16,255))
x=0
for i in (0,1,2,3):
    strip.paste(bigview(render(labels[i],0,6)), (x,0)); x += TW*10+8
strip.save('/tmp/ev/red_pose.png')
print('saved /tmp/ev/red_pose.png')
