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
from danmaku.menu import Menu
from danmaku.pause import Pause


WIDTH, HEIGHT = 300, 500
LEVEL1 = [Enemy((150, 15), "basic enemy")]
LEVEL2 = [
    Enemy((50, 25), "basic enemy"),
    Enemy((200, 10), "basic enemy"),
]
LEVEL3 = [Enemy((110, 5), "strong enemy")]
LEVEL4 = [
    Enemy((50, 25), "strong enemy"),
    Enemy((200, 10), "strong enemy"),
]
LEVEL5 = [
    Enemy((50, 15), "basic enemy"),
    Enemy((200, 10), "basic enemy"),
    Enemy((110, 5), "strong enemy"),
]
LEVEL6 = [
    Enemy((50, 15), "strong enemy"),
    Enemy((200, 10), "basic enemy"),
    Enemy((110, 5), "strong enemy"),
]
FINAL = [Enemy((150, 15), "boss")]
LEVELS = [LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5, LEVEL6, FINAL]


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
        self.pause_object.load()

        self.bullets: list[Bullet] = []

        if self.new_game:
            self.cur_level = 0
            self.enemies: list[Enemy] = LEVELS[self.cur_level].copy()
            self.player = Player((100, 450), "player")

        else:

            saved_game = get_saved_game()
            self.cur_level = saved_game["level"]

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

    def update(self):
        if Keys.ESCAPE in self.pressed_keys:
            self.pressed_keys.remove(Keys.ESCAPE)
            self.paused = not self.paused

        if self.paused:
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
                    set_saved_game(self.cur_level, self.player)
                    self.stop()

        else:
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
                self.bullets += self.player.shoot()
            if Keys.LEFT_SHIFT in self.pressed_keys:
                self.player.speed = 100
            else:
                self.player.speed = 150

            self.player.vx, self.player.vy = vx, vy

            # TODO: Check separately x and y
            if not_in_border(
                self.player.x,
                self.player.y,
                self.player.vx,
                self.player.vy,
                WIDTH,
                HEIGHT,
            ) and not_in_border(
                self.player.x + self.player.width,
                self.player.y + self.player.height,
                self.player.vx,
                self.player.vy,
                WIDTH,
                HEIGHT,
            ):
                self.player.update(self.delta)
                self.player.animation()

            for enemy in self.enemies:
                self.bullets += enemy.shoot()
                enemy.animation()
                enemy.update(self.delta)
                if not not_in_border(
                    enemy.x, enemy.y, enemy.vx, enemy.vy, WIDTH, HEIGHT
                ):
                    self.enemies.remove(enemy)

            dell = set()

            for bullet in self.bullets:
                if self.player.collision(bullet):
                    self.player.get_damage(bullet.damage)
                    dell.add(bullet)

                for enemy in self.enemies:
                    if enemy.collision(bullet):
                        enemy.get_damage(bullet.damage)
                        dell.add(bullet)
                        if enemy.hp <= 0:
                            self.enemies.remove(enemy)

                bullet.update(self.delta)
                bullet.draw(self.graphics)

                if not not_in_border(
                    bullet.x, bullet.y, bullet.vx, bullet.vy, WIDTH, HEIGHT
                ):
                    dell.add(bullet)

            for i in dell:
                self.bullets.remove(i)

            if len(self.enemies) == 0:
                self.cur_level += 1
                if len(LEVELS) > self.cur_level:
                    self.enemies = LEVELS[self.cur_level]

        if self.player.hp <= 0:
            death_sfx = pygame.mixer.Sound(resource_path("sounds/death.wav"))
            channel = death_sfx.play()
            while channel.get_busy():
                pygame.time.wait(10)
            self.stop()

    def draw(self):
        self.graphics.draw_sprite(self.player)

        for enemy in self.enemies:
            self.graphics.draw_sprite(enemy)

        for bullet in self.bullets:
            self.graphics.draw_sprite(bullet)

        self.graphics.text(f"HP: {self.player.hp}", (0, 0))

        if self.paused:
            self.pause_object.draw(self.graphics)

    def exit(self):
        pygame.mixer.music.stop()


runner = vgame.Runner()

while runner.running:
    menu = Menu(width=WIDTH, height=HEIGHT, title="Danmaku | Menu")
    runner.run(menu)
    match menu.exit_status:
        case "game_new":
            runner.run(Game(width=WIDTH, height=HEIGHT, title="Danmaku | Game"))
        case "game_continue":
            game = Game(width=WIDTH, height=HEIGHT, title="Danmaku | Game")
            game.new_game = False
            runner.run(game)
        case "settings":
            # settings = Settings(width=WIDTH, height=HEIGHT, title="Danmaku | Settings")
            # runner.run(settings)
            raise NotImplementedError()
