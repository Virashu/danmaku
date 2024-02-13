# 弾幕 (Danmaku)
![pylint](https://img.shields.io/badge/PyLint-9.63-yellow?logo=python&logoColor=white)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Goal
To create a bullet hell game similar to TouHou Project, Undertale, etc.

## How to build

```
poetry shell
poetry install
```
or
```
python3 -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade -r .\requirements.txt
```
Then,
```
.\build
```

## For developers

Most important things is written down [here](./docs/mecs.md)

## Refactoring
- [x] main.py
- [x] bullet.py
- [x] enemy.py
- [x] gameobject.py
- [x] player.py
- [x] utils.py


## TODO

- [x] Game mechanics
  - [x] Drops
      - [ ] HP (?)
    - [x] XP
    - [x] Powerups
    - [ ] Coins (?)
  - [x] Bullets
    - [ ] Trajectories
  - [x] Enemies
  - [x] Controls
    - [x] Change controls to classic (shift, z, x)
  - [x] Levels
  - [x] Make player hitbox smaller
  - [ ] Levels transition (portals?)
    - [ ] Background change
    - [ ] Enemies' texture change
- [x] Graphics
  - [x] Images
  - [x] Level background
  - [ ] Effects (particles)
  - [ ] Scaling
  - [ ] Fullscreen
  - [ ] Boss HP bar
  - [x] Player HP/Bomb info
  - [x] Player points info
  - [ ] UI
    - [x] Main menu
      - [x] Main menu style
      - [ ] Background
    - [x] Leaderboard
    - [x] Settings
      - [x] DB
      - [x] Menu interface
  - [ ] Make textures preload
- [x] Code
  - [x] Rework base classes
    - [x] Reduce instance attribute count
    - [x] GameObject
    - [x] +Animated
    - [x] +Shooter
    - [ ] +Texture
  - [ ] Split enemies types into classes
  - [x] Add enemy generate_drop() method
  - [x] Seconds
  - [ ] Move levels to DB
  - [ ] Rework database.database
    - [ ] Dicts with hand mapping --> namedtuples
  - [x] Replace resource path strings with constants from db
- [x] Sounds
  - [x] Death
  - [ ] Shoot
  - [ ] Hit
- [x] Music
