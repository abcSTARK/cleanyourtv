# One black-hole family for every dock app: same Gargantua-style composition, ring tinted per app.
import sys, os, numpy as np
from PIL import Image, ImageFilter
W, H = 1280, 720
out = sys.argv[1]
y, x = np.mgrid[0:H, 0:W].astype(np.float32)

def hole(name, warm, seed):
    warm = np.array(warm, np.float32)
    r0 = np.random.default_rng(seed)
    img = np.zeros((H, W, 3), np.float32) + np.array([2, 3, 8])
    sx, sy = r0.integers(0, W, 1500), r0.integers(0, H, 1500)
    img[sy, sx] = np.maximum(img[sy, sx], r0.power(5, 1500)[:, None] * 255)
    cx, cy, R = W * 0.70, H * 0.34, 100.0
    dx, dy = x - cx, y - cy; r = np.hypot(dx, dy / 0.92)
    # thicker, tilted-looking disk: brighter near the hole, fading outward
    band = np.exp(-((dy / 9.0) ** 2)) * (np.exp(-((np.abs(dx) / 480) ** 1.6)))
    ring = np.exp(-(((r - R * 1.18) / 10.0) ** 2)) + np.exp(-(((r - R * 1.28) / 46.0) ** 2)) * 0.4
    beam = 1.0 + 0.6 * np.tanh(-dx / 200)
    light = (band * 1.5 + ring) * beam
    img += light[..., None] * warm * 0.85 + np.clip(light - 0.7, 0, None)[..., None] * 150
    shadow = np.clip((r - R) / 3.0, 0, 1)
    front = np.exp(-((dy / 6.0) ** 2)) * np.exp(-((np.abs(dx) / 460) ** 1.6)) * (dy > -5)
    img = img * shadow[..., None] + (1 - shadow)[..., None] * front[..., None] * warm * 1.3
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    g = np.asarray(im.filter(ImageFilter.GaussianBlur(16)), np.float32)
    o = np.asarray(im, np.float32) + g * 0.7 + np.random.default_rng(seed + 1).normal(0, 1.8, (H, W, 1))
    Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).save(os.path.join(out, name), quality=90)

hole("wallpaper.jpg", (255, 190, 115), 1)                                            # classic gold
w = "wallpapers/hero_"
hole(w + "in.startv.hotstar.jpg", (190, 120, 255), 2)                                # violet
hole(w + "com.google.android.youtube.tv.jpg", (255, 120, 90), 3)                     # red-orange
hole(w + "com.netflix.ninja.jpg", (235, 70, 80), 4)                                  # crimson
hole(w + "com.amazon.amazonvideo.livingroom.jpg", (110, 190, 255), 5)                # blue
