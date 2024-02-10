"""Game scene."""

import random

import vgame
from vgame import Keys
import pygame

from danmaku.utils import not_in_border, resource_path
from danmaku.enemy import Enemy
from danmaku.player import Player
from danmaku.bullet import Bullet
from danmaku.database import (
    get_saved_objects,
    get_saved_game,
    set_saved_objects,
    set_saved_game,
    delete_saved_objects,
)
from danmaku.pause import Pause
from danmaku.background import Background
from danmaku.drop import Drop, PowerUp, Points


WIDTH, HEIGHT = 300, 500
LEVEL1 = [Enemy((150, 15), "basic enemy")]
LEVEL2 = [
    Enemy((50, -25), "basic enemy"),
    Enemy((200, -50), "basic enemy"),
]
LEVEL3 = [Enemy((110, 5), "strong enemy")]
LEVEL4 = [
    Enemy((50, -25), "strong enemy"),
    Enemy((200, -50), "strong enemy"),
]
LEVEL5 = [
    Enemy((50, -20), "basic enemy"),
    Enemy((200, -50), "basic enemy"),
    Enemy((110, -35), "strong enemy"),
]
LEVEL6 = [
    Enemy((50, -15), "strong enemy"),
    Enemy((200, -50), "basic enemy"),
    Enemy((110, -35), "strong enemy"),
]
LEVEL7 = [Enemy((WIDTH / 2, -40), "boss")]
LEVEL8 = [
    Enemy((50, -15), "strong enemy"),
    Enemy((200, -50), "strong enemy"),
    Enemy((WIDTH - 50, -35), "strong enemy"),
]
LEVEL9 = [
    Enemy((50, -15), "strong enemy"),
    Enemy((200, -50), "strong enemy"),
    Enemy((WIDTH - 50, -35), "strong enemy"),
]
LEVEL10 = [
    Enemy((50, -15), "strong enemy"),
    Enemy((200, -50), "boss"),
    Enemy((WIDTH - 50, -35), "strong enemy"),
]
LEVELS = [
    LEVEL1,
    LEVEL2,
    LEVEL3,
    LEVEL4,
    LEVEL5,
    LEVEL6,
    LEVEL7,
    LEVEL8,
    LEVEL9,
    LEVEL10,
]


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Game(vgame.Scene):
    new_game: bool = True

    def load(self):
        self.graphics.library.path = resource_path("textures")

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.load(resource_path("sounds/bgm.wav"))
        pygame.mixer.music.play(loops=-1)

        self.paused = False
        self.pause_object = Pause()
        self.exit_status = ""

        self.background_object = Background(0, 0, self.width, self.height)

        self.bullets: list[Bullet] = []
        self.drops: list[Drop] = []

        if self.new_game:
            self.cur_level = 0
            self.enemies: list[Enemy] = LEVELS[self.cur_level].copy()
            self.player = Player((WIDTH // 2, HEIGHT - 50), "player")

        else:
            self.enemies: list[Enemy] = []
            for entity in get_saved_objects():
                match entity["object"]:
                    case "enemy":
                        self.enemies.append(
                            Enemy(
                                entity["object_position"],
                                entity["object_type"],
                                updated_hp=entity["object_hp"],
                            )
                        )
                    case "bullet":
                        self.bullets.append(
                            Bullet(
                                entity["object_position"],
                                entity["object_damage"],
                                entity["object_type"],
                            )
                        )
                    case "player":
                        self.player = Player(
                            entity["object_position"],
                            entity["object_type"],
                            updated_hp=entity["object_hp"],
                        )

            saved_game = get_saved_game()
            self.cur_level = saved_game["level"]
            self.player.score = saved_game["score"]
            self.player.power = saved_game["power"]
            delete_saved_objects()

        self.player.set_bounds(0, 0, self.width, self.height)

    def update_pause(self):
        """Called from update loop if paused"""
        self.pause_object.update(self.pressed_keys)
        status = self.pause_object.exit_status
        match status:
            case "continue":
                self.paused = False
            case "settings":
                raise NotImplementedError()
            case "menu":
                delete_saved_objects()
                set_saved_objects("enemy", self.enemies)
                set_saved_objects("bullet", self.bullets)
                set_saved_objects("player", [self.player])
                set_saved_game(self.cur_level, self.player.score, self.player.power)
                self.stop()

    def update_game(self):
        """Called from update loop if *not* paused"""

        vx = (Keys.RIGHT in self.pressed_keys) - (Keys.LEFT in self.pressed_keys)
        vy = (Keys.DOWN in self.pressed_keys) - (Keys.UP in self.pressed_keys)

        if {Keys.SPACE, Keys.Z} & self.pressed_keys:
            self.bullets += self.player.shoot()
        if Keys.X in self.pressed_keys:
            self.bullets += self.player.bomb()
        if Keys.LEFT_SHIFT in self.pressed_keys:
            self.player.slow = True
        else:
            self.player.slow = False

        self.player.vx, self.player.vy = vx, vy

        self.player.update(self.delta)
        self.player.animation()

        for enemy in self.enemies:
            if self.player.collision(enemy):
                self.player.get_damage(enemy.damage / 100)
            self.bullets += enemy.shoot()
            enemy.animation()
            enemy.update(self.delta)
            if enemy.y > HEIGHT / 2 and not 0 <= enemy.x < WIDTH:
                self.enemies.remove(enemy)

        for bullet in filter(lambda b: b.enemy, self.bullets):
            if self.player.collision(bullet):
                self.player.get_damage(bullet.damage)
                self.bullets.remove(bullet)
                continue

        for bullet in filter(lambda b: not b.enemy, self.bullets):
            for enemy in self.enemies:
                if enemy.collision(bullet):
                    enemy.get_damage(bullet.damage)
                    if enemy.hp <= 0:
                        self.player.score += enemy.cost
                        x, y = enemy.x, enemy.y
                        self.enemies.remove(enemy)

                        match random.choices(("powerup", "points", None), (1, 1, 2))[0]:
                            case "powerup":
                                self.drops.append(PowerUp((x, y)))
                            case "points":
                                self.drops.append(Points((x, y)))

                    self.bullets.remove(bullet)
                    break

        for bullet in self.bullets:
            bullet.update(self.delta)

            if not not_in_border(
                bullet.x, bullet.y, bullet.vx, bullet.vy, WIDTH, HEIGHT
            ):
                self.bullets.remove(bullet)

        for drop in self.drops:
            if self.player.collision(drop):
                if isinstance(drop, PowerUp):
                    self.player.power += 2
                elif isinstance(drop, Points):
                    self.player.score += 10
                self.drops.remove(drop)
                continue

            drop.update(self.delta)

            if not not_in_border(drop.x, drop.y, drop.vx, drop.vy, WIDTH, HEIGHT):
                self.drops.remove(drop)

        self.background_object.animation()

        if len(self.enemies) == 0:
            if len(LEVELS) > self.cur_level + 1:
                self.cur_level += 1
                self.enemies = LEVELS[self.cur_level].copy()
            else:
                set_saved_game(self.cur_level, self.player.score, self.player.power)
                self.exit_status = "win"
                self.stop()

        if self.player.hp <= 0:
            set_saved_game(self.cur_level, self.player.score, self.player.power)
            self.exit_status = "lose"
            death_sfx = pygame.mixer.Sound(resource_path("sounds/death.wav"))
            channel = death_sfx.play()
            while channel.get_busy():
                pygame.time.wait(10)
            self.stop()

    def update(self):
        # self.print_stats()
        if Keys.ESCAPE in self.pressed_keys:
            self.pressed_keys.remove(Keys.ESCAPE)
            self.paused = not self.paused
            if self.paused:
                self.pause_object.load()

        if self.paused:
            self.update_pause()
        else:
            self.update_game()

    def draw(self):
        self.graphics.draw_sprite(self.background_object)

        self.player.draw(self.graphics)

        for enemy in self.enemies:
            self.graphics.draw_sprite(enemy)

        for bullet in self.bullets:
            self.graphics.draw_sprite(bullet)

        for drop in self.drops:
            self.graphics.draw_sprite(drop)

        self.graphics.text(f"HP: {self.player.hp}", (0, 0))
        self.graphics.text(f"Score: {self.player.score}", (150, 0))

        if self.paused:
            self.pause_object.draw(self.graphics)

    def exit(self):
        pygame.mixer.music.stop()

    def print_stats(self):
        """Dev debug"""
        print("\x1b[?25l", end="")  # hide cursor
        print("\x1b[2J\x1b[0;0H", end="")  # clear console

        # Tech stuff
        print(
            f"\x1b[{32 if self.fps >= self.framerate else 31}mFPS:\t{self.fps:.2f}\x1b[0m",
            f"Gr. dT:\t{self.graphics_delta*1000}ms",
            "",
            f"\x1b[{32 if self.tps >= self.tickrate else 31}mTPS:\t{self.tps:.2f}\x1b[0m",
            f"dT:\t{self.delta*1000}ms",
            sep="\n",
        )

        print(end="\n\n")

        # Game stats
        print(
            f"HP: {self.player.hp}",
            f"Score: {self.player.score}",
            f"Level: {self.cur_level}",
            "",
            f"Enemies: {len(self.enemies)}",
            f"Bullets: {len(self.bullets)}",
            f"Drops: {len(self.drops)}",
            sep="\n",
        )

        print("\x1b[?25h", end="")  # show cursor
