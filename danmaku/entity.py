import vgame

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
    ):
        GameObject.__init__(self, xy, width_height, speed)

        self.health = health
        self.damage = damage

    def get_damage(self, damage: int | float):
        """Decrease health point."""
        self.health -= damage

    def draw(self, graphics: vgame.graphics.Graphics): ...
