"""Main file to start the game."""

import pygame

from ingame.ingame import InGame

g = InGame()

g.main_menu.display_menu()
pygame.quit()
