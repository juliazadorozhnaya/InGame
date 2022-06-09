import random

import pygame

from ingame.CookieCutter import game_object
from ingame.CookieCutter.constants import *
from ingame.CookieCutter.game_object import NPC
from ingame.game_settings import *


class Game:
    NPC_CHANGE_DIRECTION_TIME = 3
    NPC_SIZE = 150

    def __init__(self, ingame, current_screen):
        self.ingame = ingame
        # Screen set-up
        self.game_screen = ingame.window
        self.game_screen.fill(PINK)
        self.shape = random.randrange(CIRCLE, STAR + 1)
        self.rectangle_size = DISPLAY_W / RECTANGLE_SHAPE_SIZE_RATIO
        self.half_rectangle = self.rectangle_size / 2
        self.notice_message = True

        self.pin_image = pygame.image.load(PIN_LOCATION)
        self.npc_size = DISPLAY_W / NPC_SIZE_RATIO
        pygame.event.get()

    def start_game(self, level, score, select_mode):
        npc = NPC(self.ingame, self.npc_size, self.npc_size, KIND_OF_NPC)

        minigame = game_object.CookieCutter(self.game_screen, NUMBER_OF_POINTS, self.shape)
        game_over_timer = GameOverTimer(GAME_TIME)
        NPC_ticks = pygame.time.get_ticks()

        while True:
            left_time = game_over_timer.time_checker()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return

            self.game_screen.fill(PINK)

            message_to_screen_left(
                self.game_screen, 'Level:' + str(level), WHITE, font_name, self.game_screen.get_width() / 11,
                                  self.game_screen.get_height() / 30, DISPLAY_W,
                DISPLAY_H)
            message_to_screen_left(
                self.game_screen, "GAME OVER : " + str(left_time), WHITE, font_name,
                                  self.game_screen.get_width() / 4.8, self.game_screen.get_height() / 14, DISPLAY_W,
                DISPLAY_H)
            message_to_screen_left(
                self.game_screen, "SCORE : " + str(round(score)), BLACK, font_name, self.game_screen.get_width() / 1.2,
                                  self.game_screen.get_height() / 23, DISPLAY_W,
                DISPLAY_H)

            pygame.draw.circle(self.game_screen, YELLOW_BROWN,
                               (self.game_screen.get_width() / 2, self.game_screen.get_height() / 2),
                               int(DISPLAY_W * DALGONA_SIZE_RATIO * self.game_screen.get_width() / DISPLAY_W),
                               int(DISPLAY_W * DALGONA_SIZE_RATIO * self.game_screen.get_width() / DISPLAY_W))

            if self.shape == CIRCLE:
                pygame.draw.circle(self.game_screen, DARK_BROWN,
                                   (self.game_screen.get_width() / 2, self.game_screen.get_height() / 2),
                                   int(
                                       DISPLAY_W * CIRCLE_SHAPE_SIZE_RATIO * self.game_screen.get_width() / DISPLAY_W),
                                   int(DISPLAY_W * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / DISPLAY_H))
            elif self.shape == RECTANGLE:
                pygame.draw.rect(self.game_screen, DARK_BROWN,
                                 [(DISPLAY_W / 2 - self.half_rectangle) * (
                                         self.game_screen.get_width() / DISPLAY_W),
                                  (DISPLAY_H / 2 - self.half_rectangle) * (
                                          self.game_screen.get_height() / DISPLAY_H),
                                  self.rectangle_size * (self.game_screen.get_width() / DISPLAY_W),
                                  self.rectangle_size * (self.game_screen.get_height() / DISPLAY_H)],
                                 int(DISPLAY_W * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / DISPLAY_W),
                                 border_radius=RECTANGLE_BORDER_RADIUS)
            elif self.shape == TRIANGLE:
                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [[DISPLAY_W / 2 * (self.game_screen.get_width() / DISPLAY_W),
                                      DISPLAY_H / 4 * (self.game_screen.get_height() / DISPLAY_H)],
                                     [(DISPLAY_W / 4 + TRIANGLE_ERROR) * (self.game_screen.get_width() / DISPLAY_W),
                                      DISPLAY_H * (2 / 3) * (self.game_screen.get_height() / DISPLAY_H)],
                                     [(DISPLAY_W * (3 / 4) - TRIANGLE_ERROR) * (
                                             self.game_screen.get_width() / DISPLAY_W),
                                      DISPLAY_H * (2 / 3) * (self.game_screen.get_height() / DISPLAY_H)]],
                                    int(DISPLAY_W * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / DISPLAY_W))
            elif self.shape == STAR:
                side_length = DISPLAY_W / 2
                half_side_length = side_length / 2
                ratio = math.sqrt(3)

                center = (DISPLAY_W / 2, DISPLAY_H / 2)
                point1 = [center[0] * (self.game_screen.get_width() / DISPLAY_W),
                          (center[1] - (half_side_length * ratio * (2 / 3))) * (
                                  self.game_screen.get_height() / DISPLAY_H)]
                point2 = [(center[0] - side_length / 2) * (self.game_screen.get_width() / DISPLAY_W),
                          (center[1] + (half_side_length / ratio)) * (self.game_screen.get_height() / DISPLAY_H)]
                point3 = [(center[0] + side_length / 2) * (self.game_screen.get_width() / DISPLAY_W),
                          (center[1] + (half_side_length / ratio)) * (self.game_screen.get_height() / DISPLAY_H)]
                reverse_point1 = [center[0] * (self.game_screen.get_width() / DISPLAY_W),
                                  (center[1] + (half_side_length * ratio * (2 / 3))) * (
                                          self.game_screen.get_height() / DISPLAY_H)]
                reverse_point2 = [(center[0] - side_length / 2) * (self.game_screen.get_width() / DISPLAY_W),
                                  (center[1] - (half_side_length / ratio)) * (
                                          self.game_screen.get_height() / DISPLAY_H)]
                reverse_point3 = [(center[0] + side_length / 2) * (self.game_screen.get_width() / DISPLAY_W),
                                  (center[1] - (half_side_length / ratio)) * (
                                          self.game_screen.get_height() / DISPLAY_H)]

                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [point1, point2, point3],
                                    int(DISPLAY_W * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / DISPLAY_W))
                pygame.draw.polygon(self.game_screen, DARK_BROWN,
                                    [reverse_point1, reverse_point2, reverse_point3],
                                    int(DISPLAY_W * SHAPE_WIDTH_RATIO * self.game_screen.get_width() / DISPLAY_W))

            minigame.draw()

            pygame.event.get()
            if pygame.mouse.get_pressed()[0]:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = pygame.mouse.get_pos()[1]
                self.game_screen.blit(self.pin_image, (x_pos, y_pos - self.pin_image.get_size()[1]))

            npc.BASE_SPEED = NPC_SPEED
            npc.move(DISPLAY_W)
            npc.draw(self.game_screen)
            NPC_elapsed_time = (pygame.time.get_ticks() - NPC_ticks) / 1000
            NPC_timer = round(float(self.NPC_CHANGE_DIRECTION_TIME - NPC_elapsed_time), 1)
            if NPC_timer <= 0:
                npc.change_direction()
                NPC_ticks = pygame.time.get_ticks()
                NPC_elapsed_time = (pygame.time.get_ticks() - NPC_ticks) / 1000

                minigame.change_wrong_points()
                self.notice_message = False

            elif NPC_timer > 0 and level == STARTING_LEVEL and self.notice_message:
                message_to_screen_center(self.game_screen, 'Avoid red dots.', WHITE, font_name,
                                         self.game_screen.get_height() / 2,
                                         DISPLAY_W,
                                         DISPLAY_H)

            if minigame.check_win()["is_success"] is True:
                message_to_screen_center(self.game_screen, 'Pass!', WHITE, font_name,
                                         self.game_screen.get_height() / 3,
                                         DISPLAY_W,
                                         DISPLAY_H)

                if select_mode:
                    message_to_screen_center(self.game_screen, 'Next level!', WHITE, font_name,
                                             self.game_screen.get_height() / 2,
                                             DISPLAY_W,
                                             DISPLAY_H)
                else:
                    message_to_screen_center(self.game_screen, 'Next game', WHITE, font_name,
                                             self.game_screen.get_height() / 2,
                                             DISPLAY_W,
                                             DISPLAY_H)

                pygame.display.update()
                clock.tick(0.5)
                return round(left_time)
            if left_time <= 0 or minigame.check_win()["wrong_point_clicked"]:
                game_over_image = pygame.image.load(GAME_OVER_LOCATION)
                game_over_image = pygame.transform.scale(game_over_image, (
                    game_over_image.get_width() * (self.game_screen.get_width() / DISPLAY_W),
                    game_over_image.get_height() * (self.game_screen.get_height() / DISPLAY_H)))
                self.game_screen.blit(game_over_image, SCREEN_STARTING_POINT)
                message_to_screen_center(self.game_screen, "Game Over", RED, font_name, self.game_screen.get_height() / 2,
                                         DISPLAY_W,
                                         DISPLAY_H)
                pygame.display.update()
                clock.tick(0.5)
                pygame.mixer.music.stop()
                return

            re_x = self.game_screen.get_width()
            re_y = self.game_screen.get_height()
            if (re_x / re_y) != (DISPLAY_W / DISPLAY_H):
                resize_screen = pygame.display.set_mode((re_x, re_x), pygame.RESIZABLE)
            if re_x > DISPLAY_W or re_y > DISPLAY_H:
                resize_screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H), pygame.RESIZABLE)

            pygame.display.update()
            clock.tick(FPS_RATE)


def start_game(level, score, select_mode, ingame):
    current_screen = pygame.display.get_window_size()
    new_game = Game(ingame, current_screen)
    return new_game.start_game(level, score, select_mode)
