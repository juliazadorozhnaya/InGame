import pygame

GAME_OVER_LOCATION = 'ingame/images/common_images/game_over.png'

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