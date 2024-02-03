"""In-game pause menu."""

import vgame


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Pause:
    def __init__(self):
        self.selection_index = 0

        self.buttons = (
            ("Continue", "continue"),
            ("Settings", "settings"),
            ("Main menu", "menu"),
        )

        self.exit_status: str = ""

    def update(self, pressed_keys):
        """Update pause menu."""
        if vgame.Keys.UP in pressed_keys:
            pressed_keys.discard(vgame.Keys.UP)
            self.selection_index = (self.selection_index - 1) % len(self.buttons)
        if vgame.Keys.DOWN in pressed_keys:
            pressed_keys.discard(vgame.Keys.DOWN)
            self.selection_index = (self.selection_index + 1) % len(self.buttons)
        if {vgame.Keys.RETURN, vgame.Keys.Z, vgame.Keys.SPACE} & pressed_keys:
            self.exit_status = self.buttons[self.selection_index][1]

    def draw(self, graphics: vgame.graphics.Graphics):
        """Draw pause menu."""
        graphics.text("Danmaku", (0, 10), (255, 255, 180))

        for i, button in enumerate(self.buttons):
            graphics.text(
                button[0],
                (0, 100 + i * 50),
                (255, 200, 180) if i == self.selection_index else (255, 255, 255),
                background=(55, 55, 55),
            )
