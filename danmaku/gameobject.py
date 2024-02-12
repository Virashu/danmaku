"""Base game object."""

import math

from vgame.graphics import Graphics, Sprite


class GameObject(Sprite):
    """
    A base game entity object.
    """

    hitbox_radius: int

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float = 0,
        hitbox_radius: int = 0,
        direction: tuple[int | float, int | float] = (0, 0),
    ):
        super().__init__()
        self.x, self.y = xy
        self.speed = speed
        self.width, self.height = width_height
        self.vx, self.vy = direction
        self.hitbox_radius = hitbox_radius

    def update(self, delta: int | float):
        self.x += self.vx * delta * self.speed
        self.y += self.vy * delta * self.speed

        self.rect.centerx, self.rect.centery, self.rect.w, self.rect.h = (
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height),
        )

    def collision(self, other) -> bool:
        """Check collision."""
        return (
            math.hypot(self.x - other.x, self.y - other.y)
            < self.hitbox_radius + other.hitbox_radius
        )

    def draw(self, graphics: Graphics):
        graphics.draw_sprite(self)
