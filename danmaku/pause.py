import pygame
from danmaku.button import Button
import vgame


class Menu(vgame.Scene):
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        if self.name == "main":
            self.new_game = False
            self.last_game = False
            self.status = self.new_game or self.last_game
        if self.name == "pause":
            self.start = False
            self.to_menu = False
            self.save = False
            self.status = self.start or self.to_menu or self.save

    def load(self):
        pygame.init()
        SCREEN = pygame.display.set_mode((self.width, self.height))
        if self.name == "main":
            self.new_game_button = Button(
                (self.width // 4, self.height // 3),
                (255, 0, 0),
                "New game",
                (0, 0, 255),
                42,
            )
            self.continue_button = Button(
                (self.width // 4 + 10, self.height // 3 + 50),
                (255, 0, 0),
                "Continue",
                (0, 0, 255),
                42,
            )
            self.settings_button = Button(
                (self.width // 4 + 13, self.height // 3 + 100),
                (255, 0, 0),
                "Settings",
                (0, 0, 255),
                42,
            )

        if self.name == "pause":
            self.start_button = Button(
                (self.width // 4, self.height // 3),
                (255, 0, 0),
                "Continue",
                (0, 0, 255),
                42,
            )
            self.to_menu_button = Button(
                (self.width // 4, self.height // 3 + 50),
                (255, 0, 0),
                "New game",
                (0, 0, 255),
                42,
            )
            self.save_button = Button(
                (self.width // 5, self.height // 3 + 100),
                (255, 0, 0),
                "Save and exit",
                (0, 0, 255),
                42,
            )

        while not self.status:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.name == "main":
                        if self.new_game_button.is_clicked(pygame.mouse.get_pos()):
                            self.new_game = True
                        if self.continue_button.is_clicked(pygame.mouse.get_pos()):
                            self.last_game = True
                        if self.settings_button.is_clicked(pygame.mouse.get_pos()):
                            pass
                        self.status = self.new_game or self.last_game
                    if self.name == "pause":
                        if self.start_button.is_clicked(pygame.mouse.get_pos()):
                            self.start = True
                        if self.to_menu_button.is_clicked(pygame.mouse.get_pos()):
                            self.to_menu = True
                        if self.save_button.is_clicked(pygame.mouse.get_pos()):
                            self.save = True
                        self.status = self.start or self.to_menu or self.save
            SCREEN.fill((0, 0, 0))
            if self.name == "main":
                self.new_game_button.draw(SCREEN)
                self.continue_button.draw(SCREEN)
                self.settings_button.draw(SCREEN)
            if self.name == "pause":
                self.start_button.draw(SCREEN)
                self.to_menu_button.draw(SCREEN)
                self.save_button.draw(SCREEN)
            pygame.display.flip()
