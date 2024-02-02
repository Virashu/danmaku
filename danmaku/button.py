import pygame
import vgame


class Button(vgame.graphics.Sprite):
    def __init__(
        self,
        coords: tuple[int | float, int | float],
        width: int | float,
        height: int | float,
        button_color: tuple[int, int, int],
        text: str,
        text_color: tuple[int, int, int] = (0, 0, 0),
        font_size: int = 24,
    ):
        self.x, self.y = coords
        self.set_rect(pygame.Rect(coords, (width, height)))
        self.button_color = button_color
        self.text_color = text_color
        self.text = " " + text + " "
        self.font_size = font_size

    def draw(self, graphics: vgame.graphics.Graphics):
        graphics.rectangle(
            (self.x, self.y), (self.rect.w, self.rect.h), self.button_color
        )
        graphics.text(self.text, (self.x, self.y), self.text_color)

    def is_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
