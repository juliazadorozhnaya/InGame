import math
import random

import pygame

DISPLAY_W, DISPLAY_H = 800, 600

CIRCLE_SHAPE_SIZE_RATIO = 1
SHAPE_WIDTH_RATIO = 0.01875
POINT_CIRCLE_RATIO = 0.2
POINT_RECTANGLE_RATIO = 3
RECTANGLE_SHAPE_SIZE_RATIO = 2.2
RECTANGLE_BORDER_RADIUS = 10
WRONG_POINT_INTERVAL = 10
TRIANGLE_ERROR = 5

CIRCLE = 1
RECTANGLE = 2
TRIANGLE = 3
CLICKED_POINT_SIZE = 2
UNCLICKED_POINT_SIZE = 6
POINT_SIZE = 5
WRONG_POINTS_NUM = 3

DIRECTION_RANGE = (1, 5)

font_name = pygame.font.get_default_font()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (227, 62, 126)
YELLOW_BROWN = (207, 153, 59)
BROWN = (117, 48, 0)
DARK_BROWN = (175, 118, 43)
GRAY = (48, 49, 52)

PIN_LOCATION = "ingame/CookieCutter/images/pin.png"
COOKIE_LOCATION = "ingame/CookieCutter/images/cookie.png"
BACKGROUND_LOCATION = "ingame/CookieCutter/images/background.jpg"
NPC_RANDRANGE = random.randrange(20, 300)
KIND_OF_NPC = 1
NPC_SPEED = 3
NPC_SIZE_RATIO = 8
GAME_TIME = 50
NUMBER_OF_POINTS = 100
DALGONA_SIZE_RATIO = (3 / 8)
FPS_RATE = 120
SCREEN_STARTING_POINT = (0, 0)
STARTING_LEVEL = 1


def get_theta(points_num, i):
    return (2 * math.pi / points_num) * i
