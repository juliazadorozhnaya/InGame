import random
import pygame.time
from ingame.game_settings import *

# Location of images
PULLING_IMG = "ingame/TugOfWar/Images/pulling.png"
HOLDING_IMG = "ingame/TugOfWar/Images/holding.png"
BACKGROUND_LOCATION = "ingame/TugOfWar/Images/TugOfWarBack.png"
RANDOM_NUMBER_FOR_TIMER = random.randint(3, 6)
FPS_RATE = 150

level_font = pygame.font.get_default_font()


class TugOfWar:
    """A class that implements the game itself."""

    NUMBER_OF_PRESS_KEY_TO_CLEAR = 30  # Winning conditions.
    CONDITION_OF_GAME_OVER = 70
    TOTAL_TIME = 40
    POWER_OF_ENEMY = 0.1
    MY_POWER = 0.2

    def __init__(self, width, height, current_screen):
        self.width = width
        self.height = height
        # Screen settings.
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.ref_w, self.ref_h = self.screen.get_size()
        self.screen.fill(WHITE)
        # Loading images.
        self.character_pull = pygame.image.load(PULLING_IMG)
        self.character_hold = pygame.image.load(HOLDING_IMG)
        self.background = pygame.image.load(BACKGROUND_LOCATION)
        # Timer setting.
        self.game_over_timer = None

    def start_game(self, level, score, select_mode=False):
        score = self.run_game_loop(level, score, select_mode)
        return score

    def win_game(self):
        
        while True:
            message_to_screen_center(
                self.screen,
                "Congratulations! You have passed the game.",
                BLUE,
                level_font,
                self.screen.get_height() / 4,
                font_size=40
            )
            message_to_screen_center(
                self.screen,
                "To go to the home screen, press R.",
                BLUE,
                level_font,
                self.screen.get_height() / 3,
                font_size=40
            )
            message_to_screen_center(
                self.screen,
                "To exit the game, press Q.",
                BLUE,
                level_font,
                self.screen.get_height() / 2,
                font_size=40
            )
            pygame.display.update()

    # Failure screen.
    def lose_game(self):
        game_over_img = pygame.image.load(GAME_OVER_LOCATION)
        self.screen.fill(BLACK)
        game_over_image = pygame.transform.scale(game_over_img, (DISPLAY_H, DISPLAY_H))
        self.screen.blit(game_over_image,
                                ((DISPLAY_W - game_over_image.get_width()) // 2, 0))
        message_to_screen_center(self.screen, 'Game Over',
                                    RED, level_font,
                                    self.screen.get_height() / 4,
                                    font_size=40)
        pygame.display.update()
        clock.tick(1)

    def run_game_loop(self, level, score, select_mode):
        game_over = False
        did_win = False
        hit_time_init = True
        num_of_pressed = 0
        num_of_press_key_to_clear = self.NUMBER_OF_PRESS_KEY_TO_CLEAR
        condition_of_game_over = self.CONDITION_OF_GAME_OVER
        hit_time = RANDOM_NUMBER_FOR_TIMER  # A pressable time.
        hold_time = RANDOM_NUMBER_FOR_TIMER
        left_time = None
        power_of_enemy = level * self.POWER_OF_ENEMY

        self.game_over_timer = GameOverTimer(self.TOTAL_TIME)

        start_ticks = pygame.time.get_ticks()
        hit_ticks = pygame.time.get_ticks()

        while not game_over:
            # Remaining time of the game end timer.
            left_time = self.game_over_timer.time_checker()

            self.screen.fill(WHITE)
            image_background = pygame.transform.scale(
                self.background, (self.screen.get_width(), self.screen.get_height())
            )
            
            self.screen.blit(image_background, (0, 0))
            pulling_characters = pygame.transform.scale(
                self.character_pull, (self.screen.get_width(), self.screen.get_height())
            )
            holding_characters = pygame.transform.scale(
                self.character_hold, (self.screen.get_width(), self.screen.get_height())
            )

            # Holding timer.
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            hold_timer = round(float(hold_time - elapsed_time), 1)

            # Current level, game over timer render on top left of screen.
            message_to_screen_left(
                self.screen,
                "Level : " + str(level),
                WHITE,
                level_font,
                self.screen.get_width() / 11,
                self.screen.get_height() / 30
            )
            message_to_screen_left(
                self.screen,
                "GAME OVER : " + str(left_time),
                WHITE,
                level_font,
                self.screen.get_width() / 4.8,
                self.screen.get_height() / 14
            )
            message_to_screen_left(
                self.screen,
                "SCORE : " + str(round(score)),
                WHITE,
                level_font,
                self.screen.get_width() / 1.2,
                self.screen.get_height() / 23
            )
            message_to_screen_center(
                self.screen,
                "To victory {} M".format(int(num_of_press_key_to_clear - num_of_pressed)),
                WHITE,
                level_font,
                self.screen.get_height() / 4
            )

            # Hold time.
            if hold_timer > 0:
                self.screen.blit(
                    holding_characters,
                    ((num_of_press_key_to_clear - num_of_pressed), 0),
                )
                message_to_screen_center(
                    self.screen,
                    "Quickly press Space.",
                    WHITE,
                    level_font,
                    self.screen.get_height() * (2 / 3)
                )
            # Hit time.
            if hold_timer <= 0:
                self.screen.blit(
                    pulling_characters,
                    ((num_of_press_key_to_clear - num_of_pressed), 0),
                )
                if hit_time_init:
                    hit_time = RANDOM_NUMBER_FOR_TIMER
                    hit_time_init = False
                hit_time_checker = round(hit_time - (hold_timer) * (-1), 1)
                message_to_screen_center(
                    self.screen,
                    "← → Quickly press one of the buttons!",
                    WHITE,
                    level_font,
                    self.screen.get_height() * (2 / 3),
                    font_size=40
                )

                if hit_time_checker <= 0: # Reset the holding timer after the end of the battering time.
                    hit_time_init = True
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    hold_time = RANDOM_NUMBER_FOR_TIMER
                    hold_timer = round(float(hold_time - elapsed_time), 1)
                else:
                    hit_elapsed_time = (pygame.time.get_ticks() - hit_ticks) / 1000
                    hit_timer = round(float(hit_time - hit_elapsed_time), 1)
                    if hit_timer <= 0:
                        hit_ticks = pygame.time.get_ticks()
                        hit_elapsed_time = (pygame.time.get_ticks() - hit_ticks) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            key = pygame.key.get_pressed()
            if hold_timer > 0:
                if key[pygame.K_SPACE] is False:
                    num_of_pressed -= power_of_enemy
            elif hold_timer < 0:
                if key[pygame.K_RIGHT] is False and key[pygame.K_LEFT] is False:
                    num_of_pressed -= power_of_enemy

                elif key[pygame.K_RIGHT] is True or key[pygame.K_LEFT] is True:
                    num_of_pressed += self.MY_POWER

            # Game over conditions.
            if left_time <= 0:
                message_to_screen_center(
                    self.screen,
                    "Timeout",
                    RED,
                    level_font,
                    self.screen.get_height() / 1.7,
                    font_size=40
                )
                self.lose_game()
                did_win = False
                break
            
            elif (num_of_press_key_to_clear - num_of_pressed) > condition_of_game_over:
                message_to_screen_center(
                    self.screen,
                    "Opponent wins.",
                    RED,
                    level_font,
                    self.screen.get_height() / 2,
                    font_size=40
                )
                pygame.display.update()
                clock.tick(1)
                self.lose_game()
                break

            elif num_of_pressed >= num_of_press_key_to_clear:
                did_win = True
                break

            pygame.display.update()
            clock.tick(FPS_RATE)

        if did_win:
            message_to_screen_center(
                self.screen,
                "Congratulations!",
                GREEN,
                level_font,
                self.screen.get_height() / 2,
                font_size=40
            )
            message_to_screen_center(
                self.screen,
                "Go to the next level.",
                GREEN,
                level_font,
                self.screen.get_height() / 1.3,
                font_size=40
            )
            pygame.display.update()
            clock.tick(1)
            return left_time

        else:
            game_over_img = pygame.image.load(GAME_OVER_LOCATION)
            self.screen.fill(BLACK)
            game_over_image = pygame.transform.scale(game_over_img, (DISPLAY_H, DISPLAY_H))
            self.screen.blit(game_over_image,
                                    ((DISPLAY_W - game_over_image.get_width()) // 2, 0))
            message_to_screen_center(self.screen, 'Game Over',
                                        RED, level_font,
                                        self.screen.get_height() / 4,
                                        font_size=40)
            pygame.display.update()
            clock.tick(1)
            return


def start_game(level, score,  select_mode=False):
    pygame.init()
    current_screen = pygame.display.get_window_size()
    new_game = TugOfWar(DISPLAY_W, DISPLAY_H, current_screen)
    score = new_game.start_game(level, score, select_mode)
    return score
