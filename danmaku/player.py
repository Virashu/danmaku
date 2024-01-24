import pygame
import vgame
from gameobject import GameObject
from bullet import Bullet


class Player(GameObject):
    def __init__(
        self,
        color: tuple[int, int, int],
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        hp: int | float,
        damage: int | float,
        endurance: int | float,
    ):
        super().__init__(
            color,
            xy,
            width_height,
            speed,
            hp,
            damage,
            endurance,
        )

        self.texture_file = "player.png"
        self.texture_size = width_height

    def draw(self, graphics: vgame.graphics.Graphics):
        graphics.rectangle((self.x, self.y), (self.width, self.height), self.color)

    def shoot(self, bullets: list[Bullet]):
        b = Bullet(
            False,
            (125, 125, 3),
            (self.x + (self.width // 2), self.y + (self.height // 2)),
            10,
            150,
            (0, -1),
            self.damage,
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
