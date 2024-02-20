"""Declaration of Animated class"""

import pygame

from danmaku.game.gameobject import GameObject
from danmaku.utils import Direction


class Animated(GameObject):
    """Base class for animated objects

    Args:
        xy (tuple[int | float, int | float]): Position of the object.
        width_height (tuple[int | float, int | float]): Width and height of the object.
        speed (int | float): Speed of the object.
        frames (list[str]): List of frames
        freq (int | float | None, optional): Frequency of animation
        period (int | float | None, optional): Period of animation. Defaults to None.

        You can pass freq as '0' and just use period

    """

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        frames: list[str],
        freq: int | float | None = None,
        period: int | float | None = None,
    ) -> None:
        super().__init__(xy, width_height, speed)

        if len(frames):
            self.animation_frames = frames
        if period is not None:
            self.animation_period = period
            self.animation_freq = 1 / period
        elif freq is not None:
            self.animation_freq = freq
            self.animation_period = 1 / freq
        else:
            raise ValueError("You must pass period or freq")
        self.animation_current = 0
        self.animation_last = 0
        self.last_direction = 0

        if len(frames):
            self.texture_file = self.animation_frames[self.animation_current]

    def can_animate(self) -> bool:
        """Check if possible to animate"""
        time = pygame.time.get_ticks() / 1000

        if time - self.animation_last >= self.animation_period:
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

    def animate_absolute(self, time: int) -> None:
        """Set frame according to time (milliseconds)"""
        frame_duration = self.animation_period * 1000

        self.animation_current = int(time // frame_duration) % len(
            self.animation_frames
        )

        self.texture_file = self.animation_frames[self.animation_current]


class AnimatedDirectional(Animated):
    """Base class for animated objects, that change animations based on direction"""

    def __init__(
        self,
        xy: tuple[int | float, int | float],
        width_height: tuple[int | float, int | float],
        speed: int | float,
        frames: list[str],
        freq: int | float | None = None,
        period: int | float | None = None,
    ) -> None:
        super().__init__(xy, width_height, speed, [], freq, period)
        self.last_direction = 0

        self.animation_frames = {
            Direction.LEFT: [],
            Direction.RIGHT: [],
            Direction.UP: [],
            Direction.DOWN: [],
            Direction.STATIC: [],
        }

        for file in frames:
            if "left" in file:
                self.animation_frames[Direction.LEFT].append(file)
            if "right" in file:
                self.animation_frames[Direction.RIGHT].append(file)
            if "up" in file:
                self.animation_frames[Direction.UP].append(file)
            if "down" in file:
                self.animation_frames[Direction.DOWN].append(file)
            if "static" in file or "idle" in file:
                self.animation_frames[Direction.STATIC].append(file)

        self.texture_file = self.animation_frames[Direction.STATIC][
            self.animation_current
        ]

    def animate(
        self, direction_vector: tuple[int | float, int | float] = (0, 0)
    ) -> None:
        """Animate one frame if possible"""

        if self.can_animate():
            direction = None
            if direction_vector[0] == direction_vector[1] and direction_vector[0] == 0:
                direction = Direction.STATIC
            elif direction_vector[0] > 0:
                direction = Direction.RIGHT
            elif direction_vector[1] > 0:
                direction = Direction.DOWN
            elif direction_vector[0] < 0:
                direction = Direction.LEFT
            elif direction_vector[1] < 0:
                direction = Direction.UP

            if direction == Direction.STATIC:
                a = ""
                if self.last_direction == Direction.UP:
                    a = "up"
                elif self.last_direction == Direction.DOWN:
                    a = "down"
                elif self.last_direction == Direction.RIGHT:
                    a = "right"
                elif self.last_direction == Direction.LEFT:
                    a = "left"
                for i in self.animation_frames[direction]:
                    if a in i:
                        self.texture_file = i
            elif direction is not None:
                self.animation_current = (self.animation_current + 1) % len(
                    self.animation_frames[direction]
                )
                self.texture_file = self.animation_frames[direction][
                    self.animation_current
                ]
                self.last_direction = direction

    def animate_absolute(
        self, time: int, direction_vector: tuple[int | float, int | float] = (0, 0)
    ) -> None:
        """Set frame according to time (milliseconds)"""

        direction = None
        if direction_vector[0] == direction_vector[1] and direction_vector[0] == 0:
            direction = Direction.STATIC
        elif direction_vector[0] > 0:
            direction = Direction.RIGHT
        elif direction_vector[1] > 0:
            direction = Direction.DOWN
        elif direction_vector[0] < 0:
            direction = Direction.LEFT
        elif direction_vector[1] < 0:
            direction = Direction.UP

        if direction == Direction.STATIC:
            a = ""
            if self.last_direction == Direction.UP:
                a = "up"
            elif self.last_direction == Direction.DOWN:
                a = "down"
            elif self.last_direction == Direction.RIGHT:
                a = "right"
            elif self.last_direction == Direction.LEFT:
                a = "left"
            for i in self.animation_frames[direction]:
                if a in i:
                    self.texture_file = i

        elif direction is not None:
            frame_duration = self.animation_period * 1000

            self.animation_current = int(time // frame_duration) % len(
                self.animation_frames[direction]
            )
            self.texture_file = self.animation_frames[direction][self.animation_current]
            self.last_direction = direction
