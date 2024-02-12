"""Entity's bullet declaration."""

from danmaku.gameobject import GameObject

# from danmaku.database import ...


class Drop(GameObject):
    """Bullet object."""

    def __init__(self, xy: tuple[int | float, int | float]):
        size = 20, 20
        super().__init__(xy, size, speed=20, hitbox_radius=10, direction=(0, 1))
        self.texture_file = ""
        self.texture_size = size


class PowerUp(Drop):
    """Player's powerup

    Should increase player's damage"""

    def __init__(self, xy: tuple[int | float, int | float]):
        super().__init__(xy)

        self.texture_file = "powerup.png"


class Points(Drop):
    """Player's score drop"""

    def __init__(self, xy: tuple[int | float, int | float]):
        super().__init__(xy)

        self.texture_file = "xp.png"
