"""Player object declaration."""

import math
import pygame
import vgame
from danmaku.bullet import Bullet
from danmaku.database import get_player_type
from danmaku.utils import constrain, Direction
from danmaku.shooter import Shooter


class Player(Shooter):
    """Player object."""

    def __init__(
        self, xy: tuple[int | float, int | float], object_type: str, updated_hp=0
    ) -> None:
        args = get_player_type(object_type)

        if updated_hp == 0:
            hp = args["hp"]
        else:
            hp = updated_hp
        # Can replace with:
        # hp = updated_hp or args["hp"]

        super().__init__(
            xy,
            args["texture_size"],
            args["speed"],
            hp,
            args["dm"],
            args["endurance"],
            "basic player bullet",
        )

        self.my_type = object_type
        self.score = 0
        self.power = 1

        self.last_shoot = 0
        self.shoot_v = args["shoot_v"]
        self.hitbox_radius = args["hitbox_radius"]
        self.slow = False

        # Bounds
        self.left = self.top = 0
        self.right = self.bottom = 10e6

        # Animation
        files = args["texture_file"].split(";")
        self.textures = {
            Direction.LEFT: [],
            Direction.RIGHT: [],
            Direction.UP: [],
            Direction.DOWN: [],
        }
        for i in files:
            path = f"/player/{i}"
            if "left" in i:
                self.textures[Direction.LEFT].append(path)
            if "right" in i:
                self.textures[Direction.RIGHT].append(path)
            if "up" in i:
                self.textures[Direction.UP].append(path)
            if "down" in i:
                self.textures[Direction.DOWN].append(path)

        self.current_frame = 0
        self.texture_file = self.textures[Direction.LEFT][self.current_frame]
        self.texture_size = args["texture_size"]
        self.animation_v = 100
        self.last_animation_time = 0

    def shoot(self) -> list[Bullet]:
        res: list[Bullet] = []

        if self.can_shoot():

            bullet = Bullet(
                (self.x, self.y),
                self.damage + self.power,
                self.bullet_type,
            )

            res.append(bullet)

            if self.power > 4:
                vx = math.cos(math.pi * 75 / 180)
                vy = -math.sin(math.pi * 75 / 180)

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
        res: list[Bullet] = []
        if self.can_shoot():
            bullet = Bullet(
                (self.x, self.y),
                self.damage + self.power + 50,
                "player bomb",
            )
            res.append(bullet)
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

        self.rect.x, self.rect.y, self.rect.w, self.rect.h = (
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            int(self.width),
            int(self.height),
        )

    def animation(self) -> None:
        """Animate one frame."""
        t = pygame.time.get_ticks()
        if t - self.last_animation_time >= self.animation_v:
            direction = None
            if self.vx > 0:
                direction = Direction.RIGHT
            elif self.vy > 0:
                direction = Direction.DOWN
            elif self.vx < 0:
                direction = Direction.LEFT
            elif self.vy < 0:
                direction = Direction.UP
            if direction is not None:
                self.current_frame = (self.current_frame + 1) % len(
                    self.textures[direction]
                )
                self.texture_file = self.textures[direction][self.current_frame]
                self.last_animation_time = t

    def draw(self, graphics: vgame.graphics.Graphics) -> None:
        graphics.draw_sprite(self)
        graphics.circle((self.x, self.y), self.hitbox_radius, (255, 255, 255))
