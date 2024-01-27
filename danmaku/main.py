import vgame
from vgame import Keys
import pygame

from danmaku.utils import not_in_border, resource_path
from danmaku.enemy import Enemy
from danmaku.player import Player
from danmaku.bullet import Bullet
from danmaku.database import get_saved_objects, get_saved_game, set_saved_objects, set_saved_game, delete_saved_objects
from menu import Menu

WIDTH, HEIGHT = 300, 500
LEVEL1 = [Enemy((25, 150, 0), (150, 15), "basic enemy")]
LEVEL2 = [
    Enemy((25, 150, 0), (50, 25), "basic enemy"),
    Enemy((25, 150, 0), (200, 10), "basic enemy"),
]
LEVEL3 = [Enemy((25, 150, 0), (110, 5), "strong enemy")]
LEVEL4 = [
    Enemy((25, 150, 0), (50, 25), "strong enemy"),
    Enemy((25, 150, 0), (200, 10), "strong enemy"),
]
LEVEL5 = [
    Enemy((25, 150, 0), (50, 15), "basic enemy"),
    Enemy((25, 150, 0), (200, 10), "basic enemy"),
    Enemy((25, 150, 0), (110, 5), "strong enemy"),
]
LEVEL6 = [
    Enemy((25, 150, 0), (50, 15), "strong enemy"),
    Enemy((25, 150, 0), (200, 10), "basic enemy"),
    Enemy((25, 150, 0), (110, 5), "strong enemy"),
]
FINAL = [Enemy((25, 150, 0), (150, 15), "boss")]
LEVELS = [LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5, LEVEL6, FINAL]


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Game(vgame.Game):
    def load(self):
        self.graphics.library.path = resource_path("./resources/textures")

        self.pause = False

        menu = Menu("main", WIDTH, HEIGHT)
        menu.load()

        if menu.new_game:
            self.cur_level = 0
            self.bullets: list[Bullet] = []
            self.enemies: list[Enemy] = LEVELS[self.cur_level].copy()
            self.player = Player((0, 125, 255), (100, 460), (50, 30), 500, 300, 100, 1)

        if menu.last_game:
            self.enemies: list[Enemy] = []
            self.bullets: list[Bullet] = []
            objects = get_saved_objects()
            for el in objects:
                if el[0] == "enemy":
                    self.enemies.append(Enemy((25, 150, 0), el[2], el[1]))
                if el[0] == "bullet":
                    if "enemy" in el[1]:
                        self.bullets.append(Bullet(True, (25, 150, 0), el[2], 150, el[3], el[1]))
                    elif "player" in el[1]:
                        self.bullets.append(Bullet(False, (25, 150, 0), el[2], 150, el[3], el[1]))

            saved_game = get_saved_game()
            self.cur_level = saved_game[3]
            self.player = Player((0, 125, 255), (saved_game[0], saved_game[1]), (50, 30), 500, saved_game[2], 100, 1)
            delete_saved_objects()
        self.graphics.library.load(self.player)

    def update(self):
        if Keys.P in self.pressed_keys:
            self.pressed_keys.remove(Keys.P)
            self.pause = True
            pause_menu = Menu("pause", WIDTH, HEIGHT)
            pause_menu.load()
            if pause_menu.start:  # It doesn't work properly
                self.pause = False
            if pause_menu.to_menu:
                pass
            if pause_menu.save:
                delete_saved_objects()
                set_saved_objects("enemy", self.enemies)
                set_saved_objects("bullet", self.bullets)
                set_saved_game(self.cur_level, self.player)
                quit()
        if not self.pause:
            vx = vy = 0
            if Keys.RIGHT in self.pressed_keys:
                vx += 1
            if Keys.LEFT in self.pressed_keys:
                vx -= 1
            if Keys.UP in self.pressed_keys:
                vy -= 1
            if Keys.DOWN in self.pressed_keys:
                vy += 1
            if Keys.SPACE in self.pressed_keys or Keys.Z in self.pressed_keys:
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


import os

print(os.listdir(resource_path("./resources/")))

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.load(resource_path("./resources/sounds/bgm.wav"))
pygame.mixer.music.play(loops=-1)
vgame.Run(Game(framerate=60, width=WIDTH, height=HEIGHT))
