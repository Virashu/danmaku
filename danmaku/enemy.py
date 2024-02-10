"""Enemy object declaration."""

from random import randint
from math import sin, cos, pi

from vgame.graphics import Graphics

from danmaku.animated import Animated
from danmaku.bullet import Bullet
from danmaku.database import get_enemy_type
from danmaku.shooter import Shooter


class Enemy(Shooter, Animated):
    """Enemy object."""

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        object_type: str,
        start_hp: int | float = 0,
    ):
        args = get_enemy_type(object_type)

        health = start_hp or args["hp"]

        super().__init__(
            xy,
            args["texture_size"],
            args["speed"],
            health,
            args["dm"],
            args["endurance"],
            "basic enemy bullet",
            0,
            args["shoot_v"] / 1000,
        )
        self.my_type = object_type
        self.cost = args["cost"]

        self.hitbox_radius = int(self.width / 2)

        # Animation
        frames = list(map(lambda x: f"/enemy/{x}", args["texture_file"].split(";")))
        Animated.__init__(
            self, xy, args["texture_size"], args["speed"], frames, 0, period=0.1
        )
        self.texture_size = args["texture_size"]
        self.vx, self.vy = 0, 1

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

    def draw(self, graphics: Graphics): ...
