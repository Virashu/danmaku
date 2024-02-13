"""Settings scene."""

import vgame

from danmaku.database import get_settings

from danmaku.ui.button import SettingsValue, Button
from danmaku.database.database import set_settings


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class Settings(vgame.Scene):
    def load(self):
        self.selection_index = 0

        settings_dict = get_settings()

        self.buttons: list[object] = []

        for key, value in settings_dict.items():
            self.buttons.append(
                SettingsValue(
                    key, value["display_name"], value["possible_values"], value["value"]
                )
            )

        self.buttons.append(
            Button("Quit", "quit"),
        )

        self.exit_status: str = ""

    def update(self):
        if self.get_click(vgame.Keys.UP):
            self.selection_index = (self.selection_index - 1) % len(self.buttons)
        if self.get_click(vgame.Keys.DOWN):
            self.selection_index = (self.selection_index + 1) % len(self.buttons)
        if self.get_click(vgame.Keys.RIGHT):
            button = self.buttons[self.selection_index]
            if isinstance(button, SettingsValue):
                button.increase()
        if self.get_click(vgame.Keys.LEFT):
            button = self.buttons[self.selection_index]
            if isinstance(button, SettingsValue):
                button.decrease()
        if {vgame.Keys.RETURN, vgame.Keys.Z, vgame.Keys.SPACE} & self.pressed_keys:
            button = self.buttons[self.selection_index]
            if isinstance(button, Button):
                if button.codename == "quit":
                    self.stop()

    def draw(self):
        self.graphics.text("Danmaku", (0, 10), (255, 255, 180))

        for i, button in enumerate(self.buttons):

            color = (255, 200, 180) if i == self.selection_index else (255, 255, 255)

            if isinstance(button, Button):
                self.graphics.text(
                    button.text,
                    (0, 100 + i * 50),
                    color,
                )

            if isinstance(button, SettingsValue):
                self.graphics.text(
                    f"{button.text}:  < {button.value} >",
                    (0, 100 + i * 50),
                    color,
                )

    def exit(self):
        update = {}
        for setting in self.buttons:
            if isinstance(setting, SettingsValue):
                name = setting.codename
                value = setting.value

                update[name] = str(value)
        set_settings(update)
