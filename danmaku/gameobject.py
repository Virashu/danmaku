from vgame.graphics import Graphics, Sprite
from abc import abstractmethod


class GameObject(Sprite):
    """
    A base game entity object.
    """

    def __init__(self, color, xy, width_height, speed, hp, dm, endurance):
        super().__init__()
        self.color = color
        self.x, self.y = xy
        self.speed = speed
        self.width, self.height = width_height
        self.hp = hp
        self.dm = dm
        self.endurance = endurance
        self.vx = self.vy = 0

    def update(self, delta):
        self.x += self.vx * delta * self.speed
        self.y += self.vy * delta * self.speed

    def get_damage(self, dm):
        self.hp -= dm * self.endurance

    @abstractmethod
    def shoot(self, other):
        ...

    @abstractmethod
    def draw(self, graphics: Graphics):
        pass

    @abstractmethod
    def collision(self, other):
        pass
