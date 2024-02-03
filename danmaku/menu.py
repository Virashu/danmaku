"""Main menu scene."""

import pygame
import vgame

from danmaku.database import get_saved_objects


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Menu(vgame.Scene):
    def load(self):
        self.selection_index = 0

        self.buttons = (
            ("New game", "new_game"),
            ("Continue", "continue"),
            ("Settings", "settings"),
            ("History", "history"),
            ("Quit", "quit"),
        )

        self.exit_status: str = ""

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
                    self.exit_status = "game_new"
                    self.stop()
                case "continue":
                    # Just go to game scene
                    if get_saved_objects():
                        self.exit_status = "game_continue"
                        self.stop()
                case "settings":
                    # Go to settings scene
                    # Maybe rework and do settings inside menu
                    # Pros: same controls
                    self.exit_status = "settings"
                    self.stop()
                case "history":
                    # Go to history scene
                    self.exit_status = "history"
                    self.stop()
                case "quit":
                    # Maybe rework to quit through exit status
                    pygame.event.post(pygame.event.Event(pygame.constants.QUIT))

    def draw(self):
        self.graphics.text("Danmaku", (0, 10), (255, 255, 180))

        for i, button in enumerate(self.buttons):
            if button[1] == "continue":
                if get_saved_objects():
                    color = (255, 255, 255)
                else:
                    color = (255, 100, 100)
            else:
                color = (
                    (255, 200, 180) if i == self.selection_index else (255, 255, 255)
                )

            self.graphics.text(
                button[0],
                (0, 100 + i * 50),
                color,
            )

    def exit(self): ...
