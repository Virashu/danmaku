import pygame
import vgame
from danmaku.gameobject import GameObject
from danmaku.bullet import Bullet
from database import get_player_type


class Player(GameObject):
    def __init__(
        self,
        xy: tuple[int | float, int | float],
        type, updated_hp=0
    ):
        args = get_player_type(type)
        if updated_hp == 0:
            hp = args["hp"]
        else:
            hp = updated_hp
        super().__init__(
            xy,
            args["texture_size"],
            args["speed"],
            hp,
            args["dm"],
            args["endurance"],
        )

        self.texture_file = args["texture_file"]
        self.texture_size = args["texture_size"]
        self.my_type = type

    """def draw(self, graphics: vgame.graphics.Graphics):
        graphics.rectangle((self.x, self.y), (self.width, self.height), self.color)"""

    def shoot(self, bullets: list[Bullet]):
        b = Bullet(
            (self.x + (self.width // 2), self.y + (self.height // 2)),
            self.damage,
            "basic player bullet"
        )
        bullets.append(b)

    def collision(self, other):
        if other.enemy:
            e = pygame.Rect(
                other.x - other.r, other.y - other.r, 2 * other.r, 2 * other.r
            )
            s = pygame.Rect(self.x, self.y, self.width, self.height)
            if e.colliderect(s):
                return True
