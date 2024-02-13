# Game mechanics, or how everything works (for devs)

## Structure

- danmaku (Runner)
  - Main menu (Scene)
  - Game field (Scene)
    - Player
    - Enemies


## Player movement
```
     -1
      ^
      |
-1 <- 0 -> 1
      |
      v
      1
```
Player has two axis (x, y) which vary from -1 to 1.
Player also has speed module (pixels / second).
Player's move distance calculation is (speed module) * (axis) * (time delta)


## Scenes

```mermaid
graph LR
  A(Main menu)
  B(Game)
  C(Settings)
  D(History)

  A-->|new_game|B
  B-->|win or lose|A

  A-->C
  C-->A

  A-->D
  D-->A
```

As we can see, all other scenes return to the main menu



## Position, hitboxes


Position of an object is a position of it's center point

*placement:*
```
/-----\
|     |
|  *  |
|     |
\-----/
```
(where the star is at)

**NOT** coordinates of left top corner

*wrong placement:*
```
*-----\
|     |
|     |
|     |
\-----/
```

## Classes

```mermaid
classDiagram
  Sprite <-- GameObject
  GameObject <-- Entity
  Shooter <-- Enemy
  Shooter <-- Player
  Entity <-- Bullet
  Animated <-- Player
  Animated <-- Enemy
  GameObject <-- Animated
  Animated <-- Background
  Entity <-- Shooter

  class Sprite {
    texture_file: str
    texture_size: tuple
    rect: Rect
  }
  class GameObject {
    x: int
    y: int
    update()
    draw()
    collision() -> bool
  }
  class Entity {
    health: int
    damage: int
    get_damage()
  }
  class Shooter {
    shoot_freq: float
    last_shot: float
    can_shoot() -> bool
    shoot()
  }
  class Player {
    score: int
    power: int
  }
  class Enemy {
    cost: int
  }
  class Animated {
    animation_frames: list[str]
    animation_current: int
    animation_period: float
    animate()
  }
  class Bullet {
    
  }
  class Background {

  }
```


## Enemies' actions processing
```mermaid
graph TB

A([Start])
B["Merge all actions (with links to objects)"]
C[Sort by timing]
E{Is it time yet?}
F[Execute action]
G[Remove from queue]
H{While actions left}
Z([End])

A --> B
B --> C
C --> H

subgraph LOOP
  direction TB

  D[Pick first]

  D --> E
  E --> |Yes| F
  E --> |No| D
  F --> G
end


LOOP --> H
H --> |Yes| LOOP
H --> |No| Z

```

## File hierarchy (import diagram)

```mermaid
%%{init: {"flowchart": {"curve": "basis"}} }%%
graph TB

GAME("game.py")
MAIN("main.py")


animated --> gameobject

background --> animated

bullet --> entity
bullet --> database

button

drop --> gameobject

enemy --> shooter
enemy --> database
enemy --> animated
enemy --> bullet
enemy --> drop

entity --> gameobject

GAME --> enemy
GAME --> player
GAME --> level
GAME --> database
GAME --> drop
GAME --> background
GAME --> pause
GAME --> utils
GAME --> bullet

gameobject

history --> database

level --> enemy

MAIN --> GAME
MAIN --> menu
MAIN --> settings
MAIN --> history

menu --> background
menu --> button
menu --> database
menu --> utils

pause

player --> shooter
player --> database
player --> animated
player --> bullet
player --> utils

settings --> button
settings --> database


shooter --> entity
shooter --> bullet

utils

subgraph S_UI
direction TB
end

subgraph S_GAME
direction TB
end

```



