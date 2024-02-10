"""Main menu scene."""

import pygame
import vgame

from danmaku.database import get_saved_objects
from danmaku.button import Button, Cursor
from danmaku.utils import resource_path


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Menu(vgame.Scene):
    def load(self):
        self.graphics.library.path = resource_path("textures")

        self.selection_index = 0

        self.buttons = (
            Button("New game", "new_game"),
            Button("Continue", "continue"),
            Button("Settings", "settings"),
            Button("History", "history"),
            Button("Quit", "quit"),
        )

        self.cursor = Cursor((10, 100))

        self.exit_status = ""

    def update(self):
        if self.get_click(vgame.Keys.UP):
            self.selection_index = (self.selection_index - 1) % len(self.buttons)
        if self.get_click(vgame.Keys.DOWN):
            self.selection_index = (self.selection_index + 1) % len(self.buttons)
        if {vgame.Keys.RETURN, vgame.Keys.Z, vgame.Keys.SPACE} & self.pressed_keys:
            match self.buttons[self.selection_index].codename:
                case "new_game":
                    # Delete game from db & go to game scene
                    self.exit_status = "game", True
                    self.stop()
                case "continue":
                    # Just go to game scene
                    if get_saved_objects():
                        self.exit_status = "game", False
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
        self.cursor.y = 100 + self.selection_index * 50
        self.cursor.update(self.delta)

    def draw(self):
        self.graphics.text("Danmaku", (0, 10), (255, 255, 180))

        self.cursor.draw(self.graphics)

        for i, button in enumerate(self.buttons):
            selected_color = (180, 255, 255)
            if button.codename == "continue":
                if not get_saved_objects():
                    selected_color = (255, 100, 100)
            color = selected_color if i == self.selection_index else (255, 255, 255)

            self.graphics.text(
                button.text,
                (70, 100 + i * 50),
                color,
            )

    def exit(self): ...
