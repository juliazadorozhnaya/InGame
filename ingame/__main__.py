"""Main module to start the game."""

import pygame

from .game import InGame


if __name__ == '__main__':
    g = InGame()
    g.main_menu.display_menu()
    pygame.quit()
