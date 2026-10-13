from PIL import Image

d0 = Image.open('/tmp/ev/dog_0.png').convert('RGB')
W, H = d0.size
# head/ear region: reduced x~10..37, y~0..20  -> full: x 108..400, y 0..200
head = d0.crop((108, 0, 400, 200))
# magnify 4x nearest
big = head.resize((head.size[0]*4, head.size[1]*4), Image.NEAREST)
big.save('/tmp/ev/head_4x.png')
print('head_4x size', big.size)
