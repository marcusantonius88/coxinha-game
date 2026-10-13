from PIL import Image
from collections import Counter

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()
print('dog full-res size', W, H)

# Sample a horizontal strip near the top to reveal the ear columns & pink.
# Print distinct colors for rows y=10..40 across full width, grouped.
for y in [12, 20, 30, 45]:
    row = Counter()
    for x in range(0, W):
        r, g, b, a = p[x, y]
        if a > 100:
            row[(r, g, b)] += 1
    # show colors sorted by count
    top = row.most_common(8)
    print('y=%d distinct=%d :: %s' % (y, len(row), top))
