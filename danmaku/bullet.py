import vgame


from danmaku.gameobject import GameObject


class Bullet(GameObject):
    def __init__(
        self,
        enemy: bool,
        color: tuple[int, int, int],
        xy: tuple[int | float, int | float],
        r: int | float,
        speed: int | float,
        vx_vy: tuple[int | float, int | float],
        damage: int | float,
    ):
        super().__init__(color, xy, (2 * r, 2 * r), speed, 0, damage, 1)
        self.enemy = enemy
        self.vx, self.vy = vx_vy
        self.r = r

    def draw(self, graphics: vgame.graphics.Graphics):
        graphics.circle((self.x, self.y), self.r, self.color)

    def update(self, delta):
        self.x += self.vx * delta * self.speed
        self.y += self.vy * delta * self.speed
