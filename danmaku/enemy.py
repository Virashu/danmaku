from vgame.graphics import Graphics
from database import get_enemy_type
from danmaku.gameobject import GameObject
from danmaku.bullet import Bullet
import pygame


class Enemy(GameObject):
    def __init__(self, xy, type, updated_hp=0):
        args = get_enemy_type(type)
        if updated_hp == 0:
            hp = args["hp"]
        else:
            hp = updated_hp
        super().__init__(xy, args["texture_size"], args["speed"], hp, args["dm"], args["endurance"])
        self.shoot_v = args["shoot_v"]
        self.last_shoot = 0
        self.texture_file = args["texture_file"]
        self.texture_size = args["texture_size"]
        self.my_type = type

    def shoot(self, bullets: list[Bullet]):
        t = pygame.time.get_ticks()
        if t - self.last_shoot >= self.shoot_v:
            b = Bullet(
                (self.x + self.width // 2, self.y),
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
