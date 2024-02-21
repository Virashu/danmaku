"""Base class for alive objects"""

import pygame

from danmaku.database import get_settings
from danmaku.game.gameobject import GameObject
from danmaku.utils import resource_path


class Entity(GameObject):
    """Base class for alive objects"""

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        health: int | float,
        damage: int | float,
        endurance: int | float = 1,
        **kwargs,
    ):
        GameObject.__init__(self, xy, width_height, speed, **kwargs)

        self.health = health
        self.damage = damage
        self.endurance = endurance

    def get_damage(self, damage: int | float):
        """Decrease health point."""
        self.health -= damage / self.endurance
        self.damage_sound(3)

    def damage_sound(self, channel: int):
        """Play damage sound"""
        pygame.mixer.init()
        sound = pygame.mixer.Sound(resource_path("sounds/hit.wav"))
        sound.set_volume(get_settings()["sfx_volume"]["value"] / 100)
        pygame.mixer.Channel(channel).play(sound)
