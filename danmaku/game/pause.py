"""In-game pause menu."""

import vgame
from danmaku.game.background import Background
from danmaku.ui.button import Button, Cursor


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Pause:
    def load(self, width, height, delta):
        """Load pause menu."""
        self.selection_index = 0
        self.delta = delta

        self.cursor = Cursor((10, 100))

        self.width, self.height = width, height
        self.background_object = Background(0, 0, self.width, self.height, ["menu.png"])

        self.buttons = (
            Button("Continue", "continue"),
            Button("Main menu", "menu")
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
            self.exit_status = self.buttons[self.selection_index].codename
        self.cursor.y = 100 + self.selection_index * 50
        self.cursor.update(self.delta)

    def draw(self, graphics: vgame.graphics.Graphics):
        """Draw pause menu."""
        graphics.draw_sprite(self.background_object)
        graphics.text("Danmaku", (self.width // 2 - 70, 10), (0, 74, 127))

        self.cursor.draw(graphics)

        for i, button in enumerate(self.buttons):
            selected_color = (0, 74, 127)
            color = selected_color if i == self.selection_index else (255, 255, 255)

            graphics.text(
                button.text,
                (70, 100 + i * 50),
                color,
            )