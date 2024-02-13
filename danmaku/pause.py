"""In-game pause menu."""

import vgame


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Pause:
    def load(self, width, height):
        """Load pause menu."""
        self.selection_index = 0

        self.width, self.height = width, height

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
        graphics.rectangle((0, 0), (self.width, self.height), (0, 0, 180)) #, alpha=1)
        graphics.text("Danmaku", (0, 10), (255, 255, 180))

        for i, button in enumerate(self.buttons):
            graphics.text(
                button[0],
                (0, 100 + i * 50),
                (255, 200, 180) if i == self.selection_index else (255, 255, 255),
            )
