import pygame

from ingame.CookieCutter.game import start_game


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def button(self, x, y, image):
        img_button = image
        img_button = pygame.transform.scale(
            img_button, (image.get_width(), image.get_height())
        )
        button = img_button.get_rect()
        button.topleft = (x, y)
        self.game.window.blit(img_button, (x, y))
        return button


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def draw_menu(self):
        return (
            self.button(
                self.game.DISPLAY_W / 3,
                self.game.DISPLAY_H / 10,
                self.game.img_play_button,
            ),
            self.button(
                self.game.DISPLAY_W / 3,
                self.game.DISPLAY_H / 3.1,
                self.game.img_select_button,
            ),
            self.button(
                self.game.DISPLAY_W / 3,
                self.game.DISPLAY_H / 1.85,
                self.game.img_help_button,
            ),
            self.button(
                self.game.DISPLAY_W / 3,
                self.game.DISPLAY_H / 1.32,
                self.game.img_exit_button,
            ),
        )

    def display_menu(self):
        self.game.click = False
        self.run_display = True
        while self.run_display:
            self.game.window.blit(self.game.display, (0, 0))
            self.game.display.fill(self.game.PINK)
            mx, my = pygame.mouse.get_pos()
            button_play, button_select, button_help, button_exit = self.draw_menu()
            if button_play.collidepoint((mx, my)):
                if self.game.click:
                    self.game.click = False
                    self.run_display = False
                    self.game.playing = True
                    return self.game.game_loop()
            elif button_select.collidepoint((mx, my)):
                if self.game.click:
                    self.game.click = False
                    self.run_display = False
                    return self.game.select_menu.display_menu()
            elif button_help.collidepoint((mx, my)):
                if self.game.click:
                    self.game.click = False
                    self.run_display = False
                    return self.game.help.display_menu()
            elif button_exit.collidepoint((mx, my)):
                if self.game.click:
                    self.game.click = False
                    self.run_display = False
                    self.running = False
                    return 0

            self.game.check_events()
            self.game.draw_text(
                "InGame", 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 260
            )
            pygame.display.update()


class SelectGameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def draw_select_menu(self):
        return (
            self.button(
                self.game.DISPLAY_W / 25,
                self.game.DISPLAY_H / 25,
                self.game.img_lvl1_button,
            ),
            self.button(
                self.game.DISPLAY_W / 2.8,
                self.game.DISPLAY_H / 5,
                self.game.img_lvl2_button,
            ),
            self.button(
                self.game.DISPLAY_W / 1.49,
                self.game.DISPLAY_H / 25,
                self.game.img_lvl3_button,
            ),
            self.button(
                self.game.DISPLAY_W / 25,
                self.game.DISPLAY_H / 1.9,
                self.game.img_lvl4_button,
            ),
            self.button(
                self.game.DISPLAY_W / 1.49,
                self.game.DISPLAY_H / 1.9,
                self.game.img_lvl5_button,
            ),
            self.button(
                self.game.DISPLAY_W / 3,
                self.game.DISPLAY_H / 1.2,
                self.game.img_back_button,
            ),
        )

    def display_menu(self):
        self.run_display = True
        self.game.click = False
        while self.run_display:
            self.game.window.blit(self.game.display, (0, 0))
            self.game.display.fill(self.game.PINK)
            mx, my = pygame.mouse.get_pos()
            (
                button_l1,
                button_l2,
                button_l3,
                button_l4,
                button_l5,
                button_back,
            ) = self.draw_select_menu()
            if button_l1.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.game.playing = True
                    return 1
            elif button_l2.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.game.playing = True
                    level = 1
                    score = 0
                    while self.game.playing:
                        res = start_game(level=level, score=score, select_mode=True, game_screen=self.game.window)
                        if type(res) is not int:
                            self.game.playing = False
                        else:
                            level += 1
                            score += res
                    return self.game.select_menu.display_menu()
            elif button_l3.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.game.playing = True
                    return 3
            elif button_l4.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.game.playing = True
                    return 4
            elif button_l5.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.game.playing = True
                    return 5
            elif button_back.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.running = False
                    return self.game.main_menu.display_menu()

            self.game.check_events()

            self.game.draw_text(
                "Select Level",
                40,
                self.game.DISPLAY_W / 2,
                self.game.DISPLAY_H / 2 - 260,
            )
            pygame.display.update()


class HelpPage(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        self.game.click = False
        while self.run_display:
            self.game.window.blit(self.game.display, (0, 0))
            self.game.display.fill(self.game.PINK)
            mx, my = pygame.mouse.get_pos()
            button_back = self.button(
                self.game.DISPLAY_W / 3,
                self.game.DISPLAY_H / 1.3,
                self.game.img_back_button,
            )

            if button_back.collidepoint((mx, my)):
                if self.game.click:
                    self.run_display = False
                    self.running = False
                    return self.game.main_menu.display_menu()

            self.game.check_events()

            self.game.draw_text(
                "About InGame",
                40,
                self.game.DISPLAY_W / 2,
                self.game.DISPLAY_H / 2 - 260,
            )
            pygame.display.update()
