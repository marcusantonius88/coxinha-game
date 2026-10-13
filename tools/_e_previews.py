from PIL import Image
import os

OUT = 'assets/coxinha/idle-revision-e'
BASE = 'assets/coxinha'

frames = [Image.open('%s/idle_%02d.png' % (OUT, i)).convert('RGBA') for i in range(4)]
cur = Image.open('%s/coxinha-idle.png' % BASE).convert('RGBA')

CHECK = (24, 26, 40, 255)

def big(im, s):
    v = im.resize((im.size[0]*s, im.size[1]*s), Image.NEAREST)
    bg = Image.new('RGBA', v.size, CHECK); bg.alpha_composite(v)
    return bg.convert('RGB')

# 1) enlarged 4-frame sheet preview x10
sheet = Image.open('%s/coxinha_idle_spritesheet.png' % OUT).convert('RGBA')
big(sheet, 10).save('%s/preview-sheet-x10.png' % OUT)

# 2) comparison: current vs revision-e frames, all at same display box
# current displays 96x64; place on a matching canvas with feet at 88.6%
def cur_on_canvas(w, h):
    # scale current so its feet baseline matches the frames' feet (row 29/32)
    cw, ch = cur.size
    # dog bbox in current
    p = cur.load()
    minx=miny=10**9; maxx=maxy=-1
    for y in range(ch):
        for x in range(cw):
            if p[x,y][3] > 40:
                minx=min(minx,x); maxx=max(maxx,x); miny=min(miny,y); maxy=max(maxy,y)
    dog = cur.crop((minx, miny, maxx+1, maxy+1))
    # target: dog height so feet at row 29 of 32 -> height 25 rows -> display h
    disp_h = 25*8   # x8 rows
    dw = round(dog.size[0]*disp_h/dog.size[1])
    d = dog.resize((dw, disp_h), Image.LANCZOS)
    canvas = Image.new('RGBA', (w, h), CHECK)
    feet_row = 29
    top = feet_row*8 - disp_h + 8
    left = (w - dw)//2
    canvas.alpha_composite(d, (left, top))
    return canvas.convert('RGB')

CW, CH = 48*8, 32*8   # 384 x 256
cur_canvas = cur_on_canvas(CW, CH)
cur_canvas.save('%s/preview-atual-x8.png' % OUT)

# side by side comparison strip: [current] [e0 e1 e2 e3]
labels_h = 0
strip = Image.new('RGB', (CW + 10 + 48*4*8, CH), (12,12,18))
strip.paste(cur_canvas, (0,0))
for i in range(4):
    strip.paste(big(frames[i], 8), (CW+10 + i*48*8, 0))
strip.save('%s/preview-comparacao-atual.png' % OUT)
print('previews saved:', os.listdir(OUT))
