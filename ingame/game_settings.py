"""Set module for InGame."""
import gettext
import locale
import os

import pygame


def get_abs_path(path):
    """Get absolute path."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

DISPLAY_W, DISPLAY_H = 800, 600

GAME_OVER_LOCATION = get_abs_path('images/game_over.png')
clock = pygame.time.Clock()

current_locale, encoding = locale.getdefaultlocale()
translation = gettext.translation('ingame', get_abs_path("translation"), [current_locale])
_, ngettext = translation.gettext, translation.ngettext

level_font = pygame.font.get_default_font()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (227, 62, 126)
YELLOW_BROWN = (198, 157, 111)
BROWN = (117, 48, 0)
DARK_BROWN = (175, 118, 43)
GRAY = (48, 49, 52)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "InGame"


class GameOverTimer:
    """Count down the time in minigames."""

    def __init__(self, timer_time):
        """
        Initialize GameOverTimer.

        :param timer_time: game time.
        """
        self.start_ticks = pygame.time.get_ticks()
        self.timer_time = timer_time

    def time_checker(self):
        """Check timer and return remaining time."""
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        timer = round(float(self.timer_time - elapsed_time), 1)
        return timer


def text_objects(text, color, font_name, font_size=20):
    """
    Create Text surface object.

    :param text: text of the message.
    :param color: color of the text.
    :param font_name: font name.
    :param font_size: font size.
    """
    text_font = pygame.font.Font(font_name, font_size)
    textSurface = text_font.render(text, True, color).convert_alpha()
    return textSurface


def message_to_screen_left(surface, msg, color, text_font, x, y, font_size=20):
    """
    Create message in the left corner of display surface.

    :param surface: display surface object.
    :param msg: text of the message.
    :param color: color of the text.
    :param font_name: font name.
    :param x: x coordinate of the text rectangle centre.
    :param y: y coordinate of the text rectangle centre.
    :param font_size: font size.
    """
    textSurf = text_objects(msg, color, text_font)
    cur_w, cur_h = surface.get_size()
    txt_w, txt_h = textSurf.get_size()
    textSurf = pygame.transform.smoothscale(textSurf, (txt_w, txt_h))
    textRect = textSurf.get_rect()
    textRect.center = x, y
    surface.blit(textSurf, textRect)


def message_to_screen_center(surface, msg, color, text_font, y, font_size=20):
    """
    Create message in the screen_center.

    :param surface: display surface object.
    :param msg: text of the message.
    :param color: color of the text.
    :param font_name: font name.
    :param y: y coordinate of the text rectangle centre.
    :param font_size: font size.
    """
    textSurf = text_objects(msg, color, text_font, font_size)
    txt_w, txt_h = textSurf.get_size()
    textSurf = pygame.transform.smoothscale(textSurf, (txt_w, txt_h))
    textRect = textSurf.get_rect()
    textRect.center = surface.get_width() / 2, y
    surface.blit(textSurf, textRect)
