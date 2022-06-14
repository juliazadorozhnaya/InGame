"""Module for creating game objects and game screen."""
import random
from .game_settings import *
import pygame


AIM_LOCATION = get_abs_path("images/aim.png")
PC_FRONT_LOCATION = get_abs_path("images/LinkFront.png")
PC_BACK_LOCATION = get_abs_path("images/LinkBack.png")
PC_LEFT_LOCATION = get_abs_path("images/LinkLeft.png")
PC_RIGHT_LOCATION = get_abs_path("images/LinkRight.png")
DIRECTION_RANGE = (1, 5)  # Where can NPC players move to.


class GameObject:
    """Create a background for game."""

    def __init__(self, x, y, width, height, game_screen=None):
        """Set size of the game screen."""
        if not game_screen:
            game_screen = pygame.display.set_mode(
                (DISPLAY_W, DISPLAY_H), pygame.RESIZABLE
            )

        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.game_screen = game_screen

    def sprite_image(self, image_path):
        """Create a background."""
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(
            object_image,
            (
                self.width * (self.game_screen.get_width() / DISPLAY_W),
                self.height * (self.game_screen.get_height() / DISPLAY_H),
            ),
        )

    def draw(self, background):
        """Drawing game objects in background."""
        self.image = pygame.transform.scale(
            self.image,
            (
                self.width * (background.get_width() / DISPLAY_W),
                self.height * (background.get_height() / DISPLAY_H),
            ),
        )
        background.blit(
            self.image, (background.get_width() / 2.25, background.get_height() / 40)
        )


class NPC(GameObject):
    """Create moving NPC Players."""

    BASE_SPEED = 1

    # Value for the Y coordinates needed to create the NPC.
    NPC_1_Y_POS = 1 / 5
    NPC_2_Y_POS = 3 / 7

    def __init__(self, width, height, kind_of_object=1):
        """Create an NPC player."""
        game_screen_size = pygame.display.get_window_size()
        x_pos = (
            game_screen_size[0] / 2
        )  # Set NPC generation X coordinate to the center.
        if kind_of_object == 1:
            value = self.NPC_1_Y_POS
        else:
            value = self.NPC_2_Y_POS

        y_pos = game_screen_size[1] * value  # Set the Y coordinate of each NPC.

        super().__init__(x_pos, y_pos, width, height)
        self.kind_of_object = kind_of_object
        object_image = pygame.image.load(get_abs_path(f"images/NPC{kind_of_object}.png"))
        self.go_forward = False
        self.direction = 1  # (1 right, 2 left, 3 up, 4 down)
        self.image = pygame.transform.scale(object_image, (width * (3 / 4), height))

    def draw(self, background):
        """Select size of moving object and determine position."""
        if self.go_forward:
            self.image = pygame.transform.scale(
                self.image,
                (
                    self.width * (background.get_width() / DISPLAY_W) * (3 / 4),
                    self.height * (background.get_height() / DISPLAY_H),
                ),
            )
            background.blit(
                self.image,
                (
                    self.x_pos * (background.get_width() / DISPLAY_W),
                    self.y_pos * (background.get_width() / DISPLAY_H),
                ),
            )
        else:
            self.image = pygame.transform.scale(
                self.image,
                (
                    self.width * (background.get_width() / DISPLAY_W) * (3 / 4),
                    self.height * (background.get_height() / DISPLAY_H),
                ),
            )
            background.blit(
                pygame.transform.flip(self.image, 1, 0),
                (
                    self.x_pos * (background.get_width() / DISPLAY_W),
                    self.y_pos * (background.get_width() / DISPLAY_H),
                ),
            )

    def move(self, max_width):
        """Set motion frame for moving player."""
        if self.x_pos <= 0:
            self.direction = 1
        elif self.x_pos >= max_width:
            self.direction = 2
        elif self.y_pos <= 0:
            self.direction = 4
        elif self.y_pos >= max_width:
            self.direction = 3

        if self.direction == 1:
            self.x_pos += self.BASE_SPEED
            self.go_forward = False
        elif self.direction == 2:
            self.x_pos -= self.BASE_SPEED
            self.go_forward = True
        elif self.direction == 3:
            self.y_pos -= self.BASE_SPEED
        else:
            self.y_pos += self.BASE_SPEED

    def change_direction(self):
        """Determine trajectory of player's NPC movement."""
        self.direction = random.randrange(*DIRECTION_RANGE)


class Aim(NPC):
    """A class for create a aim."""

    BASE_SPEED = 3

    def __init__(self, width, height, game_screen=None):
        """Create a suggestive target for doll."""
        if game_screen is None:
            game_screen = pygame.display.set_mode(
                (DISPLAY_W, DISPLAY_H), pygame.RESIZABLE
            )
        super().__init__(width, height)
        object_image = pygame.image.load(AIM_LOCATION)
        self.image = pygame.transform.scale(
            object_image,
            (
                self.width * (game_screen.get_width() / DISPLAY_W),
                self.height * (game_screen.get_height() / DISPLAY_H),
            ),
        )

    def move(self, max_width):
        """Set movement for goal."""
        super().move(max_width)
        if self.x_pos <= 0:
            self.direction = 1
        elif self.x_pos >= max_width - self.width:
            self.direction = 2
        elif self.y_pos <= 0:
            self.direction = 4
        elif self.y_pos >= max_width - self.width:
            self.direction = 3


class PC(GameObject):  # Player character.
    """Set a playing character."""

    BASE_SPEED = 6
    object_image = pygame.image.load(PC_FRONT_LOCATION)
    player_character = pygame.transform.scale(object_image, (40, 60))

    def __init__(self, x, y, width, height):
        """Сreate a character from different directions."""
        super().__init__(x, y, width, height)
        # Download all skins for rotation.
        object_image = pygame.image.load(PC_BACK_LOCATION)
        self.fr_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load(PC_FRONT_LOCATION)
        self.ba_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load(PC_LEFT_LOCATION)
        self.le_image = pygame.transform.scale(object_image, (width, height))
        object_image = pygame.image.load(PC_RIGHT_LOCATION)
        self.ri_image = pygame.transform.scale(object_image, (width, height))

    # Draw all the skins by changing the direction of the player's movement
    def draw(self, background, dir_x, dir_y):
        """Draw all skins of character at certain turns."""
        self.player_character = self.ba_image
        self.ba_image = pygame.transform.scale(
            self.ba_image,
            (
                self.width * (background.get_width() / DISPLAY_W),
                self.height * (background.get_height() / DISPLAY_H),
            ),
        )
        if dir_y > 0:
            self.fr_image = pygame.transform.scale(
                self.fr_image,
                (
                    self.width * (background.get_width() / DISPLAY_W),
                    self.height * (background.get_height() / DISPLAY_H),
                ),
            )
            background.blit(
                self.fr_image,
                (
                    self.x_pos * (background.get_width() / DISPLAY_W),
                    self.y_pos * (background.get_height() / DISPLAY_H),
                ),
            )
            self.player_character = self.fr_image
        elif dir_y < 0:
            self.ba_image = pygame.transform.scale(
                self.ba_image,
                (
                    self.width * (background.get_width() / DISPLAY_W),
                    self.height * (background.get_height() / DISPLAY_H),
                ),
            )
            background.blit(
                self.ba_image,
                (
                    self.x_pos * (background.get_width() / DISPLAY_W),
                    self.y_pos * (background.get_height() / DISPLAY_H),
                ),
            )
            self.player_character = self.ba_image
        elif dir_x > 0:
            self.ri_image = pygame.transform.scale(
                self.ri_image,
                (
                    self.width * (background.get_width() / DISPLAY_W),
                    self.height * (background.get_height() / DISPLAY_H),
                ),
            )
            background.blit(
                self.ri_image,
                (
                    self.x_pos * (background.get_width() / DISPLAY_W),
                    self.y_pos * (background.get_height() / DISPLAY_H),
                ),
            )
            self.player_character = self.ri_image
        elif dir_x < 0:
            self.le_image = pygame.transform.scale(
                self.le_image,
                (
                    self.width * (background.get_width() / DISPLAY_W),
                    self.height * (background.get_height() / DISPLAY_H),
                ),
            )
            background.blit(
                self.le_image,
                (
                    self.x_pos * (background.get_width() / DISPLAY_W),
                    self.y_pos * (background.get_height() / DISPLAY_H),
                ),
            )
            self.player_character = self.le_image
        else:
            background.blit(
                self.player_character,
                (
                    self.x_pos * (background.get_width() / DISPLAY_W),
                    self.y_pos * (background.get_height() / DISPLAY_H),
                ),
            )

    # Change direction according to keystrokes.
    def move(self, dir_x, dir_y, max_width, max_height):
        """Allow PC player to move within game screen."""
        MOVE_BY = self.BASE_SPEED
        # Changing the direction diagonally.
        if dir_x != 0 and dir_y != 0:
            MOVE_BY *= 0.707
        # Define X and Y  movement.
        self.y_pos += MOVE_BY * -dir_y
        self.x_pos += MOVE_BY * dir_x
        # Boundary detection.
        if self.y_pos > max_height - self.height:
            self.y_pos = max_height - self.height
        elif self.y_pos < 0:
            self.y_pos = 0
        if self.x_pos > max_width - self.width:
            self.x_pos = max_width - self.width
        elif self.x_pos < 0:
            self.x_pos = 0

    def detect_collision(self, other_body):
        """Meet of a PC player with an NPC player."""
        if self.y_pos > other_body.y_pos + other_body.height - self.height / 2:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        return True
