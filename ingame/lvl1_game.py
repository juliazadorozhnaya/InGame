from .lvl1_game_object import NPC, PC, Aim, GameObject
from .game_settings import *


AIM_LOCATION = get_abs_path("images/aim.png")
BGM_LOCATION = get_abs_path("sounds/mugunghwa.mp3")
BACKGROUND_LOCATION = get_abs_path("images/background_1.png")
DOLL_BACK_LOCATION = get_abs_path("images/back.png")
DOLL_FRONT_LOCATION = get_abs_path("images/front.png")
SCREEN_STARTING_POINT = (0, 0)  # Upper left half of the results screen.
STARTING_MESSAGE_Y_POS = (300, 400, 650)
NPC_1_CODE = 1
NPC_2_CODE = 2

DEAD_MESSAGE = "dead"
DOLL_MESSAGE = "DOLL"
STARTING_LEVEL = 1
KEY_INPUT = 768


class Game:
    """Creating a game window with all the characters."""
    TICK_RATE = 90
    TIMER_TIME = 5
    NPC_CHANGE_DIRECTION_TIME = 1.9
    AIM_CHANGE_DIRECTION_TIME = 1.5
    GAME_OVER_TIMER = 30
    NPC_1_SPEED = 4.1
    NPC_2_SPEED = 3.7
    AIM_SIZE = (500, 350)
    AIM_SPEED = 2
    TIMER_UNIT = 1000
    LEVEL_UP_STEP = 0.3

    def __init__(self, image_path, title, width, height, current_screen):

        self.title = title
        self.width = width
        self.height = height
        self.half_width = width / 2
        self.one_third_screen = (width / 3, height / 3)
        self.game_screen = pygame.display.set_mode(
            (width, height), pygame.RESIZABLE
        ) 

        self.game_screen.fill(WHITE)
        pygame.display.set_caption(title)  # Set the window title.
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

        self.mugunghwa_timer = False  # Timer with tagger back.
        self.game_over_timer = None
        self.aim_image = pygame.image.load(AIM_LOCATION)
        self.ref_w, self.ref_h = self.game_screen.get_size()

        self.npc_1_size = width / 10
        self.npc_2_size = width / 8

        self.doll = [
            self.width * 0.456,
            self.height / 80,
            self.width / 8,
            self.height * 0.1875,
        ]

        self.player_character_size = (width / 16, width / 11)
        self.restart_message_y_pos = (180, 280)

        self.volume_notice = True

        try:
            pygame.mixer.music.load(BGM_LOCATION)
        except Exception as e:
            print(e)
            print("Sound Load error")
        pygame.display.set_mode(current_screen, pygame.RESIZABLE)

    def create_npc(self, kind_of_npc, game_screen=None):

        if game_screen is None:
            game_screen = pygame.display.set_mode(
                (DISPLAY_W, DISPLAY_H), pygame.RESIZABLE
            )
        if kind_of_npc == NPC_1_CODE:
            size = self.npc_1_size
        elif kind_of_npc == NPC_2_CODE:
            size = self.npc_2_size

        return NPC(size, size, kind_of_npc)

    def start_game(self, level, score, select_mode):
        score = self.run_game_loop(level, score, select_mode)
        return score

    def lose_game(self):
        game_over_image = pygame.image.load(GAME_OVER_LOCATION)
        game_over_image = pygame.transform.scale(
            game_over_image,
            (
                game_over_image.get_width()
                * (self.game_screen.get_width() / DISPLAY_W),
                game_over_image.get_height()
                * (self.game_screen.get_height() / DISPLAY_H),
            ),
        )
        self.game_screen.blit(game_over_image, SCREEN_STARTING_POINT)
        message_to_screen_center(
            self.game_screen,
            "You lose.",
            RED,
            level_font,
            self.game_screen.get_width() / 4,
        )
        pygame.display.update()
        clock.tick(0.5)

    def run_game_loop(self, level, score, select_mode):
        game_over = False
        did_win = True

        pygame.mixer.music.play(-1)
        self.game_over_timer = GameOverTimer(self.GAME_OVER_TIMER)

        player = PC(
            self.half_width, self.height, *self.player_character_size
        )

        npc_1 = self.create_npc(NPC_1_CODE)
        npc_2 = self.create_npc(NPC_2_CODE)
        npc_1.BASE_SPEED = 1 + self.NPC_1_SPEED
        npc_2.BASE_SPEED = 1 + self.NPC_2_SPEED
        npcs = [npc_1, npc_2]

        aim = Aim(*self.AIM_SIZE)
        aim.BASE_SPEED *= self.AIM_SPEED

        DOLL = GameObject(*self.doll)
        DOLL.sprite_image(DOLL_BACK_LOCATION)

        start_ticks = pygame.time.get_ticks()
        npc_ticks = pygame.time.get_ticks()
        aim_ticks = pygame.time.get_ticks()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return

            left_time = self.game_over_timer.time_checker()
            if left_time < 0:
                self.lose_game()
                pygame.mixer.music.stop()
                return

            dir_x, dir_y = self.get_PC_dir()
            self.game_screen.fill(WHITE)
            self.image = pygame.transform.scale(
                self.image,
                (self.game_screen.get_width(), self.game_screen.get_height()),
            )
            self.game_screen.blit(self.image, SCREEN_STARTING_POINT)
            DOLL.draw(self.game_screen)

            for npc in npcs:
                npc.move(self.width)
                npc.draw(self.game_screen)
            player.move(dir_x, dir_y, self.width, self.height)
            player.draw(self.game_screen, dir_x, dir_y)

            # The NPC turns the timer settings.
            npc_elapsed_time = (pygame.time.get_ticks() - npc_ticks) / self.TIMER_UNIT
            npc_timer = round(
                float(self.NPC_CHANGE_DIRECTION_TIME - npc_elapsed_time), 1
            )
            if (
                npc_timer <= 0
            ):  # When npc_timer is 0, the direction of progress of all NPC changes.
                for npc in npcs:
                    npc.change_direction()
                npc_ticks = pygame.time.get_ticks()
                npc_elapsed_time = (
                    pygame.time.get_ticks() - npc_ticks
                ) / self.TIMER_UNIT

            # Progress only when stop is false.
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / self.TIMER_UNIT
            timer = round(float(self.TIMER_TIME - elapsed_time), 1)

            # Current level, displaying the game end timer in the upper left corner of the screen.
            message_to_screen_left(
                self.game_screen,
                "Level:" + str(level),
                WHITE,
                level_font,
                self.game_screen.get_width() / 11,
                self.game_screen.get_height() / 30,
            )
            message_to_screen_left(
                self.game_screen,
                "GAME OVER : " + str(left_time),
                WHITE,
                level_font,
                self.game_screen.get_width() / 4.8,
                self.game_screen.get_height() / 14,
            )
            message_to_screen_left(
                self.game_screen,
                "SCORE : " + str(round(score)),
                BLACK,
                level_font,
                self.game_screen.get_width() / 1.2,
                self.game_screen.get_height() / 23,
            )

            try:
                collision = self.detect_all_collisions(
                    player, npc_1, npc_2, DOLL, select_mode
                )
            except:
                try:
                    collision = self.detect_all_collisions(
                        player, npc_1, 0, DOLL, select_mode
                    )
                except:
                    collision = self.detect_all_collisions(
                        player, 0, 0, DOLL, select_mode
                    )

            # Sound effects.
            if pygame.mixer.music.get_busy() is False:
                pygame.mixer.music.play(-1)

            # The doll is preparing to turn around.
            if timer <= 0:
                self.volume_notice = False
                # Resetting the timer.
                DOLL.sprite_image(DOLL_FRONT_LOCATION)
                self.mugunghwa_timer = True
                time = self.TIMER_TIME
                time_checker = round(time - (timer) * (-1), 1)
                if time_checker <= 0:
                    DOLL.sprite_image(DOLL_BACK_LOCATION)
                    self.mugunghwa_timer = False
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (
                        pygame.time.get_ticks() - start_ticks
                    ) / self.TIMER_UNIT
                    timer = round(float(self.TIMER_TIME - elapsed_time), 2)
                else:

                    aim.move(self.width)
                    aim.draw(self.game_screen)
                    aim_elapsed_time = (
                        pygame.time.get_ticks() - aim_ticks
                    ) / self.TIMER_UNIT
                    aim_timer = round(
                        float(self.AIM_CHANGE_DIRECTION_TIME - aim_elapsed_time), 1
                    )
                    if aim_timer <= 0:
                        aim.change_direction()
                        aim_ticks = pygame.time.get_ticks()
                        aim_elapsed_time = (
                            pygame.time.get_ticks() - aim_ticks
                        ) / self.TIMER_UNIT

                    if event.type == KEY_INPUT:
                        did_win = False
                        self.mugunghwa_timer = False  # The doll recovers to restart.
                        DOLL.sprite_image(DOLL_BACK_LOCATION)
                        self.lose_game()
                        break

            if collision == DEAD_MESSAGE:
                did_win = False
                break
            elif collision == DOLL_MESSAGE:
                break


            pygame.display.update()
            clock.tick(self.TICK_RATE)

        if did_win:
            pygame.mixer.music.stop()
            return left_time
        else:
            pygame.mixer.music.stop()
            return

    def get_PC_dir(self, dir_x=0, dir_y=0):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            dir_y = 1
        if keys[pygame.K_DOWN]:
            dir_y = -1
        if keys[pygame.K_LEFT]:
            dir_x = -1
        if keys[pygame.K_RIGHT]:
            dir_x = 1
        return dir_x, dir_y

    def detect_all_collisions(self, player, npc_1, npc_2, DOLL, select_mode):
        dead = 0
        dead += player.detect_collision(npc_2)
        dead += player.detect_collision(npc_1)

        if dead:
            self.lose_game()
            return DEAD_MESSAGE

        # When colliding with the sight, we return DOLL_MESSAGE to transfer the winnings in the game to the parent function.
        if player.detect_collision(DOLL):
            message_to_screen_center(
                self.game_screen,
                "Pass!",
                WHITE,
                level_font,
                self.game_screen.get_height() / 3,
            )
            if select_mode:
                message_to_screen_center(
                    self.game_screen,
                    "Go to the next level.",
                    WHITE,
                    level_font,
                    self.game_screen.get_height() / 2,
                )
                
            else:
                message_to_screen_center(
                    self.game_screen,
                    "Next level.",
                    WHITE,
                    level_font,
                    self.game_screen.get_height() / 2,
                )
            pygame.display.update()
            clock.tick(0.5)
            return DOLL_MESSAGE


# Start the game up
def start_game(level, score, select_mode):
    pygame.init()
    current_screen = pygame.display.get_window_size()
    new_game = Game(
        BACKGROUND_LOCATION,
        SCREEN_TITLE,
        DISPLAY_W,
        DISPLAY_H,
        current_screen,
    )
    return new_game.start_game(level, score, select_mode)
