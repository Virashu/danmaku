"""Menu button class declaration."""

from dataclasses import dataclass
from typing import Any

import pygame
from vgame.graphics import Graphics, Sprite


class ClickableButton(Sprite):
    """Menu button class clickable by mouse"""

    def __init__(
        self,
        text: str,
        rect: tuple[int | float, int | float, int | float, int | float] | pygame.Rect,
        text_color: tuple[int, int, int] = (0, 0, 0),
        button_color: tuple[int, int, int] = (255, 255, 255),
        font_size: int = 24,
    ):
        super().__init__()
        self.set_rect(pygame.Rect(rect))
        self.button_color = button_color
        self.text_color = text_color
        self.text = text
        self.font_size = font_size

    def draw(self, graphics: Graphics):
        graphics.rectangle(self.rect.topleft, self.rect.size, self.button_color)
        graphics.text(f" {self.text} ", self.rect.topleft, self.text_color)

    def is_clicked(self, mouse_pos: tuple[int | float, int | float]) -> bool:
        """Check if button is being clicked."""
        return self.rect.collidepoint(mouse_pos)

    def update(self, delta: int | float): ...


@dataclass
class Button:
    """Menu button for keyboard controls1"""

    text: str
    codename: str


class Cursor(Sprite):
    """Cursor class"""

    def __init__(self, xy: tuple[int, int]):
        super().__init__()
        self.x, self.y = xy
        self.width, self.height = 42, 40
        self.texture_file = "bullet.png"
        self.texture_size = (self.width, self.height)

    def update(self, delta: int | float):
        self.rect.x, self.rect.y, self.rect.w, self.rect.h = (
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height),
        )

    def draw(self, graphics: Graphics):
        graphics.draw_sprite(self)


class SettingsValue:
    """An interactive value bar for settings"""

    def __init__(
        self, name: str, display_name: str, possible_values: tuple[Any], value: Any
    ) -> None:
        self.codename = name
        self.text = display_name
        self.possible_values = possible_values
        self.value = value
        self.selection_index = self.possible_values.index(self.value)

    def increase(self):
        """Select next value"""
        self.selection_index = (self.selection_index + 1) % len(self.possible_values)
        self.value = self.possible_values[self.selection_index]

    def decrease(self):
        """Select previous value"""
        self.selection_index = (self.selection_index - 1) % len(self.possible_values)
        self.value = self.possible_values[self.selection_index]
