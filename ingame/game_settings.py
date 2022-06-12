import pygame

GAME_OVER_LOCATION = 'ingame/images/common_images/game_over.png'

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
large_font = pygame.font.SysFont('comicsans', 75)
STOP_font = pygame.font.SysFont('comicsans', 120)
level_font = pygame.font.SysFont('calibri', 30)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'InGame'

class GameOverTimer:
    def __init__(self, timer_time):
        self.start_ticks = pygame.time.get_ticks()
        self.timer_time = timer_time

    def time_checker(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        timer = round(float(self.timer_time - elapsed_time), 1)
        return timer

def message_to_screen_left(surface, msg, color, text_font, x, y, ref_w, ref_h):
    textSurf, textRect = text_objects(msg, color, text_font)
    cur_w, cur_h = surface.get_size()
    txt_w, txt_h = textSurf.get_size()
    textSurf = pygame.transform.smoothscale(textSurf, (txt_w * cur_w // ref_w, txt_h * cur_h // ref_h))
    textRect = textSurf.get_rect()
    textRect.center = x, y
    surface.blit(textSurf, textRect)


def text_objects(text, color, font_name):
    text_font = pygame.font.Font(font_name, 20)
    textSurface = text_font.render(text, True, color).convert_alpha()
    return textSurface, textSurface.get_rect()

clock = pygame.time.Clock()

def message_to_screen_center(surface, msg, color, text_font, y, ref_w, ref_h):
    textSurf, textRect = text_objects(msg, color, text_font)
    cur_w, cur_h = surface.get_size()
    txt_w, txt_h = textSurf.get_size()
    textSurf = pygame.transform.smoothscale(textSurf, (txt_w * cur_w // ref_w, txt_h * cur_h // ref_h))
    textRect = textSurf.get_rect()
    textRect.center = surface.get_width() / 2, y
    surface.blit(textSurf, textRect)
    
    