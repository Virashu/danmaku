"""Entity's bullet declaration."""

import vgame

from danmaku.gameobject import GameObject
from danmaku.database import get_bullet_type


class Bullet(GameObject):
    """Bullet object."""

    def __init__(
        self, xy: tuple[int | float, int | float], damage: int | float, object_type
    ):
        args = get_bullet_type(object_type)
        super().__init__(
            xy, (2 * args["radius"], 2 * args["radius"]), args["speed"], 0, damage, 1
        )
        self.enemy = args["enemy"]
        self.vx, self.vy = args["vx_vy"]
        self.radius = args["radius"]
        self.hitbox_radius = self.radius

        self.texture_file = args["texture_file"]
        self.texture_size = (2 * self.radius, 2 * self.radius)
        self.my_type = object_type

    def update(self, delta: int | float):
        self.x += self.vx * delta * self.speed
        self.y += self.vy * delta * self.speed

        self.rect.x, self.rect.y, self.rect.w, self.rect.h = (
            int(self.x - self.radius),
            int(self.y - self.radius),
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
