from vgame.graphics import Graphics
from gameobject import GameObject
from bullet import Bullet
from database import get_bullet_type, get_enemy_type
import pygame


class Enemy(GameObject):
    def __init__(self, color, xy, type):
        args = get_enemy_type(type)
        super().__init__(color, xy, args[1], args[2], args[4], args[5], args[6])
        self.shoot_v = args[3]
        self.last_shoot = 0
        self.texture_file = args[0]
        self.texture_size = args[1]
        self.my_type = type

    def shoot(self, bullets: list[Bullet]):
        t = pygame.time.get_ticks()
        if t - self.last_shoot >= self.shoot_v:
            b = Bullet(
                True,
                (225, 125, 3),
                (self.x + self.width // 2, self.y),
                150,
                self.damage,
                "basic enemy bullet"
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
