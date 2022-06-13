import pygame
import unittest

from lvl2_game import Game as CC_Game
from lvl2_game_object import CookieCutter
from constants import NUMBER_OF_POINTS, CIRCLE
from game import InGame
from game_settings import DISPLAY_W, DISPLAY_H


class InGameTests(unittest.TestCase):
    def setUp(self):
        self.ingame = InGame()

    def test_screen_size(self):
        self.assertEqual(self.ingame.window.get_width(), DISPLAY_W, "Wrong settings of pygame display.")
        self.assertEqual(self.ingame.window.get_height(), DISPLAY_H, "Wrong settings of pygame display.")

    def test_CC_create(self):
        self.new_game = CC_Game(self.ingame.window)
        minigame = CookieCutter(self.new_game.game_screen, NUMBER_OF_POINTS, CIRCLE)
        self.assertEqual(len(minigame.points), NUMBER_OF_POINTS, "Wrong number of points.")

    def quitInGame(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()