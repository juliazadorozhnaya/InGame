"""InGame module with main class of the game."""

from ingame.menu import MainMenu, SelectGameMenu, HelpPage
from ingame.CookieCutter.game import start_game
from ingame.game_settings import *


class InGame:
    """Main InGame class."""

    def __init__(self):
        """Initialize InGame."""
        pygame.init()
        self.running, self.playing = True, False
        self.click = False
        self.display = pygame.Surface((DISPLAY_W, DISPLAY_H))
        self.window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
        pygame.display.set_caption(SCREEN_TITLE)
        self.font_name = pygame.font.get_default_font()
        self.main_menu = MainMenu(self)
        self.select_menu = SelectGameMenu(self)
        self.help = HelpPage(self)
        self.load_images()

    def load_images(self):
        """Load menu images."""
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
        """Start game loop."""
        while self.playing:
            res = start_game(level=1, score=0, select_mode=False, game_screen=self.window)
            if type(res) is not int:
                self.playing = False
        self.main_menu.display_menu()

    def check_events(self):
        """Check events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.main_menu.run_display = False
                self.select_menu.run_display = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def draw_text(self, text, size, x, y):
        """Draw text."""
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
