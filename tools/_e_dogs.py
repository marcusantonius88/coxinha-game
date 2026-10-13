from PIL import Image

ref = Image.open('assets/coxinha/idle-reference.png').convert('RGB')
px = ref.load()

def is_bg(r, g, b):
    return (b > r + 22) and (b > g + 12)

# column runs
runs = [(17, 543), (563, 1077), (1105, 1620), (1648, 2162)]
# dog body vertical band (top dog); ground line near y=331 -> trim a few bottom rows
YTOP, YBOT = 50, 328   # exclude the ground line at ~329-331

import os
os.makedirs('/tmp/ev', exist_ok=True)

crops = []
for i, (x0, x1) in enumerate(runs):
    crop = ref.crop((x0, YTOP, x1 + 1, YBOT)).convert('RGBA')
    op = crop.load()
    cw, ch = crop.size
    for yy in range(ch):
        for xx in range(cw):
            r, g, b, a = op[xx, yy]
            if is_bg(r, g, b):
                op[xx, yy] = (0, 0, 0, 0)
    bbox = crop.getbbox()
    tight = crop.crop(bbox)
    print('pose%d tight bbox=%s size=%s aspect=%.3f' % (i, bbox, tight.size, tight.size[0]/tight.size[1]))
    tight.save('/tmp/ev/dog_%d.png' % i)
    # big nearest view
    vw = 300
    vh = max(1, round(tight.size[1] * vw / tight.size[0]))
    view = tight.resize((vw, vh), Image.NEAREST)
    bgv = Image.new('RGBA', view.size, (30, 32, 48, 255))
    bgv.alpha_composite(view)
    bgv.convert('RGB').save('/tmp/ev/dog_%d_big.png' % i)
    crops.append(tight)

# diff stances: compare pose1 vs pose3 (both should be neutral), pose2 vs pose1 (blink)
def to_mask(im):
    m = im.split()[3].point(lambda a: 255 if a > 40 else 0)
    return m

print('done isolating')
