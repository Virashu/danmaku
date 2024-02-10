"""Enemy object declaration."""

from random import randint
from math import sin, cos, pi

import pygame
from vgame.graphics import Graphics

from danmaku.bullet import Bullet
from danmaku.database import get_enemy_type
from danmaku.shooter import Shooter


class Enemy(Shooter):
    """Enemy object."""

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        object_type: str,
        start_hp: int | float = 0,
    ):
        args = get_enemy_type(object_type)

        hp = start_hp or args["hp"]

        super().__init__(
            xy,
            args["texture_size"],
            args["speed"],
            hp,
            args["dm"],
            "basic enemy bullet",
            0,
            shoot_period=args["shoot_v"] / 1000,
        )
        self.my_type = object_type
        self.cost = args["cost"]

        self.hitbox_radius = int(self.width / 2)

        self.vx, self.vy = 0, 1

        # Animation
        self.current_frame = 0
        self.last_animation_time = 0
        self.frame_duration = 100
        self.frames = tuple(
            map(lambda x: f"/enemy/{x}", args["texture_file"].split(";"))
        )
        self.texture_file = self.frames[self.current_frame]
        self.texture_size = args["texture_size"]

    def shoot(self) -> list[Bullet]:
        if self.can_shoot():
            if self.my_type == "boss":
                return self.shoot_radial()
            bullet = Bullet((self.x, self.y), self.damage, self.bullet_type)
            bullet.vx = randint(-100, 100) / 100
            bullet.vy = (1 - bullet.vx**2) ** 0.5
            return [bullet]
        return []

    def shoot_radial(self) -> list[Bullet]:
        """Shoot circle of bullets"""

        bullets = []

        a = randint(0, 359)

        for i in range(0, 360, 60):
            angle = pi * ((a + i) % 360) / 180
            bullet = Bullet((self.x, self.y), self.damage, self.bullet_type)
            bullet.vx = cos(angle)
            bullet.vy = sin(angle)
            bullets.append(bullet)
        return bullets

    def animation(self):
        """Animate sprite."""
        t = pygame.time.get_ticks()
        if t - self.last_animation_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.texture_file = self.frames[self.current_frame]
            self.last_animation_time = t

    def draw(self, graphics: Graphics): ...
