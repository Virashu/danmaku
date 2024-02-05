"""Base game object."""

from abc import abstractmethod

from vgame.graphics import Graphics, Sprite


class GameObject(Sprite):
    """
    A base game entity object.
    """

    hitbox_radius: int

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
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height,
        )

    def get_damage(self, damage: int | float):
        """Decrease health point."""
        self.hp -= damage * self.endurance

    @abstractmethod
    def shoot(self) -> list:
        """Generate bullets."""

    @abstractmethod
    def draw(self, graphics: Graphics): ...

    @abstractmethod
    def collision(self, other) -> bool:
        """Check collision."""
