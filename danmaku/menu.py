import pygame
from danmaku.button import Button
import vgame


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Menu(vgame.Scene):
    def load(self):
        self.selection_index = 0
        self.new_game = False
        self.last_game = False
        self.status = self.new_game or self.last_game

        self.buttons = [
            Button(
                (self.width // 4, self.height // 3),
                200,
                40,
                (255, 0, 0),
                "New game",
                (0, 0, 255),
                42,
            ),
            Button(
                (self.width // 4 + 10, self.height // 3 + 50),
                200,
                40,
                (255, 0, 0),
                "Continue",
                (0, 0, 255),
                42,
            ),
            Button(
                (self.width // 4 + 13, self.height // 3 + 100),
                200,
                40,
                (255, 0, 0),
                "Settings",
                (0, 0, 255),
                42,
            ),
        ]

    def update(self):
        if vgame.Keys.UP in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.UP)
            self.selection_index = (self.selection_index - 1) % len(self.buttons)
        if vgame.Keys.DOWN in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.DOWN)
            self.selection_index = (self.selection_index + 1) % len(self.buttons)
        if vgame.Keys.RETURN in self.pressed_keys or vgame.Keys.Z in self.pressed_keys:
            if self.selection_index == 0:
                self.new_game = True
                # Delete game from db & go to game scene
            if self.selection_index == 1:
                self.last_game = True
                self.stop()
                # just go to game scene
            if self.selection_index == 2:
                pass
            self.status = self.new_game or self.last_game
        print(self.selection_index)

    def draw(self):
        for button in self.buttons:
            button.draw(self.graphics)
