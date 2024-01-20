import pygame
import vgame
from danmaku.gameobject import GameObject
from danmaku.bullet import Bullet


class Player(GameObject):
    def draw(self, graphics: vgame.graphics.Graphics):
        graphics.rectangle((self.x, self.y), (self.width, self.height), self.color)

    def shoot(self, bullets: list[Bullet]):
        b = Bullet(
            False,
            (125, 125, 3),
            (self.x + (self.width // 2), self.y + (self.height // 2)),
            10,
            150,
            (0, 1),
            self.damage,
        )
        b.direction = "up"
        bullets.append(b)

    def collision(self, other):
        if other.enemy:
            e = pygame.Rect(
                other.x - other.r, other.y - other.r, 2 * other.r, 2 * other.r
            )
            s = pygame.Rect(self.x, self.y, self.width, self.height)
            if e.colliderect(s):
                return True
