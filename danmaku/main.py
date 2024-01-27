import vgame
from vgame import Keys
import pygame

from danmaku.utils import not_in_border, resource_path
from danmaku.enemy import Enemy
from danmaku.player import Player
from danmaku.bullet import Bullet
from danmaku.database import get_enemy_type

WIDTH, HEIGHT = 300, 500
LEVEL1 = [Enemy((25, 150, 0), (150, 15), get_enemy_type("basic enemy"))]
LEVEL2 = [
    Enemy((25, 150, 0), (50, 25), get_enemy_type("basic enemy")),
    Enemy((25, 150, 0), (200, 10), get_enemy_type("basic enemy")),
]
LEVEL3 = [Enemy((25, 150, 0), (110, 5), get_enemy_type("strong enemy"))]
LEVEL4 = [
    Enemy((25, 150, 0), (50, 25), get_enemy_type("strong enemy")),
    Enemy((25, 150, 0), (200, 10), get_enemy_type("strong enemy")),
]
LEVEL5 = [
    Enemy((25, 150, 0), (50, 15), get_enemy_type("basic enemy")),
    Enemy((25, 150, 0), (200, 10), get_enemy_type("basic enemy")),
    Enemy((25, 150, 0), (110, 5), get_enemy_type("strong enemy")),
]
LEVEL6 = [
    Enemy((25, 150, 0), (50, 15), get_enemy_type("strong enemy")),
    Enemy((25, 150, 0), (200, 10), get_enemy_type("basic enemy")),
    Enemy((25, 150, 0), (110, 5), get_enemy_type("strong enemy")),
]
LEVELS = [LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5, LEVEL6]


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Game(vgame.Game):
    def load(self):
        self.graphics.library.path = resource_path("./resources/textures")

        self.cur_level = 0
        self.bullets: list[Bullet] = []
        self.enemies: list[Enemy] = LEVELS[self.cur_level]
        self.player = Player((0, 125, 255), (100, 460), (50, 30), 500, 300, 100, 1)

        self.graphics.library.load(self.player)

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
        if Keys.LEFT_SHIFT in self.pressed_keys:
            self.player.speed = 250
        else:
            self.player.speed = 500
        self.player.vx, self.player.vy = vx, vy

        # TODO: Check separately x and y
        if not_in_border(
            self.player.x, self.player.y, self.player.vx, self.player.vy, WIDTH, HEIGHT
        ) and not_in_border(
            self.player.x + self.player.width,
            self.player.y + self.player.height,
            self.player.vx,
            self.player.vy,
            WIDTH,
            HEIGHT,
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
                self.player.get_damage(bullet.damage)
                dell.append(bullet)
            for enemy in self.enemies:
                if enemy.collision(bullet):
                    enemy.get_damage(bullet.damage)
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
            if i in self.bullets:
                self.bullets.remove(i)

        if len(self.enemies) == 0:
            self.cur_level += 1
            if len(LEVELS) > self.cur_level:
                self.enemies = LEVELS[self.cur_level]

        if self.player.hp <= 0:
            pygame.mixer.music.load(resource_path("./resources/sounds/death.wav"))
            pygame.mixer.music.play()

    def draw(self):
        self.graphics.draw_sprite(self.player)

        for enemy in self.enemies:
            self.graphics.draw_sprite(enemy)

        for bullet in self.bullets:
            self.graphics.draw_sprite(bullet)

    def exit(self):
        ...


pygame.mixer.init()
pygame.mixer.music.load(resource_path("./resources/sounds/bgm.wav"))
pygame.mixer.music.play(loops=-1)
vgame.Run(Game(framerate=60, width=WIDTH, height=HEIGHT))
