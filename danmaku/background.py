"""Game level background class declaration."""

import vgame
import pygame

from danmaku.animated import Animated
from danmaku.gameobject import GameObject


class Background(Animated):
    """Game level background class."""

    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
    ):
        self.frame_count = 48
        frames = [f"background/background_{i}.png" for i in range(self.frame_count)]
        super().__init__((x, y), (width, height), 0, frames, 0, period=0.1)
        self.texture_size = self.width, self.height

    def draw(self, graphics: vgame.graphics.Graphics):
        graphics.draw_sprite(self)

    def update(self, delta: int | float):
        self.animate()
