# 弾幕 (Danmaku)
![pylint](https://img.shields.io/badge/PyLint-9.85-yellow?logo=python&logoColor=white)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Goal
To create a bullet hell game similar to TouHou Project, Undertale, etc.

## Refactoring
- [x] main.py
- [x] bullet.py
- [x] enemy.py
- [x] gameobject.py
- [x] player.py
- [x] utils.py


## TODO
- [x] Levels
- [ ] Boss HP bar
- [x] Player HP/Bomb info
- [x] Player points info
- [x] Main menu
- [x] Leaderboard
- [x] Sounds
  - [x] Death
  - [ ] Shoot
  - [ ] Hit
- [x] Music
- [x] Graphics
  - [x] Images
  - [x] Level background
  - [ ] Effects (particles)
  - [ ] Scaling
- [x] Bullets
  - [ ] Trajectories
- [x] Enemies
- [x] Controls
  - [x] Change controls to classic (shift, z, x)
- [ ] Settings
  - [ ] DB
  - [ ] Menu interface
- [x] Make player hitbox smaller
- [x] Replace resource path strings with constants from db
- [ ]  Rework base classes
  - [ ] Reduce instance attribute count
  - [x] GameObject
  - [x] +Animated
  - [x] +Shooter
  - [ ] +Texture
- [x] Drops
  - [ ] HP (?)
  - [x] XP
  - [x] Powerups
  - [ ] Coins (?)
- [ ] Levels transition (portals?)
  - [ ] Background change
  - [ ] Enemies' texture change
- [ ] Split enemies types into classes
- [ ] Add enemy generate_drop() method
- [x] Seconds
- [ ] Make textures preload
- [x] Main menu style
  - [ ] Background
- [ ] Game switch background ol level change
- [ ] Move levels to DB
- [ ] Fullscreen
- [ ] Rework database.database
  - [ ] Dicts with hand mapping --> namedtuples