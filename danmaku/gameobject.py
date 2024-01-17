from danmaku.utils import *


class GameObject:
    def __init__(self, color, x_y, width_height, vx_vy, hp, dm, endurance):
        self.color = color
        self.x, self.y = x_y
        self.vx, self.vy = vx_vy
        self.width, self.height = width_height
        self.hp = hp
        self.dm = dm
        self.endurance = endurances
        self.direction = ""

    def update(self, delta):
        self.x += self.vx * delta
        self.y += self.vy * delta


    def shoot(self, other):
        pass

    def get_damage(self, dm):
        self.hp -= dm * self.endurance

    def draw(self, graphicss):
        pass

    def collision(self, other):
        pass
