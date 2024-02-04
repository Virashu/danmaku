"""Game level background class declaration."""

import vgame
import pygame


class Background(vgame.graphics.Sprite):
    """Game level background class."""

    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Making it animated
        self.last_animation_time = 0
        self.current_frame = 0
        self.frame_count = 48
        self.frame_duration = 100
        self.frames = [
            f"background/background_{i}.png" for i in range(self.frame_count)
        ]
        self.texture_file = self.frames[0]
        self.texture_size = self.width, self.height

    def draw(self, graphics: vgame.graphics.Graphics):
        graphics.draw_sprite(self)

    def animation(self):
        """Animate the sprite."""
        t = pygame.time.get_ticks()
        if t - self.last_animation_time >= self.frame_duration:
            self.texture_file = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.last_animation_time = t

    def update(self, delta: int | float):
        self.animation()
