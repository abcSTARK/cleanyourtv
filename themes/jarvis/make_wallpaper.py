import sys, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
W, H = 1280, 720
cx, cy = int(W * 0.66), int(H * 0.40)
base = Image.new("RGB", (W, H), (2, 7, 16))
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
glow = np.exp(-(((x - cx) / 420) ** 2 + ((y - cy) / 300) ** 2))
arr = np.asarray(base, np.float32) + glow[..., None] * np.array([0, 40, 70], np.float32)
base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
hud = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(hud)
C, D = (90, 220, 255), (30, 110, 150)
# faint hex grid
s = 26
for row in range(-1, H // s + 2):
    for col in range(-1, W // s + 2):
        hx = col * s * 1.5; hy = row * s * math.sqrt(3) + (col % 2) * s * math.sqrt(3) / 2
        if math.hypot(hx - cx, hy - cy) > 470: continue
        pts = [(hx + s * 0.55 * math.cos(math.radians(60 * k)), hy + s * 0.55 * math.sin(math.radians(60 * k))) for k in range(7)]
        d.line(pts, fill=(8, 34, 48), width=1)
def arc(r, a0, a1, w, c): d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=c, width=w)
# concentric HUD rings with gaps
for r, segs, w, c in [(70, [(0, 360)], 6, C), (95, [(20, 160), (200, 340)], 3, C), (130, [(0, 70), (90, 250), (270, 340)], 2, D),
                      (165, [(300, 420), (130, 230)], 5, C), (205, [(0, 360)], 1, D), (240, [(200, 300), (330, 380), (20, 160)], 2, C),
                      (300, [(0, 360)], 1, (14, 60, 84))]:
    for a0, a1 in segs: arc(r, a0, a1, w, c)
for k in range(120):  # tick ring
    a = math.radians(k * 3); r0 = 212; r1 = 222 if k % 5 else 230
    d.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))], fill=D, width=1)
for k in range(10):  # arc reactor-style core segments
    a0 = k * 36 + 4
    arc(48, a0, a0 + 26, 14, (150, 235, 255))
d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(200, 245, 255))
# data lines
for i, (y0, ln) in enumerate([(cy - 120, 170), (cy - 100, 120), (cy + 110, 150), (cy + 130, 90)]):
    x0 = cx + 330
    d.line([(x0, y0), (x0 + ln, y0)], fill=D, width=2); d.rectangle([x0 - 6, y0 - 3, x0, y0 + 3], fill=C)
out = Image.composite(hud, base, hud.convert("L").point(lambda v: 255 if v else 0))
out = Image.blend(out, out.filter(ImageFilter.GaussianBlur(6)), 0.3)
g = np.asarray(hud.filter(ImageFilter.GaussianBlur(14)), np.float32) * 0.6
out = Image.fromarray(np.clip(np.asarray(out, np.float32) + g, 0, 255).astype(np.uint8))
out.save(sys.argv[1], quality=90)
