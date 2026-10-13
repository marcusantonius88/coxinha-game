from PIL import Image
from collections import Counter

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGBA')
W, H = d0.size
p = d0.load()

# horizontal run lengths within a mid row (body area, has both orange & features)
runlens = Counter()
for y in range(H//3, H//2):
    x = 0
    while x < W:
        c = p[x, y]
        j = x
        while j < W and p[j, y] == c:
            j += 1
        if j - x > 0:
            runlens[j - x] += 1
        x = j

# vertical run lengths in a column through the body
vruns = Counter()
for x in range(W//3, W//2):
    y = 0
    while y < H:
        c = p[x, y]
        j = y
        while j < H and p[j] == c if False else (j < H and p[x, j] == c):
            j += 1
        y = j
        if j - y >= 0:
            vruns[j - y] += 1

print('most common horizontal run lengths:', runlens.most_common(8))

# Count how many distinct transitions in a body row -> native width estimate
# If upscale factor is F, native width ~ W/F
for y in [H//3, H//3+5, H//2]:
    trans = sum(1 for x in range(1, W) if p[x, y] != p[x-1, y])
    print('row y=%d transitions=%d  => est native width if F=%d : %d' %
          (y, trans, 1, trans+1))
