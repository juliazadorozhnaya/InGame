"""Menu module for InGame."""

from .lvl1_game import start_game as start_game_1
from .lvl2_game import start_game as start_game_2
from .lvl3_game import start_game as start_game_3
from .game_settings import *


class Menu:
    """Menu base class."""

    def __init__(self, game):
        """
        Initialize Menu object.

        : param game: InGame object.
        """
        self.game = game
        self.mid_w, self.mid_h = DISPLAY_W / 2, DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        """Draw cursor."""
        self.game.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)

    def button(self, x, y, img_button):
        """
        Draw button.

        :param x: x coordinate of the button top left corner.
        :param y: y coordinate of the button top left corner.
        :param image: image of the button.
        """
        button = img_button.get_rect()
        button.topleft = (x, y)
        self.game.window.blit(img_button, (x, y))
        return button


class MainMenu(Menu):
    """Main menu class."""

    def __init__(self, game):
        """
        Initialize Menu object.

        : param game: InGame object.
        """
        Menu.__init__(self, game)
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def draw_menu(self):
        """Draw menu."""
        return (
            self.button(DISPLAY_W / 3, DISPLAY_H / 10, self.game.img_play_button),
            self.button(DISPLAY_W / 3, DISPLAY_H / 3.1, self.game.img_select_button),
            self.button(DISPLAY_W / 3, DISPLAY_H / 1.85, self.game.img_help_button),
            self.button(DISPLAY_W / 3, DISPLAY_H / 1.32, self.game.img_exit_button),
        )

    def display_menu(self):
        """Display menu."""
        self.game.click = False
        self.run_display = True
        while self.run_display:
            self.game.window.blit(self.game.display, (0, 0))
            self.game.display.fill(YELLOW_BROWN)
            mx, my = pygame.mouse.get_pos()
            button_play, button_select, button_help, button_exit = self.draw_menu()
            if button_play.collidepoint((mx, my)):
                if self.game.click:
                    self.game.click = False
                    self.run_display = False
                    self.game.playing = True
                    return self.game.game_loop()
            elif button_select.collidepoint((mx, my)):
                if self.game.click:
                    self.game.click = False
                    self.run_display = False
                    return self.game.select_menu.display_menu()
            elif button_help.collidepoint((mx, my)):
                if self.game.click:
                    self.game.click = False
                    self.run_display = False
                    return self.game.help.display_menu()
            elif button_exit.collidepoint((mx, my)):
                if self.game.click:
                    self.game.click = False
                    self.run_display = False
                    self.running = False
                    return 0

            self.game.check_events()
            self.game.draw_text("InGame", 40, DISPLAY_W / 2, DISPLAY_H / 2 - 260)
            pygame.display.update()


class SelectGameMenu(Menu):
    """Selection menu class."""

    def __init__(self, game):
        """
        Initialize Menu object.

        : param game: InGame object.
        """
        Menu.__init__(self, game)

    def draw_select_menu(self):
        """Draw select menu."""
        return (
            self.button(DISPLAY_W / 25, DISPLAY_H / 20, self.game.img_lvl1_button),
            self.button(DISPLAY_W / 2.8, DISPLAY_H / 3, self.game.img_lvl2_button),
            self.button(DISPLAY_W / 1.49, DISPLAY_H / 20, self.game.img_lvl3_button),
            self.button(DISPLAY_W / 3, DISPLAY_H / 1.3, self.game.img_back_button),
        )

    def display_menu(self):
        """Display select menu."""
        self.run_display = True
        self.game.click = False
        while self.run_display:
            self.game.window.blit(self.game.display, (0, 0))
            self.game.display.fill(YELLOW_BROWN)
            mx, my = pygame.mouse.get_pos()
            (
                button_l1,
                button_l2,
                button_l3,
                button_back,
            ) = self.draw_select_menu()
            if button_l1.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.game.playing = True
                    level = 1
                    score = 0
                    while self.game.playing:
                        res = start_game_1(level=level, score=score, select_mode=True)
                        if type(res) is not int:
                            self.game.playing = False
                        else:
                            level += 1
                            score += res
                    return self.game.select_menu.display_menu()
            elif button_l2.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.game.playing = True
                    level = 1
                    score = 0
                    while self.game.playing:
                        res = start_game_2(
                            level=level,
                            score=score,
                            select_mode=True,
                            game_screen=self.game.window,
                        )
                        if type(res) is not int:
                            self.game.playing = False
                        else:
                            level += 1
                            score += res
                    return self.game.select_menu.display_menu()
            elif button_l3.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.game.playing = True
                    level = 1
                    score = 0
                    while self.game.playing:
                        res = start_game_3(level=level, score=score, select_mode=True)
                        if type(res) is not int:
                            self.game.playing = False
                        else:
                            level += 1
                            score += res
                    return self.game.select_menu.display_menu()
            elif button_back.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.running = False
                    return self.game.main_menu.display_menu()

            self.game.check_events()

            self.game.draw_text(
                "Select Level",
                40,
                DISPLAY_W / 2,
                DISPLAY_H / 2 - 260,
            )
            pygame.display.update()


class HelpPage(Menu):
    """Help page class."""

    def __init__(self, game):
        """
        Initialize Help page.

        : param game: InGame object.
        """
        Menu.__init__(self, game)

    def display_menu(self):
        """Display Help page."""
        self.run_display = True
        self.game.click = False
        while self.run_display:
            self.game.window.blit(self.game.display, (0, 0))
            self.game.display.fill(YELLOW_BROWN)
            mx, my = pygame.mouse.get_pos()
            button_back = self.button(
                DISPLAY_W / 3,
                DISPLAY_H / 1.3,
                self.game.img_back_button,
            )

            if button_back.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.running = False
                    return self.game.main_menu.display_menu()

            self.game.check_events()

            self.game.draw_text(
                "About InGame",
                40,
                DISPLAY_W / 2,
                DISPLAY_H / 2 - 260,
            )
            self.game.draw_text(
                "First game: Red Light-Green Light.",
                25,
                DISPLAY_W / 3,
                DISPLAY_H / 2 - 210,
            )
            self.game.draw_text(
                "The essence of the game is that you need to have time to reach the Doll before it",
                20,
                DISPLAY_W / 2.0,
                DISPLAY_H / 2 - 180,
            )
            self.game.draw_text(
                "turns around and starts aiming. To save your life, you need to avoid the guards,",
                20,
                DISPLAY_W / 2.01,
                DISPLAY_H / 2 - 160,
            )
            self.game.draw_text(
                "who walk around the doll throughout the game. ",
                20,
                DISPLAY_W / 3.3,
                DISPLAY_H / 2 - 140,
            )
            self.game.draw_text(
                "Second Game: Cookie Cutter.",
                25,
                DISPLAY_W / 3.3,
                DISPLAY_H / 2 - 100,
            )
            self.game.draw_text(
                "In this game, it is necessary to carefully draw the needle along the contour of",
                20,
                DISPLAY_W / 2.09,
                DISPLAY_H / 2 - 75,
            )
            self.game.draw_text(
                "the cookie for 40 seconds without touching the red dots.",
                20,
                DISPLAY_W / 2.85,
                DISPLAY_H / 2 - 50,
            )
            self.game.draw_text(
                "Third game: Tug of War.",
                25,
                DISPLAY_W / 3.9,
                DISPLAY_H / 2 - 20,
            )
            self.game.draw_text(
                "The essence of this test is that it is necessary to have time to pull the rope",
                20,
                DISPLAY_W / 2.15,
                DISPLAY_H / 2 + 5,
            )
            self.game.draw_text(
                "within 40 seconds, relying on the commands on the game screen.",
                20,
                DISPLAY_W / 2.4,
                DISPLAY_H / 2 + 30,
            )
            pygame.display.update()
