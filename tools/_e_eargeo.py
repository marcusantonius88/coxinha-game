from PIL import Image

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

def is_pink(r, g, b):
    return r > 200 and g > 110 and b < 175 and r - b > 55 and b >= g - 5

def is_earorange(r, g, b):
    return 200 <= r and 55 <= g <= 110 and b <= 70

# per-column: topmost ear-orange y, topmost pink y, bottom of ear region
print('col: earOrange(top,bot) | pink(top,bot) | dogtop')
for x in range(120, 400, 6):
    eo_top = eo_bot = None
    pk_top = pk_bot = None
    dt = None
    for y in range(H):
        r, g, b, a = p[x, y]
        if a > 150:
            if dt is None: dt = y
            if is_earorange(r, g, b):
                if eo_top is None: eo_top = y
                eo_bot = y
            if is_pink(r, g, b):
                if pk_top is None: pk_top = y
                pk_bot = y
    if dt is not None and dt < 120:  # head/ear zone
        print('x=%3d dt=%3d  eo=(%s,%s) pk=(%s,%s)' % (x, dt, eo_top, eo_bot, pk_top, pk_bot))
