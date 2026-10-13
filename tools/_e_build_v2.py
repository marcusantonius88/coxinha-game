from PIL import Image

def load_dog(i):
    im = Image.open('/tmp/ev/dog_%d.png' % i).convert('RGBA')
    W, H = im.size
    p = im.load()
    wid = [sum(1 for x in range(W) if p[x, y][3] > 120) for y in range(H)]
    maxw = max(wid)
    bottom = H - 1
    while bottom > 0 and wid[bottom] > 0.90 * maxw:
        bottom -= 1
    return im.crop((0, 0, W, bottom + 1))

dogs = [load_dog(i) for i in range(4)]
for i, d in enumerate(dogs):
    print('dog%d cleaned size=%s' % (i, d.size))

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
    rgba = out.convert('RGBA')
    rgba.putalpha(alpha)
    return rgba

def fit_height(dog, target_h):
    w, h = dog.size
    nw = max(1, round(w * target_h / h))
    return dog.resize((nw, target_h), Image.LANCZOS), nw

BASE = dogs[3]
BASE_H = 23
base_img, base_w = fit_height(BASE, BASE_H)
base_q = quantize(base_img)
base_q.save('/tmp/ev/E_base_q.png')
big = base_q.resize((base_w*12, BASE_H*12), Image.NEAREST)
bg = Image.new('RGBA', big.size, (28, 30, 46, 255)); bg.alpha_composite(big)
bg.convert('RGB').save('/tmp/ev/E_base_big.png')
print('base %dx%d quantized; saved views' % (base_w, BASE_H))
