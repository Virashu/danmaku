"""Enemy object declaration."""

import pygame
from vgame.graphics import Graphics

from random import randint

from danmaku.bullet import Bullet
from danmaku.database import get_enemy_type
from danmaku.gameobject import GameObject


class Enemy(GameObject):
    """Enemy object."""

    def __init__(self, xy, object_type, updated_hp=0):
        args = get_enemy_type(object_type)
        if updated_hp == 0:
            hp = args["hp"]
        else:
            hp = updated_hp
        self.textures = []
        for i in args["texture_file"].split(";"):
            self.textures.append(f"/enemy/{i}")
        super().__init__(
            xy, args["texture_size"], args["speed"], hp, args["dm"], args["endurance"]
        )
        self.shoot_v = args["shoot_v"]
        self.last_shoot = 0
        self.last_animation = 0
        self.animation_v = 100
        self.last_animation_time = 0
        self.texture_file = self.textures[self.last_animation]
        self.texture_size = args["texture_size"]
        self.my_type = object_type
        self.cost = args["cost"]

    def shoot(self) -> list[Bullet]:
        t = pygame.time.get_ticks()
        if t - self.last_shoot >= self.shoot_v:
            bullet = Bullet(
                (self.x + self.width // 2, self.y), self.damage, "basic enemy bullet"
            )
            bullet.vx = randint(-100, 100) / 100
            bullet.vy = (1 - bullet.vx**2) ** 0.5
            self.last_shoot = t
            return [bullet]
        return []

    def animation(self):
        """Animate sprite."""
        t = pygame.time.get_ticks()
        if t - self.last_animation_time >= self.animation_v:
            self.last_animation += 1
            if self.last_animation >= len(self.textures):
                self.last_animation = 0
            self.texture_file = self.textures[self.last_animation]
            self.last_animation_time = t

    def collision(self, other) -> bool:
        if not other.enemy:
            e = pygame.Rect(
                other.x - other.r, other.y - other.r, 2 * other.r, 2 * other.r
            )
            s = pygame.Rect(
                self.x - (self.width // 2),
                self.y - self.height * 2,
                self.width,
                self.height,
            )
            if e.colliderect(s):
                return True
        return False

    def draw(self, graphics: Graphics): ...
