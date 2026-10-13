from PIL import Image

REF = 'assets/coxinha/idle-reference.png'
ref = Image.open(REF).convert('RGB')
W, H = ref.size
px = ref.load()

# background = blue-dominant. Build alpha mask: alpha=0 where blue bg, 255 otherwise.
def is_bg(r, g, b):
    return (b > r + 22) and (b > g + 12)

# per-pose column runs (from detection)
runs = [(17, 543), (563, 1077), (1105, 1620), (1648, 2162)]

import os
os.makedirs('/tmp/ev', exist_ok=True)

for i, (x0, x1) in enumerate(runs):
    crop = ref.crop((x0, 0, x1 + 1, H))
    cp = crop.load()
    cw, ch = crop.size
    # make transparent where bg
    out = crop.convert('RGBA')
    op = out.load()
    for yy in range(ch):
        for xx in range(cw):
            r, g, b, a = op[xx, yy]
            if is_bg(r, g, b):
                op[xx, yy] = (r, g, b, 0)
    # tight bbox on alpha
    bbox = out.getbbox()
    print('pose%d crop=%s alpha_bbox=%s' % (i, (cw, ch), bbox))
    # downscale for viewing (keep aspect), target width 260
    vw = 260
    vh = max(1, round(ch * vw / cw))
    view = out.resize((vw, vh), Image.NEAREST)
    bg = Image.new('RGBA', view.size, (24, 26, 40, 255))
    bg.alpha_composite(view)
    bg.convert('RGB').save('/tmp/ev/pose_%d_view.png' % i)
    # also save full-res RGBA crop
    out.save('/tmp/ev/pose_%d_full.png' % i)

print('done')
