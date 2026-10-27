import sys, numpy as np
from PIL import Image, ImageFilter
W, H = 1920, 1080
rng = np.random.default_rng(7)
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
cx, cy = W * 0.62, H * 0.40
img = np.zeros((H, W, 3), np.float32)
img += np.array([2, 3, 8], np.float32)  # deep space
# stars
n = 2600
sx, sy = rng.integers(0, W, n), rng.integers(0, H, n)
b = rng.power(6, n) * 255
img[sy, sx] = np.stack([b, b * 0.95, b * 0.9], 1)
# faint nebula haze
haze = np.exp(-(((x - W * 0.2) / 700) ** 2 + ((y - H * 0.8) / 380) ** 2))
img += haze[..., None] * np.array([10, 14, 30], np.float32)
dx, dy = x - cx, y - cy
R = 150.0  # shadow radius
# accretion disk seen almost edge-on: thin bright band through the hole
band = np.exp(-((dy / 9.0) ** 2)) * np.exp(-((np.abs(dx) / 760) ** 2.2))
# lensed ring (the disk's far side bent over and under the shadow)
r = np.hypot(dx / 1.0, dy / 0.92)
ring = np.exp(-(((r - R * 1.18) / 16.0) ** 2))
halo = np.exp(-(((r - R * 1.25) / 70.0) ** 2)) * 0.35
# Doppler beaming: left side brighter
beam = 1.0 + 0.55 * np.tanh(-dx / 300)
light = (band * 1.4 + ring + halo) * beam
warm = np.array([255, 196, 120], np.float32)
hot = np.array([255, 245, 225], np.float32)
img += light[..., None] * (warm * 0.8) + (np.clip(light - 0.6, 0, None))[..., None] * hot * 0.6
# event horizon shadow, drawn over the far ring but under the near disk band
shadow = np.clip((r - R) / 4.0, 0, 1)
front = np.exp(-((dy / 7.0) ** 2)) * np.exp(-((np.abs(dx) / 700) ** 2.2)) * (dy > -6)
img = img * shadow[..., None] + (1 - shadow)[..., None] * (front[..., None] * warm * 1.2 * beam[..., None])
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
glow = im.filter(ImageFilter.GaussianBlur(18))
out = Image.blend(im, glow, 0.35)
out = Image.fromarray(np.clip(np.asarray(out, np.float32) + np.asarray(glow, np.float32) * 0.5, 0, 255).astype(np.uint8))
out.save(sys.argv[1], quality=90)
