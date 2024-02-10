"""Entity's bullet declaration."""

from danmaku.gameobject import GameObject

# from danmaku.database import ...


class Drop(GameObject):
    """Bullet object."""

    def __init__(self, xy: tuple[int | float, int | float]):
        width, height = 20, 20
        speed = 10
        super().__init__(
            xy,
            (width, height),
            speed,
        )
        self.vx, self.vy = (0, 1)
        self.hitbox_radius = 10

        self.texture_file = ""
        self.texture_size = (20, 20)


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
