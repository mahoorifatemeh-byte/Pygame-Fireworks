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

- Python 3
- pygame (`pip install pygame`)

## How to run

You'll need pygame installed first:

```bash
pip install pygame
```

and then:

```bash
python FireWorks.py
```

## Controls

- Click anywhere on the screen to launch a rocket
- Rockets also spawn automatically at random intervals

## Notes

- Most of the values (gravity, air resistance, particle counts, etc.) were tuned by trial and error. They're all set as constants near the top of the file, so feel free to adjust them for slower/faster/bigger fireworks
- Performance can drop if a lot of rockets explode at once, since particles aren't optimized — fine for a small project, but worth knowing
- The heart explosion is probably the most fun one to watch
