import random

import pygame

from CookieCutter.constants import *
from game_settings import *


class GameObject:
    def __init__(self, ingame, x, y, width, height, game_screen=None):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.game_screen = ingame.window

class NPC(GameObject):
    BASE_SPEED = 3

    NPC_1_Y_POS = 1 / 5
    NPC_2_Y_POS = 3 / 7
    NPC_3_Y_POS = 2 / 3

    def __init__(self, ingame, width, height, kind_of_object=1):
        game_screen_size = pygame.display.get_window_size()
        x_pos = game_screen_size[0] / 2
        if kind_of_object == 1:
            value = self.NPC_1_Y_POS
        elif kind_of_object == 2:
            value = self.NPC_2_Y_POS
        else:
            value = self.NPC_3_Y_POS
        y_pos = game_screen_size[1] * value

        super().__init__(ingame, x_pos, y_pos, width, height)
        self.kind_of_object = kind_of_object
        object_image = pygame.image.load(f'CookieCutter/images/NPC/NPC{kind_of_object}.png')
        self.go_forward = False
        self.direction = 1
        self.image = pygame.transform.scale(object_image, (width * (3 / 4), height))

    def draw(self, background):
        if self.go_forward:
            self.image = pygame.transform.scale(self.image, (
            self.width * (background.get_width() / self.width)*(3/4), self.height * (background.get_height() / self.height)))
            background.blit(self.image, (self.x_pos* (background.get_width() / self.width), self.y_pos* (background.get_width() / self.height)))
        else:
            self.image = pygame.transform.scale(self.image, (
            self.width * (background.get_width() / self.width)*(3/4), self.height * (background.get_height() / self.height)))
            background.blit(pygame.transform.flip(
                self.image, 1, 0),(self.x_pos * (background.get_width() / self.width), self.y_pos * (background.get_width() / self.height)))

    def move(self, max_width):
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
        self.direction = random.randrange(*DIRECTION_RANGE)


class CookieCutter:
    def __init__(self, game_screen, points_num, shape):
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
            pos_x = self.half_width - self.half_rectangle
            pos_y = self.half_height - self.half_rectangle

            for i in range(1, int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, POINT_SIZE))
                self.points.append(Point(game_screen, pos_x + self.rectangle_size, pos_y, POINT_SIZE))
                pos_y += (DISPLAY_W / RECTANGLE_SHAPE_SIZE_RATIO) / (points_num / 4)
            pos_x = self.half_width - self.half_rectangle
            pos_y = self.half_height - self.half_rectangle
            for i in range(1, int(points_num / 4)):
                self.points.append(Point(game_screen, pos_x, pos_y, POINT_SIZE))
                self.points.append(Point(game_screen, pos_x, pos_y + self.rectangle_size, POINT_SIZE))
                pos_x += (DISPLAY_W / RECTANGLE_SHAPE_SIZE_RATIO) / (points_num / 4)

            self.change_wrong_points()

        elif shape == TRIANGLE:
            pos_x = self.half_width
            pos_y = DISPLAY_H / 4 + 10
            for i in range(int(points_num / 3)):
                move = ((5 / 12) * DISPLAY_H) / (points_num / 3)
                self.points.append(
                    Point(game_screen, pos_x + ((i + 1) * move * (1 / math.sqrt(3))), pos_y, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - ((i + 1) * move * (1 / math.sqrt(3))), pos_y, POINT_SIZE))
                pos_y += move

            pos_y = DISPLAY_H * (2 / 3)
            self.points.append(Point(game_screen, pos_x, pos_y, 5))
            for i in range(int(points_num / 6.5)):
                self.points.append(
                    Point(game_screen, pos_x + (i + 1) * (DISPLAY_W / 4 / (points_num / 6)), pos_y, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - (i + 1) * (DISPLAY_W / 4 / (points_num / 6)), pos_y, POINT_SIZE))

            self.change_wrong_points()

        elif shape == STAR:
            num_of_side = 12
            points_num_of_side = int(points_num / num_of_side)
            side_length = (DISPLAY_W / 2) / 3
            half_side_length = side_length / 2
            ratio = math.sqrt(3)
            center = (DISPLAY_W / 2, DISPLAY_H / 2)
            pos_x = center[0]
            pos_y = center[1] - (half_side_length * ratio) * 2
            reverse_pos_x = center[0]
            reverse_pos_y = center[1] + (half_side_length * ratio) * 2
            for i in range(points_num_of_side):
                increase = i * ((half_side_length * ratio) / points_num_of_side)
                self.points.append(
                    Point(game_screen, pos_x + increase / ratio, pos_y + increase, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - increase / ratio,
                          pos_y + i * ((half_side_length * ratio) / points_num_of_side), POINT_SIZE))
                self.points.append(Point(game_screen, reverse_pos_x + increase / ratio, reverse_pos_y - increase, 5))
                self.points.append(Point(game_screen, reverse_pos_x - increase / ratio, reverse_pos_y - increase, 5))

            for i in range(points_num_of_side * 2, points_num_of_side * 3):
                increase = i * ((half_side_length * ratio) / points_num_of_side)
                self.points.append(
                    Point(game_screen, pos_x + increase / ratio, pos_y + increase, POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - increase / ratio,
                          pos_y + i * ((half_side_length * ratio) / points_num_of_side), POINT_SIZE))
                self.points.append(
                    Point(game_screen, reverse_pos_x + increase / ratio, reverse_pos_y - increase, POINT_SIZE))
                self.points.append(
                    Point(game_screen, reverse_pos_x - increase / ratio, reverse_pos_y - increase, POINT_SIZE))

            pos_y += half_side_length * ratio
            reverse_pos_y -= half_side_length * ratio
            for i in range(points_num_of_side):
                self.points.append(
                    Point(game_screen, pos_x + half_side_length + i * (side_length / points_num_of_side), pos_y,
                          POINT_SIZE))
                self.points.append(
                    Point(game_screen, pos_x - half_side_length - i * (side_length / points_num_of_side), pos_y,
                          POINT_SIZE))
                self.points.append(
                    Point(game_screen, reverse_pos_x + half_side_length + i * (side_length / points_num_of_side),
                          reverse_pos_y, 5))
                self.points.append(
                    Point(game_screen, reverse_pos_x - half_side_length - i * (side_length / points_num_of_side),
                          reverse_pos_y, 5))
            self.change_wrong_points()

    def draw(self):
        for i in self.points:
            i.punching()

    def check_win(self):
        result = {"is_success": True, "wrong_point_clicked": False}
        for i in self.points:
            if not i.clicked and not i.wrong_point:
                result["is_success"] = False
            if i.wrong_point and i.clicked:
                result["wrong_point_clicked"] = True
        return result

    # change wrong point randomly
    def change_wrong_points(self):
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
    def __init__(self, game_display, x, y, radius, wrong_point=False):
        self.game_display = game_display
        self.clicked = False
        self.radius = radius
        self.x = x
        self.y = y
        self.wrong_point = wrong_point

    def is_clicked(self):
        mouse_x_pos = pygame.mouse.get_pos()[0]
        mouse_y_pos = pygame.mouse.get_pos()[1]

        if self.x + self.radius > mouse_x_pos > self.x - self.radius and self.y + self.radius > \
                mouse_y_pos > self.y - self.radius:
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True

    def draw(self):
        if self.clicked and not self.wrong_point:
            pygame.draw.circle(self.game_display, BLACK, [self.x, self.y], self.radius, UNCLICKED_POINT_SIZE)
        elif not self.clicked and not self.wrong_point:
            pygame.draw.circle(self.game_display, BROWN, [self.x, self.y], self.radius, CLICKED_POINT_SIZE)
        elif not self.clicked and self.wrong_point:
            pygame.draw.circle(self.game_display, RED, [self.x, self.y], self.radius, UNCLICKED_POINT_SIZE)

    def punching(self):
        self.is_clicked()
        self.draw()
