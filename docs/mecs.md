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
