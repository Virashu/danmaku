"""Player object declaration."""

import math
import vgame
from danmaku.game.bullet import Bullet
from danmaku.database import get_player_type
from danmaku.utils import constrain
from danmaku.game.shooter import Shooter
from danmaku.game.animated import Animated


class Player(Shooter, Animated):
    """Player object."""

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        object_type: str,
        bombs:int=0,
        lives:int=1,
        updated_hp:int=0,
    ) -> None:
        args = get_player_type(object_type)

        health:int|float = updated_hp or args["hp"] * lives

        super().__init__(
            xy,
            args["texture_size"],
            args["speed"],
            health,
            args["dm"],
            args["endurance"],
            "basic player bullet",
            0,
            args["shoot_v"] / 1000,
        )

        # Animation

        Animated.__init__(
            self, xy, args["texture_size"], args["speed"], [], 0, period=0.1
        )
        self.frames_from_str(args["texture_file"], "player")

        self.texture_size = args["texture_size"]

        self.my_type = object_type
        self.score: int = 0
        self.power: int = 1
        self.bombs = bombs

        self.hitbox_radius = args["hitbox_radius"]
        self.slow = False

        # Bounds
        self.left = self.top = 0
        self.right = self.bottom = 10e6

    def shoot(self) -> list[Bullet]:
        self.shoot_sound(1)
        res: list[Bullet] = []

        if self.can_shoot():

            bullet = Bullet(
                (self.x, self.y),
                self.damage + self.power,
                self.bullet_type,
            )

            res.append(bullet)

            if self.power > 4:
                vx = math.cos(math.pi * 85 / 180)
                vy = -math.sin(math.pi * 85 / 180)

                b1 = Bullet(
                    (self.x, self.y),
                    self.damage + self.power,
                    self.bullet_type,
                )
                b2 = Bullet(
                    (self.x, self.y),
                    self.damage + self.power,
                    self.bullet_type,
                )
                b1.vx = vx
                b2.vx = -vx
                b1.vy = b2.vy = vy
                res.extend([b1, b2])

        return res

    def bomb(self) -> list[Bullet]:
        """Spawn bomb, AKA super-bullet"""
        self.shoot_sound(1)
        res: list[Bullet] = []
        if self.bombs != 0:
            if self.can_shoot():
                bullet = Bullet(
                    (self.x, self.y),
                    (self.damage + self.power) * 30,
                    "player bomb",
                )
                res.append(bullet)
                self.bombs -= 1
        return res

    def set_bounds(
        self,
        left: int | float,
        top: int | float,
        right: int | float,
        bottom: int | float,
    ) -> None:
        """Set movement bounds"""
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def update(self, delta: int | float) -> None:
        speed = self.speed if not self.slow else self.speed * 0.5

        self.x += self.vx * delta * speed
        self.x = constrain(
            self.x, self.left + self.width / 2, self.right - self.width / 2
        )

        self.y += self.vy * delta * speed
        self.y = constrain(
            self.y, self.top + self.height / 2, self.bottom - self.height / 2
        )

        self.rect.centerx, self.rect.centery, self.rect.w, self.rect.h = (
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height),
        )

    def draw(self, graphics: vgame.graphics.Graphics) -> None:
        graphics.draw_sprite(self)
        if self.slow:
            graphics.circle((self.x, self.y), self.hitbox_radius, (200, 0, 200))
