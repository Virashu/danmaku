"""Entity's bullet declaration."""

from danmaku.entity import Entity
from danmaku.database import get_bullet_type


class Bullet(Entity):
    """Bullet object."""

    def __init__(
        self, xy: tuple[int | float, int | float], damage: int | float, object_type
    ):
        args = get_bullet_type(object_type)
        super().__init__(
            xy,
            (args["texture_size"][0], args["texture_size"][1]),
            args["speed"],
            0,
            damage,
        )
        self.enemy = args["enemy"]
        self.vx, self.vy = args["vx_vy"]
        self.hitbox_radius = args["hitbox_radius"]

        self.texture_file = args["texture_file"]
        self.texture_size = args["texture_size"]
        self.my_type = object_type
