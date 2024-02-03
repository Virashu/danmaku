"""Player object declaration."""

import pygame
import vgame
from danmaku.gameobject import GameObject
from danmaku.bullet import Bullet
from danmaku.database import get_player_type


class Player(GameObject):
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
        )

        files = args["texture_file"].split(";")
        self.textures = {"left": [], "right": [], "up": [], "down": [], "shoot": []}
        for i in files:
            if "left" in i:
                self.textures["left"].append(f"/player/{i}")
            if "right" in i:
                self.textures["right"].append(f"/player/{i}")
            if "up" in i:
                self.textures["up"].append(f"/player/{i}")
            if "down" in i:
                self.textures["down"].append(f"/player/{i}")
            if "shoot" in i:
                self.textures["shoot"].append(f"/player/{i}")
        self.last_animation = 0
        self.texture_file = self.textures["left"][self.last_animation]
        self.texture_size = args["texture_size"]
        self.my_type = object_type
        self.animation_v = 100
        self.last_animation_time = 0
        self.last_shoot = 0
        self.shoot_v = args["shoot_v"]
        self.score = 0

    def shoot(self) -> list[Bullet]:
        t = pygame.time.get_ticks()
        if t - self.last_shoot >= self.shoot_v:
            bullet = Bullet(
                (self.x + (self.width // 2), self.y + (self.height // 2)),
                self.damage,
                "basic player bullet",
            )
            self.last_shoot = t
            return [bullet]
        return []

    def animation(self) -> None:
        """Animate one frame."""
        t = pygame.time.get_ticks()
        if t - self.last_animation_time >= self.animation_v:
            self.last_animation += 1
            direction = 0
            if self.vx > 0:
                direction = "right"
            elif self.vy > 0:
                direction = "down"
            elif self.vx < 0:
                direction = "left"
            elif self.vy < 0:
                direction = "up"
            if direction != 0:
                if self.last_animation >= len(self.textures[direction]):
                    self.last_animation = 0
                self.texture_file = self.textures[direction][self.last_animation]
                self.last_animation_time = t

    def draw(self, graphics: vgame.graphics.Graphics) -> None:
        graphics.draw_sprite(self)

    def collision(self, other) -> bool:
        if other.enemy:
            e = pygame.Rect(
                other.x - other.r, other.y - other.r, 2 * other.r, 2 * other.r
            )
            s = pygame.Rect(self.x, self.y, self.width, self.height)
            if e.colliderect(s):
                return True
        return False
