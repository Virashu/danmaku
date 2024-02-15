"""Main menu scene."""

import pygame
import vgame

from danmaku.database import get_settings
from danmaku.utils import resource_path


# pylint: disable=attribute-defined-outside-init, missing-class-docstring
class GameEnd(vgame.Scene):
    def load(self):
        self.graphics.library.path = resource_path("textures")

        pygame.mixer.init()
        pygame.mixer.music.set_volume(get_settings()["music_volume"]["value"] / 100)
        pygame.mixer.music.load(resource_path(self.music))
        pygame.mixer.music.play()

    def set(self, text, background, music):
        self.text = text
        if "win" in text:
            self.delta_color = 2
        else:
            self.delta_color = 0
        self.background_color = background
        self.text_color = list(background)
        self.v = (255 - self.text_color[self.delta_color]) / 500
        self.music = music

    def update(self):
        for i in range(3):
            if i == self.delta_color:
                self.text_color[i] += self.v
            else:
                if self.text_color[i] - 50 > 0:
                    self.text_color[i] -= 50
        if self.text_color[self.delta_color] + self.v >= 255:
            pygame.time.wait(1000)
            self.stop()

    def draw(self) -> None:
        self.graphics.rectangle(
            (0, 0), (self.width, self.height), self.background_color
        )

        #  NOTE: update vgame to version 1.6.4
        self.graphics.text(
            self.text, (30, self.height // 3), tuple(self.text_color), font_size=90
        )

    def exit(self): ...
