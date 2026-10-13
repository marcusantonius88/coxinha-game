from PIL import Image

ref = Image.open('assets/coxinha/idle-reference.png').convert('RGB')
W, H = ref.size
px = ref.load()

def is_bg(r, g, b):
    return (b > r + 22) and (b > g + 12)

runs = [(17, 543), (563, 1077), (1105, 1620), (1648, 2162)]

for i, (x0, x1) in enumerate(runs):
    # vertical content profile: count non-bg px per row
    prof = []
    for y in range(H):
        c = 0
        for x in range(x0, x1 + 1):
            r, g, b = px[x, y]
            if not is_bg(r, g, b):
                c += 1
        prof.append(c)
    # find content row segments (>=2 px wide to ignore specks)
    segs = []
    y = 0
    while y < H:
        if prof[y] >= 2:
            s = y
            while y < H and prof[y] >= 2:
                y += 1
            segs.append((s, y - 1))
        else:
            y += 1
    # horizontal extent over the main (tallest) segment
    main = max(segs, key=lambda s: s[1] - s[0]) if segs else None
    print('pose%d: content-row segments (y ranges) = %s' % (i, segs))
    if main:
        ys, ye = main
        # x extent within main
        xs0, xs1 = None, None
        for x in range(x0, x1 + 1):
            has = any(not is_bg(*px[x, y]) for y in range(ys, ye + 1))
            if has:
                if xs0 is None:
                    xs0 = x
                xs1 = x
        print('   main seg y=%d..%d (h=%d)  x=%d..%d (w=%d)  aspect=%.3f'
              % (ys, ye, ye - ys + 1, xs0, xs1, xs1 - xs0 + 1,
                 (xs1 - xs0 + 1) / (ye - ys + 1)))
