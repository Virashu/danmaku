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
        hp: int | float,
        damage: int | float,
    ):
        super().__init__()
        self.x, self.y = xy
        self.speed = speed
        self.width, self.height = width_height
        self.hp = hp
        self.damage = damage
        self.vx, self.vy = (0, 0)

    def update(self, delta: int | float):
        self.x += self.vx * delta * self.speed
        self.y += self.vy * delta * self.speed

        self.rect.x, self.rect.y, self.rect.w, self.rect.h = (
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            int(self.width),
            int(self.height),
        )

    def get_damage(self, damage: int | float):
        """Decrease health point."""
        self.hp -= damage

    @abstractmethod
    def shoot(self) -> list:
        """Generate bullets."""

    @abstractmethod
    def draw(self, graphics: Graphics): ...

    def collision(self, other) -> bool:
        """Check collision."""
        # other_rect = pygame.Rect(
        #     other.x - other.hitbox_radius,
        #     other.y - other.hitbox_radius,
        #     other.hitbox_radius * 2,
        #     other.hitbox_radius * 2,
        # )
        # self_rect = pygame.Rect(
        #     self.x - self.hitbox_radius,
        #     self.y - self.hitbox_radius,
        #     self.hitbox_radius * 2,
        #     self.hitbox_radius * 2,
        # )
        # res = other_rect.colliderect(self_rect)
        res = (
            math.hypot(self.x - other.x, self.y - other.y)
            < self.hitbox_radius + other.hitbox_radius
        )
        return res
