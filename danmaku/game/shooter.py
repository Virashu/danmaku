"""Base class for shooting objects."""

from abc import abstractmethod

import pygame

from danmaku.game.entity import Entity
from danmaku.game.bullet import Bullet
from danmaku.database import get_settings
from danmaku.utils import resource_path


class Shooter(Entity):
    """Base class for shooting objects.

    Args:
        xy (tuple[int | float, int | float]): Position of the object.
        width_height (tuple[int | float, int | float]): Width and height of the object.
        speed (int | float): Speed of the object.
        health (int | float): Health of the object.
        damage (int | float): Damage of the object.
        shoot_freq (int | float): Maximum frequency of bullets (per second).
        shoot_period (int | float | None, optional): Time between shots. Defaults to None.

        You can pass shoot_freq as '0' and just use shoot_period

    """

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        health: int | float,
        damage: int | float,
        endurance: int | float,
        bullet_type: str,
        shoot_freq: int | float,
        shoot_period: int | float | None = None,
        **kwargs,
    ):
        super().__init__(xy, width_height, speed, health, damage, endurance, **kwargs)
        self.bullet_type = bullet_type

        if shoot_period is not None:
            self.shoot_freq = 1 / shoot_period
            self.shoot_period = shoot_period
        else:
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

    def shoot_sound(self, channel: int):
        """Play sound of shooting"""
        pygame.mixer.init()
        sound = pygame.mixer.Sound(resource_path("sounds/shoot.wav"))
        sound.set_volume(get_settings()["sfx_volume"]["value"] / 100)
        pygame.mixer.Channel(channel).play(sound)

    @abstractmethod
    def shoot(self) -> list[Bullet]:
        """Generate bullets."""
