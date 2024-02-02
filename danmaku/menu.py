import pygame
import vgame


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Menu(vgame.Scene):
    def load(self):
        self.selection_index = 0

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
                    # Just go to game scene
                    ...
                case "settings":
                    # Go to settings scene
                    ...
                case "quit":
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self):
        self.graphics.text("Danmaku", (0, 10), (255, 255, 180))

        for i, button in enumerate(self.buttons):
            self.graphics.text(
                button[0],
                (0, 100 + i * 50),
                (255, 200, 180) if i == self.selection_index else (255, 255, 255),
            )

    def exit(self): ...
