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

# curated identity palette (anchors measured from reference)
PAL = {
    'outline':    (10, 8, 8),
    'muzzle':     (54, 40, 36),
    'muzzle2':    (92, 62, 50),
    'fur_dark':   (166, 89, 34),
    'fur_main':   (228, 151, 63),
    'fur_light':  (238, 195, 140),
    'cream':      (246, 232, 198),
    'pink':       (239, 117, 93),
    'eye':        (40, 30, 28),
}
names = list(PAL.keys())
rgb = [PAL[n] for n in names]
def nearest(c):
    r, g, b = c[:3]
    best, bi = 1e18, 0
    for i, (pr, pg, pb) in enumerate(rgb):
        dd = (r-pr)*(r-pr)+(g-pg)*(g-pg)+(b-pb)*(b-pb)
        if dd < best: best, bi = dd, i
    return bi

TW, TH = 48, 26
OUT_W, OUT_H = 48, 32
DOG_TOP = 6
FEET_ROWS = list(range(22, 26))  # dog-space rows that are the feet/paws

def quantize(dog):
    small = dog.resize((TW, TH), Image.BOX)
    sp = small.load()
    q = Image.new('RGBA', (TW, TH)); qp = q.load()
    for yy in range(TH):
        for xx in range(TW):
            r, g, b, a = sp[xx, yy]
            qp[xx, yy] = (0, 0, 0, 0) if a < 40 else rgb[nearest((r, g, b))] + (255,)
    return q

# quantize all four artist poses
Q = [quantize(d) for d in dogs]

# pin feet: copy base (pose0) foot rows onto poses 1,2,3 so feet are identical
base = Q[0]
bp = base.load()
for qi in [1, 2, 3]:
    qp = Q[qi].load()
    for y in FEET_ROWS:
        for x in range(TW):
            qp[x, y] = bp[x, y]

# also copy the bottom silhouette (alpha) of feet fully from base to avoid gaps
def place(dog48x26, dog_top):
    canvas = Image.new('RGBA', (OUT_W, OUT_H), (0, 0, 0, 0))
    canvas.paste(dog48x26, (0, dog_top))
    return canvas

frames = [place(q, DOG_TOP) for q in Q]

os.makedirs('assets/coxinha/idle-revision-e', exist_ok=True)
for i, fr in enumerate(frames):
    fr.save('assets/coxinha/idle-revision-e/idle_%02d.png' % i)

for i, fr in enumerate(frames):
    vw = 480; vh = round(OUT_H * vw / OUT_W)
    view = fr.resize((vw, vh), Image.NEAREST)
    bgv = Image.new('RGBA', view.size, (30, 32, 48, 255)); bgv.alpha_composite(view)
    bgv.convert('RGB').save('/tmp/ev/fin_%02d.png' % i)
print('revision-e final: 4 artist poses quantized, feet pinned to base')
