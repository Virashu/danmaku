from vgame.graphics import Graphics, Sprite
from abc import abstractmethod

class GameObject(Sprite):
    """
    A base game entity object.
    """

    def __init__(self, color, x_y, width_height, vx_vy, hp, dm, endurance):
        self.color = color
        self.x, self.y = x_y
        self.vx, self.vy = vx_vy
        self.width, self.height = width_height
        self.hp = hp
        self.dm = dm
        self.endurance = endurance
        self.direction = ""

    def update(self, delta):
        self.x += self.vx * delta
        self.y += self.vy * delta

    @abstractmethod
    def shoot(self, other):
        ...

    def get_damage(self, dm):
        self.hp -= dm * self.endurance

    @abstractmethod
    def draw(self, graphics: Graphics):
        pass

    @abstractmethod
    def collision(self, other):
        pass
