import pygame
from button import Button


class Menu:
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.new_game = False
        self.last_game = False

    def load(self):
        pygame.init()
        SCREEN = pygame.display.set_mode((self.width, self.height))
        CLOCK = pygame.time.Clock()
        new_game_button = Button((self.width // 4, self.height // 3), (255, 0, 0), "New game", (0, 0, 255), 42)
        continue_button = Button((self.width // 4 + 10, self.height // 3 + 50), (255, 0, 0), "Continue", (0, 0, 255), 42)
        settings_button = Button((self.width // 4 + 13, self.height // 3 + 100), (255, 0, 0), "Settings", (0, 0, 255), 42)

        while not self.new_game and not self.last_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_button.is_clicked(pygame.mouse.get_pos()):
                        self.new_game = True
                    if continue_button.is_clicked(pygame.mouse.get_pos()):
                        self.last_game = True
                    if settings_button.is_clicked(pygame.mouse.get_pos()):
                        pass
            SCREEN.fill((0, 0, 0))
            new_game_button.draw(SCREEN)
            continue_button.draw(SCREEN)
            settings_button.draw(SCREEN)
            pygame.display.flip()
            CLOCK.tick(60)