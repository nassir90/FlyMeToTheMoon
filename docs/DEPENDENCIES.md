# Dependencies

What the scene uses today, and the maintained libraries that cover pieces it implements itself. Checked 6 October 2026.

## What it uses now

### In the page

| What | Version | From | Used for |
|---|---|---|---|
| [three.js](https://github.com/mrdoob/three.js) | r128 (2021) | cdnjs, as a global script | WebGL renderer, render targets, cameras, the moon's sphere and shader material, maths |
| Moon colour map and normal map | built once | NASA SVS [CGI Moon Kit](https://svs.gsfc.nasa.gov/4720) (LRO LROC mosaic, LOLA altimetry), public domain | `moon_albedo.jpg` and `moon_normal.jpg`, made by `tools/make_textures.py` |

Nothing else loads at runtime. The page has no npm dependencies of its own.

### To build the textures (run once, by hand)

| What | Used for |
|---|---|
| Python 3, [numpy](https://numpy.org/), [Pillow](https://python-pillow.org/) | `tools/make_textures.py`: recolours the mosaic and computes normals from the elevation |

### To serve and deploy (`package.json`, dev only)

| Package | Asked for | Installed | Latest | Notes |
|---|---|---|---|---|
| `cf` | `^1.0.0-beta.5` | 1.0.0-beta.12 | | `npm run deploy` puts the static site on a Cloudflare Worker |
| `@cloudflare/vite-plugin` | `beta` | 2.0.0-beta.sha-52b0dc0e9 | 1.63.0 (stable) | follows the `beta` tag on purpose, for `cf` |
| `vite` | `^8.3.0` | 8.3.2 | 8.3.3 | patch release available |
| `typescript` | `^7.0.2` | 7.0.2 | 7.0.2 | `npm run typecheck` of `src/index.ts` (the trailing-slash redirect) |

## Pieces it implements itself, and what could replace them

These maintained libraries cover the same ground. "Last push" and stars are from GitHub on the date above.

| What the page does itself | Library | Last push | Stars | Licence | Verdict |
|---|---|---|---|---|---|
| Everything, on three.js r128 | [three.js](https://github.com/mrdoob/three.js) r186 (0.186.1 on npm, jsDelivr and cdnjs) | 2026-10-06 | 116k | MIT | **Upgrade.** See below. |
| Ping-pong render targets stepping the wave equation (`simRT`, `simStep`) | `GPUComputationRenderer` in three.js `examples/jsm/misc` | (with three.js) | | MIT | Worth it after the upgrade. It is the same pattern in a tested helper, about 20 lines fewer. |
| The glints' bloom (bright pass, two-pass Gaussian blur, additive composite), film grain, vignette | [pmndrs/postprocessing](https://github.com/pmndrs/postprocessing) 6.39.5 (or three's `UnrealBloomPass`) | 2026-10-05 | 2.9k | Zlib | Skip for now. Our bloom blooms only the moon's image in the water (it reads the water pass's alpha), not everything bright. A library bloom would need a custom selection pass and would come out about the same size. Grain and vignette are six lines. |
| Interruptible moves between views: Hermite easing that keeps the current velocity (`ease(x, v0)`, `startTransition`) | [pmndrs/maath](https://github.com/pmndrs/math) 0.10.8 (`easing.damp3`, `dampQ`, `dampAngle`) or [yomotsu/camera-controls](https://github.com/yomotsu/camera-controls) 3.1.2 | 2026-09-30 / 2026-10-01 | 1.3k / 2.4k | MIT | Consider maath if moves become "chase a target" springs. camera-controls only moves a camera, while our moves also carry the moon, an off-centre lens, the slab and a staged turn under the surface, so it would cover a fraction. |
| GLSL hashes and value noise (`h21`, `h11`, `vnoise`), Schlick Fresnel (`transmit`), cubic B-spline texture reads (`heightAt`) | [lygia](https://github.com/patriciogonzalezvivo/lygia) 1.4.1 | 2026-09-14 | 3.5k | Prosperity / Patron (non-commercial free; commercial use needs a sponsorship) | Skip. Each function is a few lines and tuned in place. The licence is also a catch if the site is ever commercial. |
| The parameter lines (custom canvas sliders over real range inputs, hidden behind P) | [lil-gui](https://github.com/georgealways/lil-gui) 0.21.0, [Tweakpane](https://github.com/cocopon/tweakpane) 4.0.5 | 2025-10-12 / 2026-03-15 | 1.6k / 4.6k | MIT | Skip. The lines are part of the look. Tweakpane is the better choice if a separate developer panel is ever wanted. |
| The water itself: Snell's window, refraction and Fresnel from under the surface, the sea seen from above, the cut | three's `Water` / `Water2` (`examples/jsm/objects`) | (with three.js) | | MIT | No replacement. Those are reflective planes seen from above. Nothing maintained renders the view from under the surface. |

### Upgrading three.js (r128 to r186)

r128 is five years old, and newer releases have no UMD build (it was removed in r160). The upgrade means:

1. Load three as an ES module (`<script type="importmap">` pointing at jsDelivr or cdnjs `three.module.js`), and make the page script `type="module"`.
2. Colour management changed in r152 (sRGB output and colour management on by default). To keep the palette exactly as tuned, set `THREE.ColorManagement.enabled = false` and `renderer.outputColorSpace = THREE.LinearSRGBColorSpace`, then compare the screenshots.
3. Small renames: `texture.encoding` becomes `colorSpace` (not used here), `WebGLMultipleRenderTargets` becomes `WebGLRenderTarget({ count })`.

What it buys: maintained code, `GPUComputationRenderer` and multiple render targets. With those, the water pass can write the glint brightness into a second target and draw straight to the screen, which drops the copy pass added in this refactor.
