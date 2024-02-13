"""Game scene."""

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
    get_settings,
)
from danmaku.pause import Pause
from danmaku.background import Background
from danmaku.drop import Drop, PowerUp, Points
from danmaku.level import Level, Stage, BossStage


STAGE1 = Stage([Enemy((150, 15), "basic enemy")])
STAGE2 = Stage([Enemy((50, -25), "basic enemy"), Enemy((200, -50), "basic enemy")])
STAGE3 = Stage([Enemy((110, 5), "strong enemy")])
STAGE4 = Stage([Enemy((50, -25), "strong enemy"), Enemy((200, -50), "strong enemy")])
STAGE5 = Stage(
    [
        Enemy((50, -20), "basic enemy"),
        Enemy((200, -50), "basic enemy"),
        Enemy((110, -35), "strong enemy"),
    ]
)
STAGE6 = Stage(
    [
        Enemy((50, -15), "strong enemy"),
        Enemy((200, -50), "basic enemy"),
        Enemy((110, -35), "strong enemy"),
    ]
)
STAGE7 = BossStage(enemies=[], boss=Enemy((150, -40), "boss"), actions=[])


STAGE8 = Stage(
    [
        Enemy((50, -15), "strong enemy"),
        Enemy((200, -50), "strong enemy"),
        Enemy((300 - 50, -35), "strong enemy"),
    ]
)
STAGE9 = Stage(
    [
        Enemy((50, -15), "strong enemy"),
        Enemy((200, -50), "strong enemy"),
        Enemy((300 - 50, -35), "strong enemy"),
    ]
)
STAGE10 = BossStage(
    enemies=[
        Enemy((50, -15), "strong enemy"),
        Enemy((300 - 50, -35), "strong enemy"),
    ],
    boss=Enemy((200, -50), "boss"),
    actions=[],
)


LEVEL1 = Level(
    stages=[
        STAGE1,
        STAGE2,
        STAGE3,
        STAGE4,
        STAGE5,
        STAGE6,
        STAGE7,
    ]
)

LEVEL2 = Level(stages=[STAGE8, STAGE9, STAGE10])

LEVELS = LEVEL1, LEVEL2


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Game(vgame.Scene):
    new_game: bool = True

    def load(self):
        self.graphics.library.path = resource_path("textures")

        self.settings = get_settings()

        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.settings["music_volume"]["value"] / 100)
        pygame.mixer.music.load(resource_path("sounds/bgm.wav"))
        pygame.mixer.music.play(loops=-1)

        self.paused = False
        self.pause_object = Pause()
        self.exit_status = ""

        self.background_object = Background(0, 0, self.width, self.height)

        self.bullets: list[Bullet] = []
        self.drops: list[Drop] = []

        self.boss_hp: int | None = None

        if self.new_game:
            self.current_level: int = 0
            self.enemies: list[Enemy] = list(LEVELS[self.current_level].enemies)
            self.player = Player((self.width // 2, self.height - 50), "player",
                                 bombs=get_settings()["bombs"]["value"], lives=get_settings()["lives"]["value"])

        else:
            self.enemies: list[Enemy] = []
            for entity in get_saved_objects():
                match entity["object"]:
                    case "enemy":
                        self.enemies.append(
                            Enemy(
                                entity["object_position"],
                                entity["object_type"],
                                start_hp=entity["object_hp"],
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
            self.current_level: int = saved_game["level"]
            self.player.score = saved_game["score"]
            self.player.power = saved_game["power"]
            self.player.bombs = saved_game["bombs"]
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
                set_saved_game(self.current_level, self.player.score, self.player.power, self.player.bombs)
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
        self.player.animate()

        LEVELS[self.current_level].stage.update()

        for enemy in self.enemies:
            if self.player.collision(enemy):
                self.player.get_damage(enemy.damage / 100)
            self.bullets += enemy.shoot()
            enemy.animate()
            enemy.update(self.delta)
            if (
                enemy.y > self.height / 2 and not 0 <= enemy.x < self.width
            ) or enemy.y > self.height + enemy.height / 2:
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
                    if enemy.health <= 0:
                        self.player.score += enemy.cost
                        self.drops += enemy.generate_drops()
                        self.enemies.remove(enemy)

                    self.bullets.remove(bullet)
                    break

        for bullet in self.bullets:
            bullet.update(self.delta)

            if not not_in_border(
                bullet.x, bullet.y, bullet.vx, bullet.vy, self.width, self.height
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

            if not not_in_border(
                drop.x, drop.y, drop.vx, drop.vy, self.width, self.height
            ):
                self.drops.remove(drop)

        self.background_object.animate()

        if len(self.enemies) == 0:
            self.next_level()

        if self.player.health <= 0:
            set_saved_game(self.current_level, self.player.score, self.player.power, self.player.bombs)
            self.exit_status = "lose"
            death_sfx = pygame.mixer.Sound(resource_path("sounds/death.wav"))
            death_sfx.set_volume(self.settings["sfx_volume"]["value"] / 100)
            channel = death_sfx.play()
            while channel.get_busy():
                pygame.time.wait(10)
            self.stop()

    def next_level(self) -> None:
        """Start next level if possible"""
        if LEVELS[self.current_level].next_stage():
            self.enemies = list(LEVELS[self.current_level].enemies)
        elif len(LEVELS) > self.current_level + 1:
            self.current_level += 1
            self.enemies = list(LEVELS[self.current_level].enemies)
        else:
            set_saved_game(self.current_level, self.player.score, self.player.power, self.player.bombs)
            self.exit_status = "win"
            self.stop()

    def update(self):
        # self.print_stats()
        if Keys.ESCAPE in self.pressed_keys:
            self.pressed_keys.remove(Keys.ESCAPE)
            self.paused = not self.paused
            if self.paused:
                self.pause_object.load(self.width, self.height)

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

        self.graphics.text(f"HP: {self.player.health}", (0, 0))
        self.graphics.text(f"Score: {self.player.score}", (150, 0))
        # self.graphics.text(f"Bombs: {self.player.bombs}", (100, 0))
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
            f"HP: {self.player.health}",
            f"Score: {self.player.score}",
            f"Level: {self.current_level}",
            f"Power: {self.player.power}",
            f"Boss: {self.boss_hp}",
            "",
            f"Enemies: {len(self.enemies)}",
            f"Bullets: {len(self.bullets)}",
            f"Drops: {len(self.drops)}",
            sep="\n",
        )

        print("\x1b[?25h", end="")  # show cursor
