"""Enemy object declaration."""

from random import randint, choices
from math import sin, cos, pi

from danmaku.game.animated import AnimatedDirectional
from danmaku.game.bullet import Bullet
from danmaku.database import get_enemy_type
from danmaku.game.shooter import Shooter
from danmaku.game.drop import PowerUp, Points, Drop


class Enemy(Shooter, AnimatedDirectional):
    """Enemy object."""

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        object_type: str,
        start_hp: int | float = 0,
    ):
        args = get_enemy_type(object_type)

        health: int | float = start_hp or args["hp"]

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
            hitbox_radius=args["texture_size"][0] // 2,
            direction=(0, 1),
        )

        frames = list(map(lambda x: f"/enemy/{x}", args["texture_file"].split(";")))
        AnimatedDirectional.__init__(
            self,
            xy,
            args["texture_size"],
            args["speed"],
            frames,
            period=0.1,
        )
        self.texture_size = args["texture_size"]
        self.my_type = object_type
        self.cost: int = args["cost"]

        self.vx, self.vy = 0, 1

    def shoot(self) -> list[Bullet]:
        if self.can_shoot():
            match self.my_type:
                case "boss":
                    if randint(0, 6) == 0:
                        return self.shoot_cluster()
                    return self.shoot_radial(waves=2, base_angle=randint(0, 359))
                case "basic enemy":
                    self.shoot_sound(2)
                    bullet = Bullet((self.x, self.y), self.damage, self.bullet_type)
                    bullet.vx = randint(-100, 100) / 100
                    bullet.vy = (1 - bullet.vx**2) ** 0.5
                    return [bullet]
                case "strong enemy":
                    return self.shoot_radial(waves=3, n=5, base_angle=randint(0, 359))
                case _:
                    pass
        return []

    def shoot_radial(
        self, base_angle: int = 0, angle_step: int = 0, waves: int = 1, n: int = 6
    ) -> list[Bullet]:
        """Shoot circle of bullets"""

        bullets: list[Bullet] = []

        for wave in range(waves):
            first_angle = base_angle + wave * angle_step
            for add_angle in range(0, 360, 360 // n):
                angle = pi * ((first_angle + add_angle) % 360) / 180
                bullet = Bullet((self.x, self.y), self.damage, self.bullet_type)
                bullet.vx = cos(angle)
                bullet.vy = sin(angle)
                for _ in range(wave):
                    bullet.update(0.3)
                bullets.append(bullet)
        return bullets

    def shoot_cluster(
        self, waves: int = 1, n: int = 10, base_angle: int = 0, arc: int = 180
    ) -> list[Bullet]:
        """Shoot spiral wave of bullets"""
        bullets: list[Bullet] = []
        for wave in range(waves):
            for i, a in enumerate(range(0, arc, arc // n)):
                angle = pi * ((base_angle + a) % 360) / 180
                bullet = Bullet((self.x, self.y), self.damage, self.bullet_type)
                bullet.vx = cos(angle) * (i + 1) * 0.2
                bullet.vy = sin(angle) * (i + 1) * 0.2
                for _ in range(wave):
                    bullet.update(0.3)
                bullets.append(bullet)
        return bullets

    def generate_drops(self) -> list[Drop]:
        """Generate drops"""
        drops: list[Drop] = []
        count = 1
        if self.my_type == "boss":
            count = 5
        for _ in range(count):
            pos = (self.x + randint(-10, 10), self.y + randint(-10, 10))
            match choices(("powerup", "points", None), (1, 1, 2))[0]:
                case "powerup":
                    drops.append(PowerUp(pos))
                case "points":
                    drops.append(Points(pos))
                case _:
                    pass

        return drops
