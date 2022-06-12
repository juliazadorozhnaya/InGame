import pygame

from ingame.menu import MainMenu, SelectGameMenu, HelpPage
from ingame.CookieCutter.game import start_game


class InGame:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.click = False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = (
            False,
            False,
            False,
            False,
        )
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = pygame.font.get_default_font()
        self.PINK = (198, 157, 111)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.main_menu = MainMenu(self)
        self.select_menu = SelectGameMenu(self)
        self.help = HelpPage(self)
        self.load_images()

    def load_images(self):
        self.img_play_button = pygame.image.load("ingame/images/menu/button_play.png")
        self.img_select_button = pygame.image.load("ingame/images/menu/button_select.png")
        self.img_help_button = pygame.image.load("ingame/images/menu/button_help.png")
        self.img_exit_button = pygame.image.load("ingame/images/menu/button_exit.png")
        self.img_back_button = pygame.image.load("ingame/images/menu/button_back.png")
        self.img_lvl1_button = pygame.image.load("ingame/images/menu/lvl1.png")
        self.img_lvl2_button = pygame.image.load("ingame/images/menu/lvl2.png")
        self.img_lvl3_button = pygame.image.load("ingame/images/menu/lvl3.png")
        self.img_lvl4_button = pygame.image.load("ingame/images/menu/lvl4.png")
        self.img_lvl5_button = pygame.image.load("ingame/images/menu/lvl5.png")

    def game_loop(self):
        while self.playing:
            res = start_game(level=1, score=0, select_mode=False, game_screen=self.window)
            if type(res) is not int:
                self.playing = False
        self.main_menu.display_menu()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.main_menu.run_display = False
                self.select_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # enter
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = (
            False,
            False,
            False,
            False,
        )

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
