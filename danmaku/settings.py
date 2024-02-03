"""Settings scene."""

import vgame


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Settings(vgame.Scene):
    def load(self):
        self.selection_index = 0

        self.buttons = (("Quit", "quit"),)

        self.exit_status: str = ""

    def update(self):
        if vgame.Keys.UP in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.UP)
            self.selection_index = (self.selection_index - 1) % len(self.buttons)
        if vgame.Keys.DOWN in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.DOWN)
            self.selection_index = (self.selection_index + 1) % len(self.buttons)
        if vgame.Keys.RIGHT in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.RIGHT)
            # Update settings values left<->right
            # Like: music  [x x _ _ _]
            #       sfx    [x _ _ _ _]
        if vgame.Keys.LEFT in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.LEFT)
            # Same
        if {vgame.Keys.RETURN, vgame.Keys.Z, vgame.Keys.SPACE} & self.pressed_keys:
            match self.buttons[self.selection_index][1]:
                case "quit":
                    self.stop()

    def draw(self):
        self.graphics.text("Danmaku", (0, 10), (255, 255, 180))

        for i, button in enumerate(self.buttons):

            color = (255, 200, 180) if i == self.selection_index else (255, 255, 255)

            self.graphics.text(
                button[0],
                (0, 100 + i * 50),
                color,
            )

    def exit(self): ...
