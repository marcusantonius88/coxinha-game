from PIL import Image
import os

d = 'assets/coxinha/idle-revision-e'
fr = [Image.open(os.path.join(d, 'idle_%02d.png' % i)).convert('RGBA') for i in range(4)]
W, H = 48, 32

def load(im):
    p = im.load()
    out = []
    for y in range(H):
        row = []
        for x in range(W):
            r, g, b, a = p[x, y]
            row.append((r, g, b) if a > 0 else None)
        out.append(row)
    return out

F = [load(f) for f in fr]

def diff(a, b):
    # returns (feet_diffs, body_diffs, head_diffs, alpha_only_diffs)
    feet = body = head = 0
    total = 0
    for y in range(H):
        for x in range(W):
            ca, cb = a[y][x], b[y][x]
            if ca is None and cb is None:
                continue
            if ca is None or cb is None:
                # alpha silhouette difference
                total += 1
                continue
            if ca != cb:
                total += 1
                if y >= 28:
                    feet += 1
                elif y >= 12:
                    body += 1
                else:
                    head += 1
    return feet, body, head, total

# base = frame 0
base = F[0]
for i in [1, 2, 3]:
    feet, body, head, total = diff(base, F[i])
    print('frame0 vs frame%d: feet=%d body=%d head=%d total=%d' % (i, feet, body, head, total))

# foot alignment: are the foot silhouettes byte-identical across all frames?
print('--- foot silhouette check (rows 28-31) ---')
for y in range(28, 32):
    sig = []
    for i in range(4):
        rowmask = ''.join('X' if F[i][y][x] is not None else '.' for x in range(W))
        sig.append(rowmask)
    same = all(s == sig[0] for s in sig)
    print('row%d identical-feet=%s  %s' % (y, same, sig[0]))

# full alpha silhouette equality across frames
print('--- alpha silhouette equality (all rows) ---')
for i in range(1, 4):
    diffs = 0
    for y in range(H):
        for x in range(W):
            if (F[0][y][x] is None) != (F[i][y][x] is None):
                diffs += 1
    print('frame0 vs frame%d silhouette diffs = %d' % (i, diffs))
