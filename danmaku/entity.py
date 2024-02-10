"""Base class for alive objects"""

from danmaku.gameobject import GameObject


class Entity(GameObject):
    """Base class for alive objects"""

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        health: int | float,
        damage: int | float,
        endurance: int | float = 1,
    ):
        GameObject.__init__(self, xy, width_height, speed)

        self.health = health
        self.damage = damage
        self.endurance = endurance

    def get_damage(self, damage: int | float):
        """Decrease health point."""
        self.health -= damage / self.endurance