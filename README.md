# Fly Me to the Moon

A full moon seen from under the water. You look up through a moving, simulated surface: the moon's reflection breaks into a glowing, wobbling orb with glints around it, the water past the edge of the window goes dark, and a large moon hangs in front of it all. You can spin the moon, drop ripples into the water, and tune the sea.

**Live:** [mpts.ie/games/flymetothemoon](https://mpts.ie/games/flymetothemoon/)

![The default scene](docs/screenshots/01-default.jpg)

## What you're looking at

### The water

The surface is a real simulation, not a painted texture:

- **Ripples.** A 512 × 512 height grid, covering 20 × 20 units of water, is stepped on the GPU with the wave equation. Ripples travel, spread, interfere and die away on their own, with a slight pull back toward level so long waves can't drift. Wind pushes on it with a fresh pattern of pressure waves in random directions every few steps, blended smoothly from one pattern to the next.
- **Broad waves.** On top of that rides a wind sea: ten long waves (0.8–3.2 units) and six short ones, all travelling within about ±30° of one direction with irregular lengths and phases. Their long crests roll across the water, and their crests and troughs brighten and darken the surface in long bands.
- **Swell.** Four long swells. Every wave, broad or long, moves at its real speed for its length (deep-water dispersion, ω² = gk).
- **No grid.** The height grid is read back with a smooth cubic B-spline filter, and its coordinates are bent by a slow, drifting warp and turned 27°, so the simulation's grid never shows in the light.
- **A soft cap.** A soft limit on the surface's total tilt leaves gentle slopes alone and compresses steep ones, so no combination of settings throws the water into extremes.

![Calm water](docs/screenshots/02-calm.jpg)

![Rough water, every slider at its maximum](docs/screenshots/03-rough.jpg)

### Looking up through it

Each pixel casts a ray up from an underwater camera, three units deep and tilted 37° up. The ray is bent out through the moving surface with Snell's law (n = 1.333) and weighted by Fresnel reflection. Past the critical angle (48.6° from straight up) it reflects back down into the dark water instead. So the edge of the bright window ripples and breaks up, the window dims toward its edge, and the moon's image breaks apart and glints, all from the optics rather than drawn shapes.

Three things keep that from looking like a bright hole cut in a flat dark ceiling:

- **Ripples too small to simulate.** Each pixel covers many tiny ripples, each tilted a little differently, so the light that gets out is averaged over a spread of angles, and the spread widens with distance. The window's edge, and the bright patches that break off it as waves tilt the surface, shade off smoothly instead of switching on and off.
- **Distance.** Light fades toward the water's own colour the further it travels through it. The surface near overhead stays clear, and toward the horizon it recedes into haze until it meets the open water, so it reads as a sheet stretching away rather than a flat wall.
- **Murk.** Particles in the water scatter light from the window toward you. The glow is strongest right at the window's edge and fades out into the dark water, with a lighter veil over the window itself.

The dark water below and the surface's mirror of it share one colour field, warm brown-black on the left and cooler on the right, with a faint, slow drift of light, so the whole frame reads as water. That light depends on direction, nearly black straight down and brighter toward the surface, so as the waves tilt the mirror it shows their shape.

![Murk at its maximum](docs/screenshots/22-murk.jpg)

![No murk: clear water](docs/screenshots/23-clear.jpg)

![Broad waves alone, rolling across the surface](docs/screenshots/04-broad-waves.jpg)

Some light also leaks into the dark water, badly scrambled. There, each ray is bent again through an exaggerated version of the surface (its real slopes amplified about six times, plus a fast jitter), so the few rays that still get out pick up warped fragments of sky, moon glow and moon. They drift through the dark water below the window's edge and fade out with depth. With the moon **Behind** the surface, the same happens to the moon itself: whatever part of it sinks below the waterline still comes through as a faint, shattered ghost, looked up at a badly scrambled position, instead of vanishing. Lower it with **Height** to see more of it. The **Leak** control sets how much gets through.

![The moon behind the water, lowered, leaking through the dark water as a shattered ghost](docs/screenshots/21-leak.jpg)

With the warp turned off, the ripples settle into a more even, cell-like pattern:

![The warp turned off](docs/screenshots/05-no-warp.jpg)

### The reflection

The moon's image in the surface is the real refraction of a moon in the sky above. The one deliberate cheat: that image is drawn a second time on top of the big moon, so the reflection sits in front of it.

A bloom makes the image glow. It's computed at quarter size, with four samples spread across each bloom pixel so thin glints add their real share of light, then blurred twice and added back.

![Bloom off](docs/screenshots/06-bloom-off.jpg)

![Glow at its maximum](docs/screenshots/07-glow.jpg)

### The moon

The moon's surface is NASA's Lunar Reconnaissance Orbiter colour mosaic, recoloured to the scene's teal palette by rank (so the real maria and ray craters stay where they are). Its normal map is computed from LRO laser altimetry. It's lit from the upper right, which leaves a shadowed crescent on the lower left, and the craters only show their relief along that terminator.

Drag the moon to spin it. Let go mid-drag to throw it; press on it while it's turning to catch it. Arrow keys spin it too, and Space stops it. Alt+drag moves it about the frame. The controls are the same in every view.

![The moon turned to show its far side](docs/screenshots/08-turned.jpg)

![A clean frame](docs/screenshots/09-clean.jpg)

### In front of or behind the water

The **In front** button sends the moon up behind the surface (it then reads **Behind**). It glides up into the bright window and shrinks, as if far above, and from then on you see it through the water: it's rendered off-screen each frame and looked up at a position bent by the surface's slope, so the waves wobble it, it dims toward the window's edge where less light gets through, and it disappears past the critical angle, where its lower edge dips into the dark water. The bright reflection fades to a faint shimmer so there aren't two moons, and the halo follows it up. You can still spin it.

![The moon behind the water at night](docs/screenshots/18-moon-behind.jpg)

![The moon behind the water by day](docs/screenshots/19-moon-behind-day.jpg)

The **Height** line raises or lowers the moon, in the water or in the sky. Lowered behind the surface, it sinks into the waterline and is cut off where the window ends. **Drift** keeps it moving: the moon travels steadily down or up through the frame, through the window and the dark water below it, and comes back in at the other edge, while the time of day stays put.

![The moon raised](docs/screenshots/20-height.jpg)

### The sky

Seven sky presets, at the top of the controls, set the time of day and the kind of moon. Every colour in the scene comes from one palette: the water on both sides, the light falling from above, the sky seen through the surface and the glow around the moon in it, the reflection and its bloom, the halo, and the moon's own tint, shadow and crater relief. Pressing a preset fades every colour across to the new look over about a second.

**Day:** a bright blue sky through the surface and teal water. The moon is washed almost white, and the glow around it all but disappears.

![Day](docs/screenshots/12-sky-day.jpg)

**Sunset:** an orange sky fading to violet overhead, warm dark water, a warm moon and a golden reflection.

![Sunset](docs/screenshots/13-sky-sunset.jpg)

**Night:** the default.

![Night](docs/screenshots/14-sky-night.jpg)

**Midnight:** near-black water and sky, a dimmer moon, and a cold, faint glow.

![Midnight](docs/screenshots/15-sky-midnight.jpg)

**Eclipse:** a blood moon. The moon turns copper-red, and its reflection glows orange against dark red water.

![Eclipse](docs/screenshots/16-sky-eclipse.jpg)

**Harvest:** a yellow full moon in a black sky, with a golden path on black water.

![Harvest](docs/screenshots/28-sky-harvest.jpg)

![Harvest, from above the water](docs/screenshots/30-above-harvest.jpg)

**Blood:** a blood moon in a black sky.

![Blood](docs/screenshots/29-sky-blood.jpg)

Halfway through the fade from Day to Sunset:

![Between day and sunset](docs/screenshots/17-sky-between.jpg)

### Cut and Above

Two more views put the moon in the sky above the water, where you can move it. Both are drawn with the scene's own code, so they show the same water: the surface is the same simulated ripples, swells and waves, the light is computed the same way, and every colour follows the sky preset.

**Cut** opens the water up and looks at it from the side. The camera's eye sits under the surface; drag it about. As everywhere, drag the moon to spin it, Alt+drag to move it, and tap the water to drop a ripple. The water is lit one of two ways (the **Eye light** / **Side light** button):

- **Eye light**: the light reaching the eye. Every direction from it glows with exactly what the scene shows the camera looking that way, so a fan of light converges on the eye: the sky through Snell's window, the moon's image as its brightest beam, and darkness past the critical angle, all moving with the waves. On the surface above, the same light draws the window as a bright circle.
- **Side light**: god rays as you'd see them from the side: moonlight refracted down into the water and gathered under the broad waves' crests, shafts with depth that fade as they go down.

![Cut, with the eye's light](docs/screenshots/24-cut.jpg)

![Cut, with god rays seen from the side](docs/screenshots/25-cut-side.jpg)

In both, the moon in the sky is the real one, the same 3D moon as in Below, with its colours, shading and spin, and its light (its beam to the eye, its glint, its path on the sea, the god rays) takes its colour under each sky: teal at night, gold at sunset, copper in the eclipse.

**Above** looks across the water from just above it. The moon hangs over the sea with its path of light broken up on the waves, and the sea meets the sky at a soft horizon: a low moon sets into it, cut by the water, with only a sliver showing through where the far water fades out. Alt+drag to move the moon; drag it to spin it.

![Above, at night](docs/screenshots/26-above.jpg)

![Above, at sunset](docs/screenshots/27-above-sunset.jpg)

## Controls

The controls sit in the lower right: the sky presets and the three views along the top, then plain white lines that reach left to line up under the first preset, solid up to the current value and blending quickly into a faint line that barely wobbles, then a row of buttons. Drag along a line, or focus it and use the arrow keys. Press **H** to hide or show the controls.

![The line controls](docs/screenshots/11-controls.jpg)

| Control | What it does | Range | Default |
|---|---|---|---|
| Day · Sunset · Night · Midnight · Eclipse · Harvest · Blood | Sky presets; pressing one fades the scene to it | | Night |
| Below · Cut · Above | The view: from under the water, the water cut open from the side, or across it from above | | Below |
| Wind | Strength of the simulated wind ripples | 0 – 1.2 | 0.45 |
| Warp | How much the height grid is bent | 0 – 2 | 1 |
| Waves | Strength of the broad wind sea | 0 – 1.2 | 0.9 |
| Swell | Strength of the long swells | 0 – 1.2 | 0.8 |
| Speed | How fast all the water moves (also slows the simulation) | 0.1 – 1.5 | 0.6 |
| Height | Raises or lowers the moon, in the water or in the sky | −1 – 1 | 0 |
| Drift | Sends the moon slowly down (left) or up (right) through the frame; once it leaves one edge it comes back in at the other. The sky stays as it is | −1 – 1 | 0 |
| Halo | Strength of the glow around the big moon (on top of what the sky sets) | 0 – 2 | 1 |
| Leak | How much scrambled light, and with the moon Behind, the moon itself, leaks into the dark water | 0 – 1 | 0.5 |
| Murk | How cloudy the water is: the glow around the window's edge and how quickly the distance fades | 0 – 1.5 | 0.7 |
| Glow | Strength of the bloom | 0 – 2 | 0.6 |
| In front / Behind | Moon in the water, or up in the sky behind the surface | | In front |
| Bloom on/off | Turns the bloom off entirely | | on |
| Eye light / Side light | In Cut: the light reaching the eye, or god rays seen from the side | | Eye light |
| Pause | Freezes the water and the moon | | |

Tap the water to drop a ripple, or drag across it to stir. In every view: drag the moon to spin it, Alt+drag to move it.

### Settings in the address

Every control can be set from the address, which is how the screenshots here were made:

```
?sky=sunset                       a look by name (day, sunset, night, midnight, eclipse, harvest, blood)
?sky=0.5                          or any point between them (0 = day ... 6 = blood), no fade
?wind=0.1&waves=0.3&swell=0.3     calm water
?wind=1.2&waves=1.2&swell=1.2     rough water
?speed=0.3                        slow motion
?moon=behind                      start with the moon behind the water
?height=1                         raise the moon (−1 lowers it)
?drift=-0.35                      the moon sinks slowly through the frame and comes back in at the top
?halo=0                           no glow around the moon
?leak=0                           no light leaking into the dark water
?murk=0                           clear water (1.5 is very cloudy)
?bloom=0                          bloom off
?turn=140                         turn the moon 140° to start
?view=cut                         the water cut open from the side (?view=above: across it from above)
?light=side                       in Cut, god rays seen from the side
?ui=0                             hide the controls
```

It works on phones too (here at sunset):

<img src="docs/screenshots/10-phone.jpg" alt="The scene on a phone at sunset" width="320">

## Running it

The site is static: everything lives in [`public/games/flymetothemoon/`](public/games/flymetothemoon/) (one `index.html` and two textures). A small Cloudflare Worker serves it at `mpts.ie/games/flymetothemoon` and redirects the bare path to the trailing-slash URL.

```bash
npm install
npm run dev      # local dev server
npm run deploy   # deploy the worker and its assets
```

It needs WebGL 2. [three.js](https://threejs.org/) r128 is loaded from cdnjs.

### Rebuilding the moon textures

[`tools/make_textures.py`](tools/make_textures.py) downloads the two source maps from NASA's CGI Moon Kit and writes `moon_albedo.jpg` and `moon_normal.jpg` next to the page:

```bash
pip install numpy pillow
python tools/make_textures.py
```

## Credits

Moon imagery and elevation: NASA's Scientific Visualization Studio, [CGI Moon Kit](https://svs.gsfc.nasa.gov/4720) (LRO LROC colour mosaic and LOLA altimetry), public domain.
