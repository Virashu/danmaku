import pygame


class Button:
    def __init__(self, coords, button_color, text, text_color, font_size):
        self.x, self.y = coords
        self.button_color = button_color
        self.text_color = text_color
        self.text = " " + text + " "
        self.font_size = font_size
        self.font = pygame.font.SysFont("Segoe UI", self.font_size)
        self.img = self.font.render(self.text, True, self.text_color)
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, self.rect)
        screen.blit(self.img, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
