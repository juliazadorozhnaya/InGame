"""CookieCutter game module."""

import random

import pygame

from ingame.CookieCutter import game_object
from ingame.CookieCutter.constants import *
from ingame.game_settings import *
from ingame.game_settings import _


class Game:
    """CookieCutter game class."""

    def __init__(self, game_screen):
        """
        Initialize CookieCutter game.

        :param game_screen: game screen.
        """
        # Screen set-up
        self.game_screen = game_screen
        self.game_screen.fill(PINK)
        self.shape = random.randrange(1, 4)
        self.rectangle_size = DISPLAY_W / RECTANGLE_SHAPE_SIZE_RATIO
        self.half_rectangle = self.rectangle_size / 2
        self.notice_message = True

        self.pin_image = pygame.image.load(PIN_LOCATION)
        self.cookie = Background(COOKIE_LOCATION, [0, 0])
        self.background = Background(BACKGROUND_LOCATION, [0, 0])
        pygame.event.get()

    def start_game(self, level, score, select_mode):
        """Start game."""
        minigame = game_object.CookieCutter(self.game_screen, NUMBER_OF_POINTS, self.shape)
        game_over_timer = GameOverTimer(GAME_TIME)

        while True:
            left_time = game_over_timer.time_checker()

            if left_time % 10 == 0:
                minigame.change_wrong_points()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.game_screen.fill(PINK)
            self.game_screen.blit(self.background.image, self.background.rect)
            self.game_screen.blit(self.cookie.image, self.cookie.rect)

            message_to_screen_left(
                self.game_screen, _('Level : {}').format(level), PINK, font_name,
                self.game_screen.get_width() / 11,
                self.game_screen.get_height() / 30)
            message_to_screen_left(
                self.game_screen, _('Time : {}').format(left_time), PINK, font_name,
                self.game_screen.get_width() / 11,
                self.game_screen.get_height() / 11)
            message_to_screen_left(
                self.game_screen, _('Score : {}').format(round(score)), PINK, font_name,
                self.game_screen.get_width() / 1.2,
                self.game_screen.get_height() / 23)

            minigame.draw()

            pygame.event.get()
            if pygame.mouse.get_pressed()[0]:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = pygame.mouse.get_pos()[1]
                self.game_screen.blit(self.pin_image, (x_pos, y_pos - self.pin_image.get_size()[1]))

            elif level == STARTING_LEVEL and self.notice_message:
                message_to_screen_center(self.game_screen, _('Avoid red dots.'), WHITE, font_name,
                                         self.game_screen.get_height() / 2)

            if minigame.check_win()["is_success"] is True:
                message_to_screen_center(self.game_screen, _('Level {} passed!').format(level),
                                         WHITE, font_name,
                                         self.game_screen.get_height() / 3)

                if select_mode:
                    message_to_screen_center(self.game_screen, _('Next round'),
                                             WHITE, font_name,
                                             self.game_screen.get_height() / 2)
                else:
                    message_to_screen_center(self.game_screen, _('Next level'),
                                             WHITE, font_name,
                                             self.game_screen.get_height() / 2)

                pygame.display.update()
                clock.tick(0.5)
                return round(left_time)
            if left_time <= 0 or minigame.check_win()["wrong_point_clicked"]:
                game_over_img = pygame.image.load(GAME_OVER_LOCATION)
                self.game_screen.fill(BLACK)
                game_over_image = pygame.transform.scale(game_over_img, (DISPLAY_H, DISPLAY_H))
                self.game_screen.blit(game_over_image,
                                      ((DISPLAY_W - game_over_image.get_width()) // 2, 0))
                message_to_screen_center(self.game_screen, _('Game Over'),
                                         RED, font_name,
                                         self.game_screen.get_height() / 4,
                                         font_size=40)
                pygame.display.update()
                clock.tick(0.5)
                return

            pygame.display.update()
            clock.tick(FPS_RATE)


class Background(pygame.sprite.Sprite):
    """Background class."""

    def __init__(self, image_file, location):
        """
        Initialize Background.

        :param image_file: image of background.
        :param location: coordinate of the top left corner of background location.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def start_game(level, score, select_mode, game_screen):
    """
    Start CookieCutter game.

    :param level: level.
    :param score: current score.
    :param select_mode: training mode if True, playin otherwise.
    :param game_screen: game screen.
    """
    new_game = Game(game_screen)
    return new_game.start_game(level, score, select_mode)
