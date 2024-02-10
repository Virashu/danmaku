"""Entity's bullet declaration."""

import vgame

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

    def update(self, delta: int | float):
        self.x += self.vx * delta * self.speed
        self.y += self.vy * delta * self.speed

        self.rect.centerx, self.rect.centery, self.rect.w, self.rect.h = (
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height),
        )

    def draw(self, graphics: vgame.graphics.Graphics):
        graphics.draw_sprite(self)

    def shoot(self) -> list:
        # bruh...
        # Need to rewrite and split GameObject into 2 classes (GameObject, Shooter)
        # TODO
        ...


class PowerUp(Drop):
    def __init__(self, xy: tuple[int | float, int | float]):
        super().__init__(xy)

        self.texture_file = "powerup.png"


class Points(Drop):
    def __init__(self, xy: tuple[int | float, int | float]):
        super().__init__(xy)

        self.texture_file = "xp.png"
