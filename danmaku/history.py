from danmaku.database import get_game_history
import vgame


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class History(vgame.Scene):
    def load(self):
        self.selection_index = 0

        self.history = get_game_history()
        self.record_count = len(self.history)

    def update(self):
        if vgame.Keys.UP in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.UP)
            self.selection_index = (self.selection_index - 1) % self.record_count
        if vgame.Keys.DOWN in self.pressed_keys:
            self.pressed_keys.discard(vgame.Keys.DOWN)
            self.selection_index = (self.selection_index + 1) % self.record_count
        if {
            vgame.Keys.RETURN,
            vgame.Keys.Z,
            vgame.Keys.SPACE,
            vgame.Keys.ESCAPE,
        } & self.pressed_keys:
            self.stop()

    def draw(self):
        self.graphics.text("History", (0, 0), (255, 255, 180))

        for i, game in enumerate(self.history[self.selection_index :]):
            self.graphics.text(
                f"Level: {game['level'] + 1}, Score: {game['score']}",
                (0, 20 * i),
                (255, 255, 255),
            )

    def exit(self): ...
