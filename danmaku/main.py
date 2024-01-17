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
            Enemy((255, 0, 0), (100, 0), (50, 25), "down", (30, 30), 1500, 30, 50, 0.1),
            Enemy(
                (255, 0, 0), (200, 100), (50, 25), "down", (30, 30), 1500, 30, 50, 0.1
            ),
        ]
        self.player = Player(
            (0, 125, 255), (100, 460), (50, 30), (250, 250), 300, 100, 1
        )

    def update(self):
        if Keys.RIGHT in self.pressed_keys:
            self.player.vx += 1
        if Keys.LEFT in self.pressed_keys:
            self.player.vx -= 1
        if Keys.UP in self.pressed_keys:
            self.player.vy -= 1
        if Keys.DOWN in self.pressed_keys:
            self.player.vy += 1
        if Keys.SPACE in self.pressed_keys:
            self.player.shoot(self.bullets)

        if not_in_border(
            self.player.x, self.player.y, self.player.direction, WIDTH, HEIGHT
        ):
            self.player.update(self.delta)

        for enemy in self.enemies:
            enemy.shoot(self.bullets)
            enemy.update(self.delta)
            if not not_in_border(enemy.x, enemy.y, "down", WIDTH, HEIGHT):
                self.enemies.pop(self.enemies.index(enemy))

        ###################################
        ###################################
        ###################################
        ###################################
        ###################################

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
                        self.enemies.pop(self.enemies.index(enemy))
            bullet.update(self.delta)
            bullet.draw(self.graphics)
            if not not_in_border(
                bullet.x, bullet.y, "down", WIDTH, HEIGHT
            ) or not not_in_border(bullet.x, bullet.y, "up", WIDTH, HEIGHT):
                dell.append(bullet)
        for i in dell:
            self.bullets.pop(self.bullets.index(i))

        if self.player.hp <= 0:
            quit()

    def draw(self):
        self.player.draw(self.graphics)

        for enemy in self.enemies:
            enemy.draw(self.graphics)

    def exit(self):
        ...


vgame.Run(Game(framerate=60, width=WIDTH, height=HEIGHT))
