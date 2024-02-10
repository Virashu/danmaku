"""Base class for shooting objects."""

import pygame
import vgame

from danmaku.gameobject import GameObject
from danmaku.bullet import Bullet


class Shooter(GameObject):
    """Base class for shooting objects.

    Args:
        xy (tuple[int | float, int | float]): Position of the object.
        width_height (tuple[int | float, int | float]): Width and height of the object.
        speed (int | float): Speed of the object.
        health (int | float): Health of the object.
        damage (int | float): Damage of the object.
        shoot_freq (int | float): Maximum frequency of bullets (per second).

    """

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        health: int | float,
        damage: int | float,
        shoot_freq: int | float,
        bullet_type: str,
    ):
        super().__init__(xy, width_height, speed, health, damage)
        self.bullet_type = bullet_type
        self.shoot_freq = shoot_freq
        self.shoot_period = 1 / self.shoot_freq
        self.last_shot = 0  # seconds

    def can_shoot(self) -> bool:
        """Check if it's time to shoot.

        Resets the timer if successful."""
        time = pygame.time.get_ticks() / 1000
        if time - self.last_shot >= self.shoot_period:
            self.last_shot = time
            return True
        return False

    def shoot(self) -> list[Bullet]: ...
    def update(self, delta: int | float): ...
    def draw(self, graphics: vgame.graphics.Graphics): ...
