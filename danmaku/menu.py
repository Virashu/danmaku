import pygame
from danmaku.button import Button
from danmaku.database import get_game_history, get_saved_objects


class Menu:
    def __init__(self, name, WIDTH, HEIGHT):
        self.name = name
        self.width = WIDTH
        self.height = HEIGHT
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
                (self.width // 5, self.height // 3),
                (64, 224, 208),
                "New game",
                (0, 0, 139),
                36,
            )
            self.continue_button = Button(
                (self.width // 4, self.height // 3 + 50),
                (112, 128, 144),
                "Continue",
                (0, 0, 139),
                36,
            )
            if get_saved_objects():
                self.continue_button.button_color = (64, 224, 208)
            self.settings_button = Button(
                (self.width // 4 + 10, self.height // 3 + 100),
                (64, 224, 208),
                "Settings",
                (0, 0, 139),
                36,
            )
            self.history_button = Button(
                (self.width // 8, self.height // 3 + 150),
                (64, 224, 208),
                "Games history",
                (0, 0, 139),
                36,
            )

        if self.name == "pause":
            self.start_button = Button(
                (self.width // 4, self.height // 3),
                (64, 224, 208),
                "Continue",
                (0, 0, 139),
                36,
            )
            self.to_menu_button = Button(
                (self.width // 4, self.height // 3 + 50),
                (64, 224, 208),
                "New game",
                (0, 0, 139),
                36,
            )
            self.save_button = Button(
                (self.width // 5, self.height // 3 + 100),
                (64, 224, 208),
                "Save and exit",
                (0, 0, 139),
                36,
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
                            if get_saved_objects():
                                self.continue_button.button_color = (64, 224, 208)
                                self.last_game = True
                        if self.settings_button.is_clicked(pygame.mouse.get_pos()):
                            pass
                        if self.history_button.is_clicked(pygame.mouse.get_pos()):
                            pygame.init()
                            draw = True
                            SCREEN = pygame.display.set_mode((self.width, self.height))
                            exit_button = Button(
                                (self.width // 3 + 10, self.height - 60),
                                (64, 224, 208),
                                "Exit",
                                (0, 0, 139),
                                36,
                            )
                            while draw:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        quit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if exit_button.is_clicked(pygame.mouse.get_pos()):
                                            draw = False
                                SCREEN.fill((0, 0, 0))
                                history = get_game_history()
                                font = pygame.font.SysFont("Segoe UI", 20)
                                x, y = 20, 20
                                for i in history:
                                    self.img = font.render(f"Level: {i['level'] + 1}, Score: {i['score']}",
                                                           True, (0, 191, 255))
                                    SCREEN.blit(self.img, (x, y))
                                    y += 20
                                exit_button.draw(SCREEN)
                                pygame.display.flip()
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
                self.history_button.draw(SCREEN)
            if self.name == "pause":
                self.start_button.draw(SCREEN)
                self.to_menu_button.draw(SCREEN)
                self.save_button.draw(SCREEN)
            pygame.display.flip()
