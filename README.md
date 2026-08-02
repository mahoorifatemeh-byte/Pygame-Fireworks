# Fireworks Simulation

**Course**: Computer Graphics  
**University**: Islamic Azad University Central Tehran Branch  
**Instructor**: Dr.Ghaderian  
**Semester**: Fall 2025  
**Student**: Fatemeh Mahoori

---

## Overview

A small pygame project that simulates a fireworks show — rockets, explosions, particle trails, and a starry background. There's no game logic or goal, it's just meant to look nice.

![Explosion display](demo.gif)


## What it does

- Rockets launch from random positions at the bottom of the screen and rise with gravity acting on them
- Each rocket explodes either at its peak or at a random height
- Explosions are picked randomly from a few types: sphere, heart, crackling, shell (multi-color), ring, and a slower trailing type
- Particles fade out over time, leave short trails, and occasionally throw off extra "glitter" sparks as they die
- The background has stars that twinkle slightly
- The screen isn't fully cleared each frame, so there's a light fade/streak effect behind the fireworks

## Requirements

- Python 3.8 or higher
- pygame (`pip install pygame`)

## How to run

You'll need pygame installed first:

```bash
pip install pygame
```

or (if you have the requirements file):

```bash
pip install -r requirements.txt
```

and then run the script:

```bash
python FireWorks.py
```

## Controls

- Click anywhere on the screen to launch a rocket
- Rockets also spawn automatically at random intervals

## Technical details

- Gravity & air resistance: Simple physics on each particle (vy += GRAVITY, vx *= AIR_RESISTANCE)
- Fade effect: Semi-transparent black overlay each frame ((0,0,0,20)) gives the motion trail look
- Particle trails: Each spark stores its last 5 positions and draws them with decreasing opacity
- Heart shape: Uses `x = 16 sin³(t)`, `y = 13cos(t) - 5cos(2t) - 2cos(3t) - cos(4t)`
- Star twinkling: Sine wave over time for smooth brightness changes

## Notes

- Most of the values (gravity, air resistance, particle counts, etc.) were tuned by trial and error. They're all set as constants near the top of the file, so feel free to adjust them for slower/faster/bigger fireworks
- Performance can drop if a lot of rockets explode at once, since particles aren't optimized — fine for a small project, but worth knowing
- The heart explosion is probably the most fun one to watch

## Known limitations

- Performance drops with too many particles on screen (not optimized for huge numbers)
- Particles aren't removed when they go off-screen until their lifetime ends — minor inefficiency
- Heart shape might look slightly off-center sometimes, but it's fine

## Credits
- Heart shape formula from standard parametric equations
- Fade effect technique inspired by pygame community examples
- Everything else was just trial and error
