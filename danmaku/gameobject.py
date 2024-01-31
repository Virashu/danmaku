from vgame.graphics import Graphics, Sprite
from abc import abstractmethod


class GameObject(Sprite):
    """
    A base game entity object.
    """

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        hp: int | float,
        damage: int | float,
        endurance: int | float,
    ):
        super().__init__()
        self.x, self.y = xy
        self.speed = speed
        self.width, self.height = width_height
        self.hp = hp
        self.damage = damage
        self.endurance = endurance
        self.vx, self.vy = (0, 1)

    def update(self, delta: int | float):
        self.x += self.vx * delta * self.speed
        self.y += self.vy * delta * self.speed
        self.rect.x, self.rect.y, self.rect.w, self.rect.h = (
            self.x,
            self.y,
            self.width,
            self.height,
        )

    def get_damage(self, damage: int | float):
        self.hp -= damage * self.endurance

    @abstractmethod
    def shoot(self):
        ...

    @abstractmethod
    def draw(self, graphics: Graphics):
        ...

    @abstractmethod
    def collision(self, other):
        ...
