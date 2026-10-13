from PIL import Image

src = Image.open('assets/coxinha/idle-reference.png')
print('REFERENCE mode=%s size=%s' % (src.mode, src.size))
rgb = src.convert('RGB')
# sample a few pixels inside pose0 dog body (x~250,y~200) and ear area
for (x, y, label) in [(250, 200, 'body?'), (200, 120, 'ear?'), (250, 260, 'chest?'), (60, 40, 'bg-corner')]:
    print('  ref px(%d,%d) %s -> %s' % (x, y, label, rgb.getpixel((x, y))))

print('---saved dog_1---')
d = Image.open('/tmp/ev/dog_1.png')
print('dog_1 mode=%s size=%s' % (d.mode, d.size))
dr = d.convert('RGBA')
# find first few opaque pixels and print them
n = 0
for yy in range(dr.size[1]):
    for xx in range(dr.size[0]):
        r, g, b, a = dr.getpixel((xx, yy))
        if a > 40:
            print('  dog_1 opaque px(%d,%d)=%s' % (xx, yy, (r, g, b, a)))
            n += 1
            if n >= 6:
                break
    if n >= 6:
        break

# count distinct opaque colors in dog_1 (full res, no resize)
seen = set()
for yy in range(dr.size[1]):
    for xx in range(dr.size[0]):
        r, g, b, a = dr.getpixel((xx, yy))
        if a > 40:
            seen.add((r, g, b))
print('dog_1 distinct opaque colors:', len(seen))
import statistics
mx = max(max(c) for c in seen)
print('dog_1 max channel value:', mx)
