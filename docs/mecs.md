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

  A -->B
  B -->A

  A -->C
  C -->A
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
  GameObject <-- Shooter
  Shooter <-- Enemy
  Shooter <-- Player
  GameObject <-- Bullet
  Animated <-- Player
  Animated <-- Enemy
  Sprite <-- Animated
  Animated <--Background
  GameObject <.. Background

  class Sprite {
    str texture_file
    str texture_size
    Rect rect
  }
  class GameObject {
    int x
    int y
    int health
    int damage
    update()
    draw()
    get_damage()
    collision()
  }
  class Shooter {
    float shoot_freq
    float last_shot
    shoot()
  }
  class Player {
    int score
    int power
  }
  class Enemy {
    int cost
    type
  }
  class Animated {
    list[str] frames
    int current_frame
    float fps
    animate()
  }
  class Bullet {
    
  }
  class Background {

  }
```