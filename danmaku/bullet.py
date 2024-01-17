import vgame

from .utils import *


class Bullet:
    def __init__(self, enemy, color, x_y, r, vx_vy, dm):
        self.enemy = enemy
        self.color = color
        self.x, self.y = x_y
        self.vx, self.vy = vx_vy
        self.r = r
        self.dm = dm
        self.direction = ""

    def draw(self, graphics: vgame.Graphics):
        graphics.circle((self.x, self.y), self.r, self.color)

    def update(self, delta):
        self.x += self.vx * delta
        self.y += self.vy * delta
