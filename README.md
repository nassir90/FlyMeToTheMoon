# Fly Me to the Moon

Attempt at capturing the end of NEON GENESIS EVANGELION in threejs.

**Live:** [mpts.ie/games/flymetothemoon](https://mpts.ie/games/flymetothemoon/)

![The default scene, with the controls](docs/screenshots/01-default.jpg)

## Skies

| Day | Sunset | Night |
|---|---|---|
| ![Day](docs/screenshots/12-sky-day.jpg) | ![Sunset](docs/screenshots/13-sky-sunset.jpg) | ![Night](docs/screenshots/14-sky-night.jpg) |

| Midnight | Eclipse |
|---|---|
| ![Midnight](docs/screenshots/15-sky-midnight.jpg) | ![Eclipse](docs/screenshots/16-sky-eclipse.jpg) |

## Views

| Below | Below, by day |
|---|---|
| ![Below](docs/screenshots/18-moon-behind.jpg) | ![Below by day](docs/screenshots/19-moon-behind-day.jpg) |

| Cut | Above | Wide |
|---|---|---|
| ![Cut](docs/screenshots/24-cut.jpg) | ![Above](docs/screenshots/26-above.jpg) | ![Wide at sunset](docs/screenshots/29-wide-sunset.jpg) |

## Controls

Press **P** to show the sliders and **H** to hide all the controls. Tap the water to drop a ripple, drag the moon to spin it.

<img src="docs/screenshots/11-controls.jpg" alt="The controls" width="320"> <img src="docs/screenshots/10-phone.jpg" alt="On a phone at sunset" width="200">

Every control can also be set in the address, for example `?sky=sunset&view=below&murk=0`.

## Running it

```bash
npm install
npm run dev      # local dev server
```

`python tools/make_textures.py` rebuilds the moon textures from NASA's CGI Moon Kit (needs numpy and pillow).

## Credits

Moon imagery and elevation: NASA's Scientific Visualization Studio, [CGI Moon Kit](https://svs.gsfc.nasa.gov/4720), public domain.

## License

The code is [MIT](LICENSE). The moon textures are NASA imagery and stay public domain.
