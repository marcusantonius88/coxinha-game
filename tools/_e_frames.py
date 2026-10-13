from PIL import Image
import os

OUT = 'assets/coxinha/idle-revision-e'
os.makedirs(OUT, exist_ok=True)

def load_dog(i):
    im = Image.open('/tmp/ev/dog_%d.png' % i).convert('RGBA')
    W, H = im.size
    p = im.load()
    wid = [sum(1 for x in range(W) if p[x, y][3] > 120) for y in range(H)]
    maxw = max(wid)
    bottom = H - 1
    while bottom > 0 and wid[bottom] > 0.90 * maxw:   # trim ground line
        bottom -= 1
    top = 0
    while top < bottom and wid[top] == 0:             # trim empty top
        top += 1
    return im.crop((0, top, W, bottom + 1))

dogs = [load_dog(i) for i in range(4)]
for i, d in enumerate(dogs):
    print('dog%d %s' % (i, d.size))

PALRGB = [
    (0, 0, 0), (22, 22, 26), (48, 38, 40), (120, 70, 45),
    (166, 89, 34), (206, 132, 58), (224, 152, 66), (238, 182, 104),
    (237, 113, 90), (208, 92, 76), (244, 240, 225), (250, 250, 248),
]

def nearest(r, g, b):
    best = 0; bd = 1e9
    for i, (pr, pg, pb) in enumerate(PALRGB):
        d = (r-pr)*(r-pr)+(g-pg)*(g-pg)+(b-pb)*(b-pb)
        if d < bd:
            bd = d; best = i
    return best

def quantize(img):
    img = img.convert('RGBA')
    out = Image.new('P', img.size, 0)
    out.putpalette([c for col in PALRGB for c in col])
    src = img.load(); dst = out.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = src[x, y]
            dst[x, y] = nearest(r, g, b) if a >= 128 else 0
    alpha = img.split()[3].point(lambda v: 255 if v >= 128 else 0)
    rgba = out.convert('RGBA'); rgba.putalpha(alpha)
    return rgba

FEET_ROW = 28           # feet baseline, matches current asset (88.6% of 32)
BOX_W, BOX_H = 48, 32

def place(dog, target_h):
    w, h = dog.size
    nw = max(1, round(w * target_h / h))
    small = dog.resize((nw, target_h), Image.LANCZOS)
    q = quantize(small)
    frame = Image.new('RGBA', (BOX_W, BOX_H), (0, 0, 0, 0))
    top = FEET_ROW - target_h + 1
    left = (BOX_W - nw) // 2
    frame.alpha_composite(q, (left, top))
    return frame

BASE = dogs[3]     # neutral
BLINK = dogs[2]    # artist blink pose

frames = [
    place(BASE, 24),   # 0 neutral
    place(BASE, 25),   # 1 inhale +1
    place(BLINK, 24),  # 2 blink
    place(BASE, 23),   # 3 exhale -1
]

for i, f in enumerate(frames):
    f.save('%s/idle_%02d.png' % (OUT, i))
    print('idle_%02d.png saved, bbox=%s' % (i, f.getbbox()))

# sheet
sheet = Image.new('RGBA', (BOX_W*4, BOX_H), (0, 0, 0, 0))
for i, f in enumerate(frames):
    sheet.alpha_composite(f, (BOX_W*i, 0))
sheet.save('%s/coxinha_idle_spritesheet.png' % OUT)
print('sheet saved', sheet.size)
