"""Base game object."""

import math

from abc import abstractmethod

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
        speed: int | float,
    ):
        super().__init__()
        self.x, self.y = xy
        self.speed = speed
        self.width, self.height = width_height
        self.vx, self.vy = (0, 0)

    def update(self, delta: int | float):
        self.x += self.vx * delta * self.speed
        self.y += self.vy * delta * self.speed

        self.rect.centerx, self.rect.centery, self.rect.w, self.rect.h = (
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            int(self.width),
            int(self.height),
        )

    def collision(self, other) -> bool:
        """Check collision."""
        return (
            math.hypot(self.x - other.x, self.y - other.y)
            < self.hitbox_radius + other.hitbox_radius
        )

    @abstractmethod
    def draw(self, graphics: Graphics): ...
