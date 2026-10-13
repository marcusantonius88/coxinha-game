from PIL import Image

# --- current asset true geometry ---
cur = Image.open('assets/coxinha/coxinha-idle.png').convert('RGBA')
CW, CH = cur.size
c = cur.load()
minx = miny = 10**9; maxx = maxy = -1
for y in range(CH):
    for x in range(CW):
        if c[x, y][3] > 40:
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y
print('current asset %dx%d' % (CW, CH))
print('  dog bbox x=%d..%d y=%d..%d  (w=%d h=%d)' % (minx, maxx, miny, maxy, maxx-minx+1, maxy-miny+1))
print('  feet baseline y=%d  -> %.1f%% down' % (maxy, 100*maxy/CH))
print('  displayed 96x64 -> feet at %.1f px from top; dog box 96x64' % (64*maxy/CH))
# feet baseline mapped to a 32-tall frame
print('  mapped to 48x32 box: feet baseline row ~%.1f' % (32*maxy/CH))
print('  dog width mapped: %.1f of 48' % (48*(maxx-minx+1)/CW))
