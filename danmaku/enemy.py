from vgame.graphics import Graphics
from gameobject import GameObject
from bullet import Bullet
import pygame


class Enemy(GameObject):
    def __init__(self, color, xy, width_height, speed, shoot_v, hp, dm, endurance):
        super().__init__(color, xy, width_height, speed, hp, dm, endurance)
        self.shoot_v = shoot_v
        self.last_shoot = 0

    def draw(self, graphics: Graphics):
        graphics.polygon(
            [
                (self.x, self.y),
                (self.x + (self.width // 2), self.y - self.height * 2),
                (self.x - (self.width // 2), self.y - self.height * 2),
            ],
            self.color,
        )

    def shoot(self, bullets: list[Bullet]):
        t = pygame.time.get_ticks()
        if t - self.last_shoot >= self.shoot_v:
            b = Bullet(
                True,
                (225, 125, 3),
                (self.x, self.y),
                10,
                150,
                (0, 1),
                self.damage,
            )
            b.direction = "down"
            bullets.append(b)
            self.last_shoot = t

    def collision(self, other):
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
