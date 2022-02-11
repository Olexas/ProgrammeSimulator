import pygame
import sys
import os
import time
from pygame.sprite import Sprite
from pygame.sprite import Group
from random import randint
from threading import Thread


class Sets():
    def __init__(self):
        self.screen_width = 850
        self.screen_height = 500
        self.fps = 60


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, lvl, text='', place_on_center=False, place=None, *group):
        super().__init__(*group)
        self.width = width
        self.height = height
        self.text = text
        self.image = load_image("button.png", None, (width, height))
        self.rect = self.image.get_rect()

        self.button_on_window = False
        self.mouse_on_button = False
        self.button_pressed = False

        self.button_lvl = lvl

        if place_on_center:
            self.rect.center = place.rect.center
            self.rect.y = self.rect.y + 15
            self.rect.x = self.rect.x
        else:
            self.rect.x = x
            self.rect.y = y

    def draw1(self, screen, fontsize):
        if self.text in ['Подземелья', 'Средние_Века', 'Ритм_Игра', 'Колонизация',
                         'Гейммейкер', 'Дикий_Запад', 'Тайм_Тревел']:
            fontsize = fontsize - 2
        if self.text != '':
            font = pygame.font.Font('fonts/DroidSansMono.ttf', fontsize)
            text = font.render(self.text, True, (0, 0, 0))
            screen.blit(text, (
                self.rect.x + (self.width / 2 - text.get_width() / 2), self.rect.y +
                (self.height / 2.35 - text.get_height() / 2)))

    def is_over(self, pos):
        print(self.button_on_window, self.text)
        if not self.button_on_window:
            return 0
        if self.rect.x < pos[0] < self.rect.x + self.width:
            if self.rect.y < pos[1] < self.rect.y + self.height:
                return True
        return False

    def update(self, screen, fontsize):
        self.draw1(screen, fontsize)

    def button_check_for_cursor(self, pos):
        if self.is_over(pos):
            if not self.mouse_on_button:
                self.image.fill((25, 25, 25), special_flags=pygame.BLEND_RGB_ADD)
                self.mouse_on_button = True
        else:
            if not self.button_pressed:
                self.image = load_image("button.png", None, (self.width, self.height))
                self.mouse_on_button = False

    def button_pressed_check(self):
        self.image = load_image("button_press.png", None, (self.width, self.height))
        self.image.fill((25, 25, 25), special_flags=pygame.BLEND_RGB_ADD)


class Creature(pygame.sprite.Sprite):
    def __init__(self, screen, floor, *group):
        super().__init__(*group)
        self.screen = screen
        self.image = load_image("persDown1.png", -1, (126, 246))
        self.rect = self.image.get_rect()
        self.rect.x = save_person_x
        self.rect.y = save_person_y
        self.clock = pygame.time.Clock()
        self.screen_rect = screen.get_rect()
        self.floor_rect = floor.rect

        self.position_value_up = 0
        self.position_value_down = 0
        self.position_value_left = 0
        self.position_value_right = 0

        self.movie_right = False
        self.movie_left = False
        self.movie_up = False
        self.movie_down = False

        self.time_for_movement_last = None
        self.time_for_movement_now = pygame.time.get_ticks()

    def update(self, *args):
        if self.movie_up:
            if not self.time_for_movement_last:
                self.time_for_movement_last = pygame.time.get_ticks()
            self.time_for_movement_now = pygame.time.get_ticks()
            if self.time_for_movement_now - self.time_for_movement_last >= 65:
                self.position_value_up = (self.position_value_up + 1) % 4
                self.position_value_down = 3
                self.position_value_left = 3
                self.position_value_right = 3

                self.sprite_update('up')

                if self.rect.bottom + 8 > 490:
                    self.rect.y -= +6
                self.time_for_movement_last = None

        if self.movie_down:
            if not self.time_for_movement_last:
                self.time_for_movement_last = pygame.time.get_ticks()
            self.time_for_movement_now = pygame.time.get_ticks()
            if self.time_for_movement_now - self.time_for_movement_last >= 65:
                self.position_value_down = (self.position_value_down + 1) % 4
                self.position_value_left = 3
                self.position_value_right = 3
                self.position_value_up = 3

                self.sprite_update('down')

                if self.rect.bottom < self.screen_rect.bottom:
                    self.rect.y -= -5
                self.time_for_movement_last = None

        if self.movie_left:
            if not self.time_for_movement_last:
                self.time_for_movement_last = pygame.time.get_ticks()
            self.time_for_movement_now = pygame.time.get_ticks()
            if self.time_for_movement_now - self.time_for_movement_last >= 65:
                self.position_value_left = (self.position_value_left + 1) % 4
                self.position_value_down = 3
                self.position_value_right = 3
                self.position_value_up = 3

                self.sprite_update('left')

                if self.rect.left > self.screen_rect.left:
                    self.rect.x -= 20
                self.time_for_movement_last = None

        if self.movie_right:
            if not self.time_for_movement_last:
                self.time_for_movement_last = pygame.time.get_ticks()
            self.time_for_movement_now = pygame.time.get_ticks()
            if self.time_for_movement_now - self.time_for_movement_last >= 65:
                self.position_value_right = (self.position_value_right + 1) % 4
                self.position_value_down = 3
                self.position_value_left = 3
                self.position_value_up = 3

                self.sprite_update('right')

                if self.rect.right < self.screen_rect.right:
                    self.rect.x -= -20
                self.time_for_movement_last = None

    def sprite_update(self, key):
        if key == 'right':
            self.image = load_image(f"persRight{self.position_value_right + 1}.png", -1, (126, 246))
        elif key == 'left':
            self.image = load_image(f"persLeft{self.position_value_left + 1}.png", -1, (126, 246))
        elif key == 'up':
            self.image = load_image(f"persUp{self.position_value_up + 1}.png", -1, (126, 246))
        else:
            self.image = load_image(f"persDown{self.position_value_down + 1}.png", -1, (126, 246))


class BackGround(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("bg.png", 0, (850, 500))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Floor(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("floor.png", 0, (850, 38))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 462


class Divan(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.w = 325
        self.h = 123
        self.image = load_image("div.png", -1, (325, 123))
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 341
        self.player_near_sofa = False


class Table(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.w = 236
        self.h = 108
        self.image = load_image("table.png", -1, (236, 108))
        self.rect = self.image.get_rect()
        self.rect.x = 555
        self.rect.y = 360
        self.player_near_table = False


class Computer(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("comp.png", -1, (144, 116))
        self.rect = self.image.get_rect()
        self.rect.x = 601
        self.rect.y = 250


class ComputerBg(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, *group):
        super().__init__(*group)
        self.w = w
        self.h = h
        self.image = load_image("computer_bg.png", None, (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Kokoro(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image("kokoro2.png", None, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MoneyIcon(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image("money_icon.png", -1, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class LevitationButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, *group):
        super().__init__(*group)
        self.image = load_image("eButton.png", None, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.down_movement_flag = False

    def movement(self):
        if not self.down_movement_flag:
            self.rect.y -= 0.5
        else:
            self.rect.y += 1
        if self.rect.y == self.y - 25:
            self.down_movement_flag = True
        if self.rect.y == self.y:
            self.down_movement_flag = False


class Functions():
    def __init__(self, screen, sets, person, table, ebutton1, ebutton2, sofa):
        self.screen = screen
        self.sets = sets
        self.person = person
        self.table = table
        self.ebutton1 = ebutton1
        self.ebutton2 = ebutton2
        self.sofa = sofa

        self.time_for_health_decrease_last = None
        self.time_for_money_decrease_last = None
        self.time_for_animation_last = None

        self.start_gameplay_flag = False
        self.main_menu_flag = True
        self.genres_menu_flag = True
        self.types_menu_flag = True
        self.ages_menu_flag = True
        self.game_result_menu_flag = True
        self.final_score_flag = False

        self.specifications_place_flag = True

        self.notification_sofa_flag = False
        self.notification_flag = False

        self.money_error_flag = False
        self.sec_error_flag = False
        self.max_lvl_flag = False

        self.last_value_flag = True

        self.computer_level_up_flag = False

        self.computer_bg = ComputerBg(720, 370, 65, 65)

        self.spec_place_bg = ComputerBg(216, 111, 675, -20)

        self.notification_bg = ComputerBg(500, 257, 0, 0)
        self.notification_bg.rect.center = (425, 250)

        self.loose_window_bg = ComputerBg(850, 500, 0, 0)
        self.loose_window_bg.rect.center = (425, 250)

        self.button_game = Button(297, 140, 256, 160, 3, 'Создать игру')
        self.computer_level_up_button = Button(345, 315, 160, 100, 3, 'Прокачка')

        self.genres_buttons = pygame.sprite.Group()
        self.types_buttons = pygame.sprite.Group()
        self.ages_buttons = pygame.sprite.Group()
        self.notification_sofa_buttons = pygame.sprite.Group()
        self.security_buttons = pygame.sprite.Group()

        self.genres_menu_buttons_on_window = False
        self.types_menu_buttons_on_window = False
        self.ages_menu_buttons_on_window = False
        self.security_buttons_on_window = False
        self.button_go_on_window = False

        self.users_flag = False
        self.user = 0

        self.types_lvl1, self.types_lvl2, self.types_lvl3, self.all_types = [], [], [], []

        self.computer_lvl = save_computer_lvl

        self.health_points = save_health_points
        self.money = save_money
        self.health_cost = 1000
        self.sec_cost = 0
        self.sec_text = ''

        self.notification_warning_text = ''
        self.notification_plus_text = ''

        self.button_continue = Button(335, 315, 80, 50, 3, 'Продолжить', False, None, self.notification_sofa_buttons)
        self.button_cancel = Button(435, 315, 80, 50, 3, 'Отмена', False, None, self.notification_sofa_buttons)
        self.button_ok = Button(375, 295, 100, 62.6, 3, 'ОК', False, None, self.notification_sofa_buttons)

        self.button_go = Button(185, 350, 120, 75, 3, 'Создать', False, None)
        self.button_end = Button(545, 350, 120, 75, 3, 'Готово', False, None)

        self.button_loose = Button(275, 180, 300, 188, 3, 'Начать заново', False, None)

        self.full_score = 0

        self.money2 = 0
        self.health_points2 = 0

    def check_events(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                time_now = pygame.time.get_ticks()
                if time_now - self.time_for_health_decrease_last >= 3750:
                    self.health_points -= 1
                if time_now - self.time_for_money_decrease_last >= 15000:
                    self.money -= 10000
                with open("data/" + "saves.txt", 'w', encoding='utf-8') as saves_data:
                    saves_data.write(f"{self.health_points} {self.money} {self.computer_lvl} {self.person.rect.x}"
                                     f" {self.person.rect.y}")
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                print(event.pos)
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w]:
                    self.person.movie_up = True
                if pressed[pygame.K_a]:
                    self.person.movie_left = True
                if pressed[pygame.K_d]:
                    self.person.movie_right = True
                if pressed[pygame.K_s]:
                    self.person.movie_down = True

                if pressed[pygame.K_e] and self.table.player_near_table:
                    self.start_gameplay_flag = True

                if pressed[pygame.K_e] and self.sofa.player_near_sofa:
                    self.notification_sofa_flag = True

                if pressed[pygame.K_ESCAPE] and self.start_gameplay_flag:
                    self.start_gameplay_flag = False
                    self.button_game.button_on_window = False
                    self.button_game.mouse_on_button = False
                    self.button_game.button_pressed = False
                    self.computer_level_up_button.button_on_window = False
                    self.computer_level_up_button.mouse_on_button = False
                    self.computer_level_up_button.button_pressed = False
                    self.specifications_place_flag = True
                    for button in self.genres_buttons:
                        button.button_on_window = False
                        button.mouse_on_button = False
                        button.button_pressed = False
                    for button in self.types_buttons:
                        button.button_on_window = False
                        button.mouse_on_button = False
                        button.button_pressed = False
                    for button in self.ages_buttons:
                        button.button_on_window = False
                        button.mouse_on_button = False
                        button.button_pressed = False
                    self.button_end.button_pressed = False
                    self.button_end.button_on_window = False
                    self.button_end.mouse_on_button = False
                    self.final_score_flag = True
                    self.game_result_menu_flag = False
                    self.security_buttons_on_window = False
                    self.button_go_on_window = False
                    self.users_flag = False
                    self.time_for_animation_last = None
                    self.start_gameplay_flag = False
                    self.final_score_flag = False
                    self.button_game.image = load_image("button.png")
                    self.button_game.button_on_window = False
                    self.button_game.mouse_on_button = False
                    self.button_game.button_pressed = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.person.movie_right = False
                if event.key == pygame.K_a:
                    self.person.movie_left = False
                if event.key == pygame.K_w:
                    self.person.movie_up = False
                if event.key == pygame.K_s:
                    self.person.movie_down = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_game.is_over(pos):
                    self.button_game.image = load_image("button_press.png")
                    self.button_game.button_pressed = True
                    self.button_game.button_on_window = False
                    self.main_menu_flag = False
                    self.computer_level_up_button.button_on_window = False
                    self.computer_level_up_button.mouse_on_button = False
                    self.computer_level_up_button.button_pressed = False

                if self.button_loose.is_over(pos):
                    self.button_loose.button_on_window = False

                    self.start_gameplay_flag = False
                    self.button_game.button_on_window = False
                    self.button_game.mouse_on_button = False
                    self.button_game.button_pressed = False
                    self.computer_level_up_button.button_on_window = False
                    self.computer_level_up_button.mouse_on_button = False
                    self.computer_level_up_button.button_pressed = False
                    self.specifications_place_flag = True
                    for button in self.genres_buttons:
                        button.button_on_window = False
                        button.mouse_on_button = False
                        button.button_pressed = False
                    for button in self.types_buttons:
                        button.button_on_window = False
                        button.mouse_on_button = False
                        button.button_pressed = False
                    for button in self.ages_buttons:
                        button.button_on_window = False
                        button.mouse_on_button = False
                        button.button_pressed = False
                    self.button_end.button_pressed = False
                    self.button_end.button_on_window = False
                    self.button_end.mouse_on_button = False
                    self.final_score_flag = True
                    self.game_result_menu_flag = False
                    self.security_buttons_on_window = False
                    self.button_go_on_window = False
                    self.users_flag = False
                    self.time_for_animation_last = None
                    self.start_gameplay_flag = False
                    self.final_score_flag = False
                    self.button_game.image = load_image("button.png")
                    self.button_game.button_on_window = False
                    self.button_game.mouse_on_button = False
                    self.button_game.button_pressed = False

                    self.time_for_health_decrease_last = None
                    self.time_for_money_decrease_last = None
                    self.time_for_animation_last = None

                    self.notification_sofa_flag = False
                    self.notification_flag = False

                    self.money_error_flag = False
                    self.sec_error_flag = False
                    self.max_lvl_flag = False

                    self.computer_level_up_flag = False

                    self.users_flag = False
                    self.user = 0

                    self.computer_lvl = 1

                    self.health_points = 20
                    self.money = 15000
                    self.health_cost = 1000
                    self.sec_cost = 0
                    self.sec_text = ''

                    self.notification_warning_text = ''
                    self.notification_plus_text = ''

                    self.full_score = 0

                    self.person.rect.x = 365.5
                    self.person.rect.y = 247

                    self.person.image = load_image(f"persDown1.png", -1, (126, 246))

                for button in self.genres_buttons:
                    if button.is_over(pos):
                        button.button_pressed = True
                        self.genres_menu_flag = False
                        game_list.append(button.text)
                        print(game_list)
                        for button1 in self.genres_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False

                for button in self.types_buttons:
                    if button.is_over(pos):
                        self.types_menu_flag = False
                        game_list.append(button.text)
                        print(game_list)
                        button.button_pressed = True
                        for button1 in self.types_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False

                for button in self.ages_buttons:
                    if button.is_over(pos):
                        self.ages_menu_flag = False
                        game_list.append(button.text)
                        print(game_list)
                        button.button_pressed = True
                        for button1 in self.ages_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False

                if self.button_go.is_over(pos):
                    for button1 in self.security_buttons:
                        button1.mouse_on_button = False
                        button1.button_pressed = False
                        button1.button_on_window = False
                    self.button_go.button_pressed = False
                    self.button_go.button_on_window = False
                    self.button_go.mouse_on_button = False
                    self.final_score_flag = True

                if self.computer_level_up_button.is_over(pos):
                    self.computer_level_up_flag = True
                    self.notification_warning_text = "Вы собираетесь купить улучшение уровня вашего компьютера"
                    if self.computer_lvl == 1:
                        self.sec_cost = 30000
                        self.notification_plus_text = 'приносящие больше денег тематики для игр'
                    elif self.computer_lvl == 2:
                        self.sec_cost = 60000
                        self.notification_plus_text = 'приносящие больше денег тематики для игр'
                    self.notification_flag = True
                    self.computer_level_up_button.mouse_on_button = False
                    self.computer_level_up_button.button_pressed = False
                    self.computer_level_up_button.button_on_window = False

                if self.button_continue.button_on_window and self.notification_flag and self.computer_level_up_flag:
                    if self.button_continue.is_over(pos):
                        if self.money < self.sec_cost:
                            self.money_error_flag = True
                            return 0
                        if self.computer_lvl == 3:
                            self.max_lvl_flag = True
                            return 0
                        self.notification_flag = False
                        self.computer_level_up_flag = False
                        self.button_continue.button_pressed = True
                        self.money -= self.sec_cost
                        self.computer_lvl += 1
                        for button1 in self.notification_sofa_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False
                        self.computer_level_up_button.button_on_window = True
                        self.health_cost *= self.computer_lvl

                if self.button_cancel.button_on_window and self.notification_flag and self.computer_level_up_flag:
                    if self.button_cancel.is_over(pos):
                        self.money_error_flag = False
                        self.sec_error_flag = False
                        self.max_lvl_flag = False
                        self.notification_flag = False
                        self.computer_level_up_flag = False
                        self.button_cancel.button_pressed = True
                        for button1 in self.notification_sofa_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False
                        self.computer_level_up_button.button_on_window = True

                if self.button_end.is_over(pos):
                    self.button_end.button_pressed = False
                    self.button_end.button_on_window = False
                    self.button_end.mouse_on_button = False
                    self.final_score_flag = True
                    self.game_result_menu_flag = False
                    self.security_buttons_on_window = False
                    self.button_go_on_window = False
                    self.users_flag = False
                    self.time_for_animation_last = None
                    self.start_gameplay_flag = False
                    self.final_score_flag = False
                    self.button_game.image = load_image("button.png")
                    self.button_game.button_on_window = False
                    self.button_game.mouse_on_button = False
                    self.button_game.button_pressed = False
                    self.money += self.full_score
                    self.specifications_place_flag = True

                for button in self.security_buttons:
                    if button.is_over(pos):
                        self.sec_text = button.text
                        print(game_list)

                        for button1 in self.security_buttons:
                            button.image = load_image("button.png", None, (button.width, button.height))
                            button1.mouse_on_button = False
                            button1.button_pressed = False
                            button1.button_on_window = False
                        button.button_pressed = True

                        if button.text == 'Защита 1':
                            self.notification_warning_text = "Вы собираетесь купить защиту от пиратства 1го уровня"
                            self.sec_cost = 6000
                            self.notification_plus_text = 'увеличение дохода от игры в 1,5 раза'
                        elif button.text == 'Защита 2':
                            self.notification_warning_text = "Вы собираетесь купить защиту от пиратства 2го уровня"
                            self.sec_cost = 20000
                            self.notification_plus_text = 'увеличение дохода от игры в 2 раза'
                        else:
                            self.notification_warning_text = "Вы собираетесь купить защиту от пиратства 3го уровня"
                            self.sec_cost = 50000
                            self.notification_plus_text = 'увеличение дохода от игры в 2,5 раза'
                        self.notification_flag = True

                if self.button_continue.button_on_window and self.notification_flag and not self.computer_level_up_flag:
                    if self.button_continue.is_over(pos):
                        if self.money < self.sec_cost:
                            self.money_error_flag = True
                            return 0
                        if game_list[3][-1] != 'т':
                            if int(game_list[3][-1]) >= int(self.sec_text[-1]):
                                self.sec_error_flag = True
                                return 0
                        self.notification_flag = False
                        self.button_continue.button_pressed = True
                        self.money -= self.sec_cost
                        game_list[3] = self.sec_text
                        for button1 in self.notification_sofa_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False
                        for button1 in self.security_buttons:
                            button1.button_on_window = True

                if self.button_cancel.button_on_window and self.notification_flag and not self.computer_level_up_flag:
                    if self.button_cancel.is_over(pos):
                        self.money_error_flag = False
                        self.sec_error_flag = False
                        self.notification_flag = False
                        self.button_cancel.button_pressed = True
                        for button1 in self.notification_sofa_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False
                        for button1 in self.security_buttons:
                            button1.button_on_window = True

                if self.button_continue.button_on_window and self.notification_sofa_flag:
                    if self.button_continue.is_over(pos):
                        if self.money < self.health_cost:
                            self.money_error_flag = True
                            return 0
                        self.notification_sofa_flag = False
                        self.button_continue.button_pressed = True
                        self.health_points = min(self.health_points + 1, 20)
                        self.money -= self.health_cost
                        for button1 in self.notification_sofa_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False

                if self.button_cancel.button_on_window and self.notification_sofa_flag:
                    if self.button_cancel.is_over(pos):
                        self.money_error_flag = False
                        self.notification_sofa_flag = False
                        self.button_cancel.button_pressed = True
                        for button1 in self.notification_sofa_buttons:
                            button1.button_on_window = False
                            button1.mouse_on_button = False
                            button1.button_pressed = False

                if self.button_ok.button_on_window:
                    if self.button_ok.is_over(pos):
                        self.notification_sofa_flag = False
                        self.button_ok.button_pressed = True
                        self.button_ok.button_on_window = False
                        self.button_ok.mouse_on_button = False
                        self.button_ok.button_pressed = False

            if event.type == pygame.MOUSEMOTION:
                if self.button_loose.button_on_window:
                    self.button_loose.button_check_for_cursor(pos)

            if self.start_gameplay_flag:
                if event.type == pygame.MOUSEMOTION:
                    for button in self.genres_buttons:
                        button.button_check_for_cursor(pos)

                    for button in self.types_buttons:
                        button.button_check_for_cursor(pos)

                    for button in self.ages_buttons:
                        button.button_check_for_cursor(pos)

                    for button in self.notification_sofa_buttons:
                        button.button_check_for_cursor(pos)

                    for button in self.security_buttons:
                        button.button_check_for_cursor(pos)

                    self.button_go.button_check_for_cursor(pos)

                    self.button_end.button_check_for_cursor(pos)

                    self.computer_level_up_button.button_check_for_cursor(pos)

                    if self.button_game.is_over(pos):
                        if not self.button_game.mouse_on_button:
                            self.button_game.image.fill((25, 25, 25), special_flags=pygame.BLEND_RGB_ADD)
                            self.button_game.mouse_on_button = True
                    else:
                        if not self.button_game.button_pressed:
                            self.button_game.image = load_image("button.png")
                            self.button_game.mouse_on_button = False

            if self.notification_sofa_flag:
                if event.type == pygame.MOUSEMOTION:
                    for button in self.notification_sofa_buttons:
                        button.button_check_for_cursor(pos)

    def table_check(self):
        if self.person.rect.bottom < 485 and \
                self.table.rect.x < self.person.rect.center[0] < self.table.rect.x + self.table.w:
            self.screen.blit(self.ebutton1.image, self.ebutton1.rect)
            self.table.player_near_table = True
            self.ebutton1.movement()
        else:
            self.table.player_near_table = False

    def sofa_check(self):
        if self.person.rect.bottom < 485 and \
                self.sofa.rect.x + 50 < self.person.rect.center[0] < self.sofa.rect.x + self.sofa.w - 50:
            self.screen.blit(self.ebutton2.image, self.ebutton2.rect)
            self.sofa.player_near_sofa = True
            self.ebutton2.movement()
        else:
            self.sofa.player_near_sofa = False

    def minus_health(self):
        if not self.time_for_health_decrease_last:
            self.time_for_health_decrease_last = pygame.time.get_ticks()
        time_for_health_decrease_now = pygame.time.get_ticks()
        if time_for_health_decrease_now - self.time_for_health_decrease_last >= 7500:
            self.health_points -= 1
            self.time_for_health_decrease_last = None

    def minus_money(self):
        if not self.time_for_money_decrease_last:
            self.time_for_money_decrease_last = pygame.time.get_ticks()
        time_for_money_decrease_now = pygame.time.get_ticks()
        if time_for_money_decrease_now - self.time_for_money_decrease_last >= 30000:
            self.money -= 10000
            self.time_for_money_decrease_last = None

    def notification(self, warning_text, cost, plus_text):
        if self.notification_flag:
            self.screen.blit(self.notification_bg.image, self.notification_bg.rect)
            font = pygame.font.Font('fonts/DroidSansMono.ttf', 40)
            text = font.render("Предупреждение!", True, (0, 0, 0))
            self.screen.blit(text, (250, 145))

            font = pygame.font.Font('fonts/DroidSansMono.ttf', 14)
            text = font.render(warning_text, True, (0, 0, 0))
            self.screen.blit(text, (192, 215))

            font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)
            text = font.render(f"Вы потратите: {cost}", True, (0, 0, 0))
            self.screen.blit(text, (192, 245))

            money_image = MoneyIcon(366, 243)
            self.screen.blit(money_image.image, money_image.rect)

            font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)
            text = font.render(f"Вы получите: {plus_text}", True, (0, 0, 0))
            self.screen.blit(text, (192, 275))

            for button in self.notification_sofa_buttons:
                button.button_on_window = True

            self.screen.blit(self.button_continue.image, self.button_continue.rect)
            self.screen.blit(self.button_cancel.image, self.button_cancel.rect)
            self.button_cancel.draw1(self.screen, 10)
            self.button_continue.draw1(self.screen, 10)

            if self.money_error_flag:
                font = pygame.font.Font('fonts/DroidSansMono.ttf', 10)
                text = font.render("Ошибка: недостаточно средств", True, (255, 0, 0))
                self.screen.blit(text, (340, 297))

            if self.sec_error_flag:
                font = pygame.font.Font('fonts/DroidSansMono.ttf', 10)
                text = font.render("Ошибка: вы уже умеете эту или выше уровнем защиту для вашей игры",
                                   True, (255, 0, 0))
                self.screen.blit(text, (232.5, 297))

            if self.max_lvl_flag:
                font = pygame.font.Font('fonts/DroidSansMono.ttf', 10)
                text = font.render("Ошибка: вы уже достигли максимального уровня",
                                   True, (255, 0, 0))
                self.screen.blit(text, (293, 297))

    def notification_sofa(self):
        if self.notification_sofa_flag:
            self.screen.blit(self.notification_bg.image, self.notification_bg.rect)
            if self.health_points < 20:
                font = pygame.font.Font('fonts/DroidSansMono.ttf', 40)
                text = font.render("Предупреждение!", True, (0, 0, 0))
                self.screen.blit(text, (250, 145))

                font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)
                text = font.render("Вы собираетесь купить еды для восполнения здоровья", True, (0, 0, 0))
                self.screen.blit(text, (200, 215))

                font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)
                print(self.health_cost)
                text = font.render(f"Вы потратите: {self.health_cost}", True, (0, 0, 0))
                self.screen.blit(text, (200, 245))

                money_image = MoneyIcon(366, 243)
                self.screen.blit(money_image.image, money_image.rect)

                font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)
                text = font.render(f"Вы получите:  1", True, (0, 0, 0))
                self.screen.blit(text, (200, 275))

                kokoro_image = Kokoro(340, 273)
                self.screen.blit(kokoro_image.image, kokoro_image.rect)

                for button in self.notification_sofa_buttons:
                    button.button_on_window = True

                self.screen.blit(self.button_continue.image, self.button_continue.rect)
                self.screen.blit(self.button_cancel.image, self.button_cancel.rect)
                self.button_cancel.draw1(self.screen, 10)
                self.button_continue.draw1(self.screen, 10)

                if self.money_error_flag:
                    font = pygame.font.Font('fonts/DroidSansMono.ttf', 10)
                    text = font.render("Ошибка: недостаточно средств", True, (255, 0, 0))
                    self.screen.blit(text, (340, 297))

            else:
                font = pygame.font.Font('fonts/DroidSansMono.ttf', 17)
                text = font.render("Ваше здоровье уже восполнено до максимума!", True, (0, 0, 0))
                self.screen.blit(text, (217.5, 230))

                self.button_ok.button_on_window = True

                self.screen.blit(self.button_ok.image, self.button_ok.rect)

                self.button_ok.draw1(self.screen, 17)

    def specifications_place(self):
        self.screen.blit(self.spec_place_bg.image, self.spec_place_bg.rect)

        kokoro_image = Kokoro(680, 33)
        self.screen.blit(kokoro_image.image, kokoro_image.rect)

        money_image = MoneyIcon(680, 58)
        self.screen.blit(money_image.image, money_image.rect)

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)
        text = font.render("Игровые показатели:", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.spec_place_bg.rect.center
        self.screen.blit(text, (text_rect[0] - 20, 10))

        kokoro_value = font.render(f"{self.health_points}", True, (0, 0, 0))
        self.screen.blit(kokoro_value, (704, 34))

        money_value = font.render(f"{self.money}", True, (0, 0, 0))
        self.screen.blit(money_value, (704, 59))

    def main_computer_menu(self):
        font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)

        kokoro_image = Kokoro(75, 135)
        self.screen.blit(kokoro_image.image, kokoro_image.rect)

        money_image = MoneyIcon(75, 160)
        self.screen.blit(money_image.image, money_image.rect)

        kokoro_value = font.render(f"{self.health_points}", True, (0, 0, 0))
        self.screen.blit(kokoro_value, (99, 136))

        money_value = font.render(f"{self.money}", True, (0, 0, 0))
        self.screen.blit(money_value, (99, 161))

        black_rect = pygame.draw.rect(self.screen, (0, 0, 0), (80, 120, 695, 1))
        font = pygame.font.Font('fonts/DroidSansMono.ttf', 40)
        main_text = font.render("Главное меню разработки", True, (0, 0, 0))
        self.screen.blit(main_text, (147.5, 70))

        self.screen.blit(self.button_game.image, self.button_game.rect)
        self.button_game.button_on_window = True

        self.screen.blit(self.computer_level_up_button.image, self.computer_level_up_button.rect)
        self.computer_level_up_button.button_on_window = True

        self.button_game.draw1(self.screen, 30)
        self.computer_level_up_button.draw1(self.screen, 20)

    def genres_menu(self):
        font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)

        kokoro_image = Kokoro(75, 135)
        self.screen.blit(kokoro_image.image, kokoro_image.rect)

        money_image = MoneyIcon(75, 160)
        self.screen.blit(money_image.image, money_image.rect)

        kokoro_value = font.render(f"{self.health_points}", True, (0, 0, 0))
        self.screen.blit(kokoro_value, (99, 136))

        money_value = font.render(f"{self.money}", True, (0, 0, 0))
        self.screen.blit(money_value, (99, 161))

        global game_list
        game_list = []

        black_rect = pygame.draw.rect(self.screen, (0, 0, 0), (80, 120, 695, 1))
        font = pygame.font.Font('fonts/DroidSansMono.ttf', 40)
        main_text = font.render("Выберите жанр вашей игры", True, (0, 0, 0))
        self.screen.blit(main_text, (137.5, 70))

        genres = ['RPG', 'Adventure', 'Action', 'Simulator', 'Strategy', 'Casual']

        if not self.genres_menu_buttons_on_window:
            x = 75
            for genre in genres:
                Button(x, 230, 108.3, 67.5, 3, genre, False, None, self.genres_buttons)
                x += 118

            self.genres_menu_buttons_on_window = True

        for button in self.genres_buttons:
            button.button_on_window = True

        self.genres_buttons.draw(self.screen)
        self.genres_buttons.update(self.screen, 15)

    def types_menu(self):
        font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)

        kokoro_image = Kokoro(75, 135)
        self.screen.blit(kokoro_image.image, kokoro_image.rect)

        money_image = MoneyIcon(75, 160)
        self.screen.blit(money_image.image, money_image.rect)

        kokoro_value = font.render(f"{self.health_points}", True, (0, 0, 0))
        self.screen.blit(kokoro_value, (99, 136))

        money_value = font.render(f"{self.money}", True, (0, 0, 0))
        self.screen.blit(money_value, (99, 161))

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 35)
        main_text = font.render("Выберите тематику вашей игры", True, (0, 0, 0))
        self.screen.blit(main_text, (132.5, 70))
        black_rect = pygame.draw.rect(self.screen, (0, 0, 0), (80, 113, 695, 1))

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)
        first_lvl_text = font.render("Доступно на 1ом уровне:", True, (0, 0, 0))
        self.screen.blit(first_lvl_text, (322.5, 115))

        second_lvl_text = font.render("Доступно на 2ом уровне:", True, (0, 0, 0))
        self.screen.blit(second_lvl_text, (322.5, 237))

        third_lvl_text = font.render("Доступно на 3ем уровне:", True, (0, 0, 0))
        self.screen.blit(third_lvl_text, (322.5, 359))

        if not self.types_menu_buttons_on_window:
            for game_type in self.load_file('game_data.txt'):
                if game_type[0] == '1':
                    self.types_lvl1.append(game_type[1:])
                elif game_type[0] == '2':
                    self.types_lvl2.append(game_type[1:])
                else:
                    self.types_lvl3.append(game_type[1:])
                self.all_types.append(game_type[1:])

            x, x1, s = 157.1, 103.7, 0
            for game_type in self.types_lvl1:
                if s < 6:
                    Button(x, 135, 76.8, 48, 1, game_type[0], False, None, self.types_buttons)
                    x += 91.8
                else:
                    Button(x1, 185, 76.8, 48, 1, game_type[0], False, None, self.types_buttons)
                    x1 += 91.8
                s += 1

            x, x1, s = 157.1, 103.7, 0
            for game_type in self.types_lvl2:
                if s < 6:
                    Button(x, 257, 76.8, 48, 2, game_type[0], False, None, self.types_buttons)
                    x += 91.8
                else:
                    Button(x1, 307, 76.8, 48, 2, game_type[0], False, None, self.types_buttons)
                    x1 += 91.8
                s += 1

            x = 103.7
            for game_type in self.types_lvl3:
                Button(x, 379, 76.8, 48, 3, game_type[0], False, None, self.types_buttons)
                x += 91.8

            self.types_menu_buttons_on_window = True

        for button in self.types_buttons:
            if self.computer_lvl < button.button_lvl:
                button.button_pressed_check()
            else:
                button.button_on_window = True

        self.types_buttons.draw(self.screen)
        self.types_buttons.update(self.screen, 12)

    def ages_menu(self):
        font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)

        kokoro_image = Kokoro(75, 135)
        self.screen.blit(kokoro_image.image, kokoro_image.rect)

        money_image = MoneyIcon(75, 160)
        self.screen.blit(money_image.image, money_image.rect)

        kokoro_value = font.render(f"{self.health_points}", True, (0, 0, 0))
        self.screen.blit(kokoro_value, (99, 136))

        money_value = font.render(f"{self.money}", True, (0, 0, 0))
        self.screen.blit(money_value, (99, 161))

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 30)
        main_text = font.render("Выберите основную аудиторию вашей игры", True, (0, 0, 0))
        self.screen.blit(main_text, (82.5, 75))
        black_rect = pygame.draw.rect(self.screen, (0, 0, 0), (80, 113, 695, 1))

        ages = ['6+', '12+', '18+']

        for game_ages in ages:
            if not self.ages_menu_buttons_on_window:
                x = 85
                for game_ages in ages:
                    Button(x, 190, 213.3, 133.3, 3, game_ages, False, None, self.ages_buttons)
                    x += 233.3

                self.ages_menu_buttons_on_window = True

            for button in self.ages_buttons:
                button.button_on_window = True

            self.ages_buttons.draw(self.screen)
            self.ages_buttons.update(self.screen, 60)

    def game_result_menu(self):
        font = pygame.font.Font('fonts/DroidSansMono.ttf', 15)

        kokoro_image = Kokoro(445, 100)
        self.screen.blit(kokoro_image.image, kokoro_image.rect)

        money_image = MoneyIcon(445, 125)
        self.screen.blit(money_image.image, money_image.rect)

        kokoro_value = font.render(f"{self.health_points}", True, (0, 0, 0))
        self.screen.blit(kokoro_value, (469, 101))

        money_value = font.render(f"{self.money}", True, (0, 0, 0))
        self.screen.blit(money_value, (469, 126))

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 30)
        main_text = font.render("Ваша игра:", True, (0, 0, 0))
        self.screen.blit(main_text, (82.5, 82.5))
        black_rect = pygame.draw.rect(self.screen, (0, 0, 0), (425, 80, 1, 340))

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 20)
        main_text = font.render(f"Жанр игры: {game_list[0]}", True, (0, 0, 0))
        self.screen.blit(main_text, (82.5, 130))

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 20)
        main_text = font.render(f"Тематика игры: {game_list[1]}", True, (0, 0, 0))
        self.screen.blit(main_text, (82.5, 170))

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 20)
        main_text = font.render(f"Возврастное ограничение: {game_list[2]}", True, (0, 0, 0))
        self.screen.blit(main_text, (82.5, 210))

        if len(game_list) == 3:
            game_list.append('Отсутствует')

        if not self.security_buttons_on_window:
            x = 78
            for security_version in ['Защита 1', 'Защита 2', 'Защита 3']:
                Button(x, 280, 100, 62.5, 3, security_version, False, None, self.security_buttons)
                x += 118

            for button in self.security_buttons:
                button.button_on_window = True

            self.security_buttons_on_window = True

        font = pygame.font.Font('fonts/DroidSansMono.ttf', 17)
        main_text = font.render(f"Защита от пиратства: {game_list[3]}", True, (0, 0, 0))
        self.screen.blit(main_text, (82.5, 250))

        self.security_buttons.draw(self.screen)
        self.security_buttons.update(self.screen, 15)

        self.screen.blit(self.button_go.image, self.button_go.rect)
        self.button_go.draw1(self.screen, 20)

        if not self.button_go_on_window:
            self.button_go.button_on_window = True
            self.button_go_on_window = True

        if self.final_score_flag:
            self.final_score()

    def final_score(self):
        font = pygame.font.Font('fonts/DroidSansMono.ttf', 25)

        if not self.users_flag:
            self.user = randint(0, 10)

        if not self.time_for_animation_last:
            self.time_for_animation_last = pygame.time.get_ticks()
        time_for_animation_now = pygame.time.get_ticks()

        if time_for_animation_now - self.time_for_animation_last >= 1000:

            for sc in self.all_types:
                index = self.all_types.index(sc)
                if sc[0] == game_list[1]:
                    genre_age_score = int(self.all_types[index][self.return_list_id_genre()]) + \
                                      int(self.all_types[index][self.return_list_id_age()]) + 2

            main_text = font.render(f"Итоговый счет игры:{genre_age_score}", True, (0, 0, 0))
            self.screen.blit(main_text, (435, 170))

        if time_for_animation_now - self.time_for_animation_last >= 2000:

            if time_for_animation_now - self.time_for_animation_last >= 3000:
                self.users_flag = True
                text = font.render(f"Оценка пользователей:{self.user}", True, (0, 0, 0))
                self.screen.blit(text, (435, 210))
            else:
                text = font.render(f"Оценка пользователей:{self.user}", True, (0, 0, 0))
                self.screen.blit(text, (435, 210))

        if time_for_animation_now - self.time_for_animation_last >= 4000:
            self.full_score = (int((genre_age_score * self.return_type_multiplier() +
                                    self.user * self.return_type_multiplier() / 2) *
                                   self.return_list_security()))

            text = font.render(f"Вы заработали:{self.full_score}", True, (0, 0, 0))

            self.screen.blit(text, (435, 280))

        if time_for_animation_now - self.time_for_animation_last >= 4500:
            self.screen.blit(self.button_end.image, self.button_end.rect)
            self.button_end.draw1(self.screen, 20)

            self.button_end.button_on_window = True

    def return_type_multiplier(self):
        for type_ in self.types_lvl1:
            if game_list[1] == type_[0]:
                return 1000

        for type_ in self.types_lvl2:
            if game_list[1] == type_[0]:
                return 2000

        for type_ in self.types_lvl3:
            if game_list[1] == type_[0]:
                return 3000

    def return_list_security(self):
        if game_list[3] == 'Отсутствует':
            return 1
        if game_list[3] == 'Защита 1':
            return 1.5
        if game_list[3] == 'Защита 2':
            return 2
        if game_list[3] == 'Защита 3':
            return 2.5

    def return_list_id_age(self):
        if game_list[2] == '6+':
            return 7
        if game_list[2] == '12+':
            return 8
        if game_list[2] == '18+':
            return 9

    def return_list_id_genre(self):
        if game_list[0] == 'Action':
            return 1
        if game_list[0] == 'Adventure':
            return 2
        if game_list[0] == 'RPG':
            return 3
        if game_list[0] == 'Simulator':
            return 4
        if game_list[0] == 'Strategy':
            return 5
        if game_list[0] == 'Casual':
            return 6

    def start_gameplay(self):
        if not self.start_gameplay_flag:
            self.main_menu_flag = True
            self.genres_menu_flag = True
            self.types_menu_flag = True
            self.ages_menu_flag = True
            self.game_result_menu_flag = True
            return 0

        self.screen.blit(self.computer_bg.image, self.computer_bg.rect)

        self.specifications_place_flag = False

        if self.main_menu_flag:
            self.main_computer_menu()
        else:
            if self.genres_menu_flag:
                self.genres_menu()
            else:
                if self.types_menu_flag:
                    self.types_menu()
                else:
                    if self.ages_menu_flag:
                        self.ages_menu()
                    else:
                        if self.game_result_menu_flag:
                            self.game_result_menu()

    def loose_window(self):
        if self.money <= 0 or self.health_points <= 0:

            if self.last_value_flag:
                self.money2 = self.money
                self.health_points2 = self.health_points
                self.last_value_flag = False

            # sys.exit()
            self.screen.blit(self.loose_window_bg.image, self.loose_window_bg.rect)
            self.screen.blit(self.button_loose.image, self.button_loose.rect)

            self.button_loose.draw1(self.screen, 30)

            font = pygame.font.Font('fonts/DroidSansMono.ttf', 40)
            main_text = font.render(f"Вы проиграли((", True, (0, 0, 0))
            self.screen.blit(main_text, (260, 100))

            self.button_loose.button_on_window = True

            self.specifications_place()

            if self.money <= 0:
                self.money = 0
                self.health_points = self.health_points2

            if self.health_points <= 0:
                self.health_points = 0
                self.money = self.money2

    def load_file(self, filename):
        filename = "data/" + filename
        with open(filename, 'r', encoding='utf-8') as game_data:
            game_data_list = [line.strip().split() for line in game_data]
        return game_data_list


def load_image(name, color_key=None, scale_trans=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)

    if scale_trans is not None:
        image = pygame.transform.scale(image, scale_trans)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_game():
    global save_money, save_computer_lvl, save_health_points, save_person_x, save_person_y, save_time_for_health
    global save_time_for_money
    with open("data/" + "saves.txt", 'r', encoding='utf-8') as saves_data:
        saves_data_list = [line.strip().split() for line in saves_data]
        save_money = int(saves_data_list[0][1])
        save_computer_lvl = int(saves_data_list[0][2])
        save_health_points = int(saves_data_list[0][0])
        save_person_x = float(saves_data_list[0][3])
        save_person_y = float(saves_data_list[0][4])


def run_game():
    sets = Sets()
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((sets.screen_width, sets.screen_height))

    all_sprites = pygame.sprite.Group()
    background = BackGround(all_sprites)
    floor = Floor(all_sprites)
    divan = Divan(all_sprites)
    table = Table(all_sprites)
    comp = Computer(all_sprites)
    ebutton1 = LevitationButton(640, 150, 50, 50)
    ebutton2 = LevitationButton(165, 165, 50, 50)
    person = Creature(screen, floor, all_sprites)

    # button = Button((0, 255, 0), 100, 100, 40, 40, 'e')

    gf = Functions(screen, sets, person, table, ebutton1, ebutton2, divan)

    running = True
    while running:

        clock.tick(sets.fps)

        all_sprites.draw(screen)

        gf.check_events()

        if not gf.start_gameplay_flag and not gf.notification_sofa_flag:
            gf.table_check()
            gf.sofa_check()

        if gf.specifications_place_flag:
            gf.specifications_place()

        gf.notification_sofa()

        gf.minus_health()

        gf.minus_money()

        gf.start_gameplay()

        if not gf.start_gameplay_flag and not gf.notification_sofa_flag:
            all_sprites.update()

        gf.notification(gf.notification_warning_text, gf.sec_cost, gf.notification_plus_text)

        gf.loose_window()

        pygame.display.flip()
    pygame.quit()


load_game()
run_game()
