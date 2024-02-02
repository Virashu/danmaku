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

        self.buttons = (
            ("New game", "new_game"),
            ("Continue", "continue"),
            ("Settings", "settings"),
            ("Quit", "quit"),
        )

    def update(self):
        if vgame.Keys.UP in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.UP)
            self.selection_index = (self.selection_index - 1) % len(self.buttons)
        if vgame.Keys.DOWN in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.DOWN)
            self.selection_index = (self.selection_index + 1) % len(self.buttons)
        if {vgame.Keys.RETURN, vgame.Keys.Z, vgame.Keys.SPACE} & self.pressed_keys:
            match self.buttons[self.selection_index][1]:
                case "new_game":
                    # Delete game from db & go to game scene
                    ...
                case "continue":
                    # Load game from db & go to game scene
                    ...
                case "settings":
                    # Go to settings scene
                    ...
                case "quit":
                    # Trigger pygame quit event
                    ...

    def draw(self):
        for i, button in enumerate(self.buttons):
            self.graphics.text(
                button[0],
                (0, i * 50),
                (255, 200, 180) if i == self.selection_index else (255, 255, 255),
            )

    def exit(self): ...
