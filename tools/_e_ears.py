from PIL import Image
import colorsys
from collections import Counter

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

# print colors in hue 330-360 regardless of val/sat
c = Counter()
for y in range(H):
    for x in range(W):
        r,g,b,a = p[x,y]
        if a < 150: continue
        h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
        if 330 <= h*360 <= 360 and v > 0.25:
            c[(r,g,b)] += 1
print('hue 330-360, v>0.25 :', sum(c.values()))
for col,n in c.most_common(8): print('  ',col,'x%d'%n)

# crop head+ears (right side, top) and zoom big
head = d0.crop((300, 0, W, 150))   # ears+head on right top
hw,hh = head.size
zbg = Image.new('RGBA',(hw,hh),(15,15,25,255)); zbg.alpha_composite(head)
zbg.convert('RGB').resize((hw*3,hh*3),Image.NEAREST).save('/tmp/ev/head_zoom.png')
print('head_zoom saved', head.size)

# Sample a vertical strip through left ear (x~330) and right ear (x~390) to read pink values
for x in (338, 348, 358, 396, 406):
    print('strip x=%d:'%x)
    for y in range(0, 90, 6):
        print('   y=%3d'%y, p[x,y])
