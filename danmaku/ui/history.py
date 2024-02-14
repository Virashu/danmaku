"""Game history scene."""

import vgame

from danmaku.database import get_game_history


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class History(vgame.Scene):
    def load(self):
        self.selection_index = 0

        self.history = get_game_history()
        self.record_count = len(self.history)

    def update(self):
        if self.get_click(vgame.Keys.UP):
            self.selection_index = (self.selection_index - 1) % self.record_count
        if self.get_click(vgame.Keys.DOWN):
            self.selection_index = (self.selection_index + 1) % self.record_count
        if {
            vgame.Keys.RETURN,
            vgame.Keys.Z,
            vgame.Keys.SPACE,
            vgame.Keys.ESCAPE,
        } & self.pressed_keys:
            self.stop()

    def draw(self):
        self.graphics.rectangle((0, 0), (self.width, self.height), (30, 157, 214, 180))

        self.graphics.text("History", (self.width // 2 - 30, 0), (0, 74, 127))

        for i, game in enumerate(self.history[self.selection_index :]):
            self.graphics.text(
                f"Level: {game['level'] + 1}, Score: {game['score']}, Time: {game['time']}",
                (20, 50 + 50 * i),
                (255, 255, 255),
            )

    def exit(self): ...
