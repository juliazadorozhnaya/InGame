"""CookieCutter game object."""

import random

from constants import *
from game_settings import *


class CookieCutter:
    """CookieCutter object class."""

    def __init__(self, game_screen, points_num, shape):
        """
        Initialize CookieCutter object.

        :param game_screen: game screen.
        :param points_num: number of points.
        :param shape: shape of figure. 1 - CIRCLE, 2 - RECTANGLE, 3 - TRIANGLE.
        """
        self.points = []
        self.wrong_point_indexes = []
        self.half_width = DISPLAY_W / 2
        self.half_height = DISPLAY_H / 2
        self.rectangle_size = DISPLAY_W / POINT_RECTANGLE_RATIO
        self.half_rectangle = self.rectangle_size / 2

        if shape == CIRCLE:
            for i in range(points_num):
                theta = get_theta(points_num, i)
                pos_x = self.half_width + (int(DISPLAY_W * POINT_CIRCLE_RATIO) * math.cos(theta))
                pos_y = self.half_height + (int(DISPLAY_W * POINT_CIRCLE_RATIO) * math.sin(theta))
                self.points.append(Point(game_screen, pos_x, pos_y, POINT_SIZE))

            self.change_wrong_points()

        elif shape == RECTANGLE:
            points_num -= 20
            pos_x = self.half_width - self.half_rectangle
            pos_y = self.half_height - self.half_rectangle

            for i in range(1, int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, POINT_SIZE))
                self.points.append(Point(game_screen, pos_x + self.rectangle_size,
                                         pos_y, POINT_SIZE))
                pos_y += (DISPLAY_W / RECTANGLE_SHAPE_SIZE_RATIO) / (points_num / 4)
            pos_x = self.half_width - self.half_rectangle
            pos_y = self.half_height - self.half_rectangle
            for i in range(1, int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, POINT_SIZE))
                self.points.append(Point(game_screen, pos_x,
                                         pos_y + self.rectangle_size, POINT_SIZE))
                pos_x += (DISPLAY_W / RECTANGLE_SHAPE_SIZE_RATIO) / (points_num / 4)

            self.change_wrong_points()

        elif shape == TRIANGLE:
            pos_x = self.half_width
            pos_y = DISPLAY_H / 4 + 10
            for i in range(int(points_num / 3)):
                move = ((5 / 12) * DISPLAY_H) / (points_num / 3)
                self.points.append(
                    Point(game_screen, pos_x + ((i + 1) * move * (1 / math.sqrt(3))),
                          pos_y, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - ((i + 1) * move * (1 / math.sqrt(3))),
                          pos_y, POINT_SIZE))
                pos_y += move

            pos_y = DISPLAY_H * (2 / 3)
            self.points.append(Point(game_screen, pos_x, pos_y, 5))
            for i in range(int(points_num / 6.5)):
                self.points.append(
                    Point(game_screen,
                          pos_x + (i + 1) * (DISPLAY_W / 4 / (points_num / 6)),
                          pos_y, POINT_SIZE))
                self.points.append(
                    Point(game_screen,
                          pos_x - (i + 1) * (DISPLAY_W / 4 / (points_num / 6)),
                          pos_y, POINT_SIZE))

            self.change_wrong_points()

    def draw(self):
        """Draw points."""
        for i in self.points:
            i.punching()

    def check_win(self):
        """Check win."""
        result = {"is_success": True, "wrong_point_clicked": False}
        for i in self.points:
            if not i.clicked and not i.wrong_point:
                result["is_success"] = False
            if i.wrong_point and i.clicked:
                result["wrong_point_clicked"] = True
        return result

    def change_wrong_points(self):
        """Change wrong point randomly."""
        if self.wrong_point_indexes:
            for i in self.wrong_point_indexes:
                self.points[i].wrong_point = False
                self.points[i].clicked = False
            self.wrong_point_indexes.clear()
        wrong_points = random.sample(self.points, WRONG_POINTS_NUM)
        for point in wrong_points:
            if type(point) is not int:
                point.clicked = False
                point.wrong_point = True
                index = self.points.index(point)
                self.wrong_point_indexes.append(index)


class Point:
    """Point state class."""

    def __init__(self, game_display, x, y, radius, wrong_point=False):
        """
        Initialize new point.

        :param game_display: game display.
        :param x: x coordinate of the point.
        :param y: y coordinate of the point.
        :param radius: radius of the point.
        :param wrong_point: red point if True and brown otherwise.
        """
        self.game_display = game_display
        self.clicked = False
        self.radius = radius
        self.x = x
        self.y = y
        self.wrong_point = wrong_point

    def is_clicked(self):
        """Click on the point."""
        mouse_x_pos = pygame.mouse.get_pos()[0]
        mouse_y_pos = pygame.mouse.get_pos()[1]

        if self.x + self.radius > mouse_x_pos > self.x - self.radius and self.y + self.radius > \
                mouse_y_pos > self.y - self.radius:
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True

    def draw(self):
        """Draw point."""
        if self.clicked and not self.wrong_point:
            pygame.draw.circle(self.game_display, BLACK, [self.x, self.y],
                               self.radius, UNCLICKED_POINT_SIZE)
        elif not self.clicked and not self.wrong_point:
            pygame.draw.circle(self.game_display, BROWN, [self.x, self.y],
                               self.radius, CLICKED_POINT_SIZE)
        elif not self.clicked and self.wrong_point:
            pygame.draw.circle(self.game_display, RED, [self.x, self.y],
                               self.radius, UNCLICKED_POINT_SIZE)

    def punching(self):
        """Punch point."""
        self.is_clicked()
        self.draw()
