import vgame
from vgame import Keys

from danmaku.utils import not_in_border
from danmaku.enemy import Enemy
from danmaku.player import Player


WIDTH, HEIGHT = 300, 500


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Game(vgame.Game):
    def load(self):
        self.bullets = []
        self.enemies = [
            Enemy((255, 0, 0), (100, 0), (50, 25), 30, 1500, 30, 50, 0.1),
            Enemy((255, 0, 0), (200, 100), (50, 25), 30, 1500, 30, 50, 0.1),
        ]
        self.player = Player((0, 125, 255), (100, 460), (50, 30), 500, 300, 100, 1)

    def update(self):
        vx = vy = 0
        if Keys.RIGHT in self.pressed_keys:
            vx += 1
        if Keys.LEFT in self.pressed_keys:
            vx -= 1
        if Keys.UP in self.pressed_keys:
            vy -= 1
        if Keys.DOWN in self.pressed_keys:
            vy += 1
        if Keys.SPACE in self.pressed_keys:
            self.player.shoot(self.bullets)
        self.player.vx, self.player.vy = vx, vy

        if not_in_border(
            self.player.x, self.player.y, self.player.vx, self.player.vy, WIDTH, HEIGHT
        ):
            self.player.update(self.delta)

        for enemy in self.enemies:
            enemy.shoot(self.bullets)
            enemy.update(self.delta)
            if not not_in_border(enemy.x, enemy.y, enemy.vx, enemy.vy, WIDTH, HEIGHT):
                self.enemies.remove(enemy)

        dell = []
        for bullet in self.bullets:
            if self.player.collision(bullet):
                self.player.get_damage(bullet.dm)
                dell.append(bullet)
            for enemy in self.enemies:
                if enemy.collision(bullet):
                    enemy.get_damage(bullet.dm)
                    dell.append(bullet)
                    if enemy.hp <= 0:
                        self.enemies.remove(enemy)
            bullet.update(self.delta)
            bullet.draw(self.graphics)
            if not not_in_border(
                bullet.x, bullet.y, bullet.vx, bullet.vy, WIDTH, HEIGHT
            ) or not not_in_border(
                bullet.x, bullet.y, bullet.vx, bullet.vy, WIDTH, HEIGHT
            ):
                dell.append(bullet)
        for i in dell:
            self.bullets.remove(i)

        if self.player.hp <= 0:
            quit()

    def draw(self):
        self.player.draw(self.graphics)

        for enemy in self.enemies:
            enemy.draw(self.graphics)

    def exit(self):
        ...


vgame.Run(Game(framerate=60, width=WIDTH, height=HEIGHT))
