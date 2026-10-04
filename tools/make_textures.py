"""Build the moon textures used by the page from NASA's CGI Moon Kit.

Sources (public domain, NASA's Scientific Visualization Studio, item 4720):
  lroc_color_poles_2k.tif  LRO camera colour mosaic, 2048x1024
  ldem_16_uint.tif         LRO laser altimetry (LOLA), 16 pixels per degree

Outputs, written next to the page:
  moon_albedo.jpg  the colour map, rank-remapped onto the scene's teal palette
  moon_normal.jpg  a tangent-space normal map computed from the elevation, relief exaggerated

Usage:
  pip install numpy pillow
  python tools/make_textures.py            # downloads the two source files into tools/raw/
"""

import os
import sys
import urllib.request

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

BASE = "https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "..", "public", "games", "flymetothemoon")

W, H = 2048, 1024
RELIEF = 6.0  # normal-map slope exaggeration

# Palette the moon is remapped onto, as (rank, colour): the darkest maria at the bottom,
# the brightest highlands at the top.
STOPS = [
    (0.00, "#47727f"),
    (0.05, "#557f8b"),
    (0.25, "#608c97"),
    (0.50, "#6f9b9a"),
    (0.75, "#85a09d"),
    (0.95, "#91a6a6"),
    (1.00, "#9db1ac"),
]


def fetch(name):
    os.makedirs(RAW, exist_ok=True)
    path = os.path.join(RAW, name)
    if not os.path.exists(path):
        print("downloading", name)
        urllib.request.urlretrieve(f"{BASE}/{name}", path)
    return path


def hex_rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def main():
    lat = (0.5 - (np.arange(H) + 0.5) / H) * np.pi

    # Albedo: rank every pixel's brightness (weighted by area, so the stretched poles don't
    # skew it) and map the rank onto the palette. Keeps the real maria and ray craters.
    c = np.asarray(Image.open(fetch("lroc_color_poles_2k.tif")).convert("RGB")).astype(np.float64) / 255
    lum = 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
    wts = np.repeat(np.cos(lat)[:, None], W, 1).ravel()
    order = np.argsort(lum.ravel(), kind="stable")
    cdf = np.empty_like(wts)
    cdf[order] = np.cumsum(wts[order]) / wts.sum()
    q = np.array([s[0] for s in STOPS])
    cols = np.array([hex_rgb(s[1]) for s in STOPS])
    alb = np.stack([np.interp(cdf, q, cols[:, k]) for k in range(3)], 1).reshape(H, W, 3)
    Image.fromarray(np.clip(alb + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(OUT, "moon_albedo.jpg"), quality=90)

    # Normals: slopes of the elevation map (half-metre units) in metres per metre, with the
    # east-west spacing shrinking toward the poles.
    h = np.asarray(Image.open(fetch("ldem_16_uint.tif"))).astype(np.float32) * 0.5
    h = np.asarray(Image.fromarray(h).resize((W, H), Image.BOX)).astype(np.float64)
    radius = 1737.4e3
    dx = (2 * np.pi * radius / W * np.maximum(np.cos(lat), 0.02))[:, None]
    dy = np.pi * radius / H
    dh_east = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) / (2 * dx)
    hp = np.pad(h, ((1, 1), (0, 0)), mode="edge")
    dh_north = (hp[:-2] - hp[2:]) / (2 * dy)
    n = np.dstack([-dh_east * RELIEF, -dh_north * RELIEF, np.ones_like(h)])
    n /= np.sqrt((n ** 2).sum(2, keepdims=True))
    img = Image.fromarray(((n * 0.5 + 0.5) * 255 + 0.5).astype(np.uint8))
    img.save(os.path.join(OUT, "moon_normal.jpg"), quality=93, subsampling=0)
    print("wrote", OUT)


if __name__ == "__main__":
    sys.exit(main())
