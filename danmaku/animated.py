"""Declaration of Animated class"""

import pygame
import vgame

from danmaku.gameobject import GameObject


class Animated(GameObject):
    """Base class for animated objects

    Args:
        xy (tuple[int | float, int | float]): Position of the object.
        width_height (tuple[int | float, int | float]): Width and height of the object.
        speed (int | float): Speed of the object.
        frames (list[str]): List of frames
        freq (int | float): Frequency of animation
        period (int | float | None, optional): Period of animation. Defaults to None.

        You can pass freq as '0' and just use period

    """

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        frames: list[str],
        freq: int | float,
        period: int | float | None = None,
    ) -> None:
        super().__init__(xy, width_height, speed)

        if len(frames):
            self.animation_frames = frames
        if period is not None:
            self.animation_period = period
            self.animation_freq = 1 / period
        else:
            self.animation_freq = freq
            self.animation_period = 1 / freq
        self.animation_current = 0
        self.animation_last = 0

        if len(frames):
            self.texture_file = self.animation_frames[self.animation_current]

    def can_animate(self) -> bool:
        """Check if possible to animate"""
        time = pygame.time.get_ticks() / 1000

        if time - self.animation_last >= self.animation_freq:
            self.animation_last = time
            return True
        return False

    def animate(self) -> None:
        """Animate one frame if possible"""
        if self.can_animate():
            self.animation_current = (self.animation_current + 1) % len(
                self.animation_frames
            )
            self.texture_file = self.animation_frames[self.animation_current]

    def draw(self, graphics: vgame.graphics.Graphics) -> None: ...
