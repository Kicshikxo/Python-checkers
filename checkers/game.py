from tkinter import Canvas, Event, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from time import sleep
from random import choice
from math import inf

from checkers.field import Field
from checkers.move import Move
from checkers.constants import *
from checkers.enums import CheckerType, SideType

class Game:
    def __init__(self, canvas: Canvas, x_field_size: int, y_field_size: int):
        self.__canvas = canvas
        self.__field = Field(x_field_size, y_field_size)

        self.__player_turn = True

        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()

        self.__init_images()
        
        self.__draw()

    def __init_images(self):
        '''Инициализация изображений'''
        self.__images = {
            CheckerType.WHITE_REGULAR: ImageTk.PhotoImage(Image.open(Path('assets', 'white-regular.png')).resize((CELL_SIZE, CELL_SIZE), Image.ANTIALIAS)),
            CheckerType.BLACK_REGULAR: ImageTk.PhotoImage(Image.open(Path('assets', 'black-regular.png')).resize((CELL_SIZE, CELL_SIZE), Image.ANTIALIAS)),
            CheckerType.WHITE_QUEEN: ImageTk.PhotoImage(Image.open(Path('assets', 'white-queen.png')).resize((CELL_SIZE, CELL_SIZE), Image.ANTIALIAS)),
            CheckerType.BLACK_QUEEN: ImageTk.PhotoImage(Image.open(Path('assets', 'black-queen.png')).resize((CELL_SIZE, CELL_SIZE), Image.ANTIALIAS)),
        }

    def __animate_move(self, move: Move):
        '''Анимация перемещения шашки'''
        self.__animated_cell = Point(move.from_x, move.from_y)
        self.__draw()

        # Создание шашки для анимации
        animated_checker = self.__canvas.create_image(move.from_x * CELL_SIZE, move.from_y * CELL_SIZE, image=self.__images.get(self.__field.type_at(move.from_x, move.from_y)), anchor='nw', tag='animated_checker')
        
        # Вектора движения
        dx = 1 if move.from_x < move.to_x else -1
        dy = 1 if move.from_y < move.to_y else -1

        # Анимация
        for distance in range(abs(move.from_x - move.to_x)):
            for _ in range(100 // ANIMATION_SPEED):
                self.__canvas.move(animated_checker, ANIMATION_SPEED / 100 * CELL_SIZE * dx, ANIMATION_SPEED / 100 * CELL_SIZE * dy)
                self.__canvas.update()
                sleep(0.01)

        self.__animated_cell = Point()

    def __draw(self):
        '''Отрисовка сетки поля и шашек'''
        self.__canvas.delete('all')
        self.__draw_field_grid()
        self.__draw_checkers()

    def __draw_field_grid(self):
        '''Отрисовка сетки поля'''
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                self.__canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE, fill=FIELD_COLORS[(y + x) % 2], width=0, tag='boards')

                # Отрисовка рамок у необходимых клеток
                if (x == self.__selected_cell.x and y == self.__selected_cell.y):
                    self.__canvas.create_rectangle(x * CELL_SIZE + BORDER_WIDTH // 2, y * CELL_SIZE + BORDER_WIDTH // 2, x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2, y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2, outline=SELECT_BORDER_COLOR, width=BORDER_WIDTH, tag='border')
                elif (x == self.__hovered_cell.x and y == self.__hovered_cell.y):
                    self.__canvas.create_rectangle(x * CELL_SIZE + BORDER_WIDTH // 2, y * CELL_SIZE + BORDER_WIDTH // 2, x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2, y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2, outline=HOVER_BORDER_COLOR,  width=BORDER_WIDTH, tag='border')

                # Отрисовка возможных точек перемещения, если есть выбранная ячейка
                if (self.__selected_cell):
                    white_moves_list = self.__get_moves_list(SideType.WHITE)
                    for move in white_moves_list:
                        if (self.__selected_cell.x == move.from_x and self.__selected_cell.y == move.from_y):
                            self.__canvas.create_oval(move.to_x * CELL_SIZE + CELL_SIZE / 3, move.to_y * CELL_SIZE + CELL_SIZE / 3, move.to_x * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3), move.to_y * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3), fill=POSIBLE_MOVE_CIRCLE_COLOR, width=0, tag='posible_move_circle' )

    def __draw_checkers(self):
        '''Отрисовка шашек'''
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Не отрисовывать пустые ячейки и анимируемую шашку
                if (self.__field.type_at(x, y) != CheckerType.NONE and not (x == self.__animated_cell.x and y == self.__animated_cell.y)):
                    self.__canvas.create_image(x * CELL_SIZE, y * CELL_SIZE, image=self.__images.get(self.__field.type_at(x, y)), anchor='nw', tag='checkers')

    def mouse_move(self, event: Event):
        '''Событие перемещения мышки'''

        x, y = (event.x) // CELL_SIZE, (event.y) // CELL_SIZE
        if (x != self.__hovered_cell.x or y != self.__hovered_cell.y):
            self.__hovered_cell = Point(x, y)

            # Если ход игрока, то перерисовать
            if (self.__player_turn):
                self.__draw()

    def mouse_down(self, event: Event):
        '''Событие нажатия мышки'''
        if not (self.__player_turn): return

        x, y = (event.x) // CELL_SIZE, (event.y) // CELL_SIZE

        # Если точка не внутри поля
        if not (self.__field.is_within(x, y)): return

        # Если нажатие по белой шашке, то выбрать её
        if (self.__field.type_at(x, y) in WHITE_CHECKERS):
            self.__selected_cell = Point(x, y)
            self.__draw()
        elif (self.__player_turn):
            move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)

            # Если нажатие по ячейке, на которую можно походить
            if (move in self.__get_moves_list(SideType.WHITE)):
                self.__handle_white_turn(move)

                # Если не ход игрока, то ход чёрных
                if not (self.__player_turn):
                    self.__handle_black_turn()

    def __handle_move(self, move: Move, draw: bool = True) -> bool:
        '''Совершение хода'''
        if (draw): self.__animate_move(move)

        # Изменение типа шашки, если она дошла до края
        if (move.to_y == 0 and self.__field.type_at(move.from_x, move.from_y) == CheckerType.WHITE_REGULAR):
            self.__field.at(move.from_x, move.from_y).change_type(CheckerType.WHITE_QUEEN)
        elif (move.to_y == self.__field.y_size - 1 and self.__field.type_at(move.from_x, move.from_y) == CheckerType.BLACK_REGULAR):
            self.__field.at(move.from_x, move.from_y).change_type(CheckerType.BLACK_QUEEN)

        # Изменение позиции шашки
        self.__field.at(move.to_x, move.to_y).change_type(self.__field.type_at(move.from_x, move.from_y))
        self.__field.at(move.from_x, move.from_y).change_type(CheckerType.NONE)

        # Вектора движения
        dx = -1 if move.from_x < move.to_x else 1
        dy = -1 if move.from_y < move.to_y else 1

        # Удаление съеденной ячейки
        has_killed_checker = False
        x, y = move.to_x, move.to_y
        while (x != move.from_x or y != move.from_y):
            x += dx
            y += dy
            if (self.__field.type_at(x, y) != CheckerType.NONE):
                self.__field.at(x, y).change_type(CheckerType.NONE)
                has_killed_checker = True

        if (draw): self.__draw()

        return has_killed_checker

    def __handle_white_turn(self, move: Move):
        '''Обработка хода белых (игрока)'''
        self.__player_turn = False

        moves_list = self.__get_moves_list(SideType.WHITE)
        if (move in moves_list):
            # Была ли убита шашка
            has_killed_checker = self.__handle_move(move)

            required_moves_list = list(filter(lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y, self.__get_required_moves_list(SideType.WHITE)))
            
            # Если есть ещё ход этой же шашкой
            if (has_killed_checker and required_moves_list):
                self.__player_turn = True

        self.__selected_cell = Point()

    def __handle_black_turn(self):
        '''Обработка хода чёрных (компьютера)'''
        moves_list = self.__predict_optimal_move(SideType.BLACK)

        if (moves_list):
            for move in moves_list:
                self.__handle_move(move)
                
            self.__player_turn = True
        
        self.__check_for_game_over()

    def __check_for_game_over(self):
        game_over = False
        
        white_moves_list = self.__get_moves_list(SideType.WHITE)
        if not (white_moves_list):
            # Белые проиграли
            answer = messagebox.showinfo('Конец игры', 'Чёрные выиграли')
            game_over = True

        black_moves_list = self.__get_moves_list(SideType.BLACK)
        if not (black_moves_list):
            # Чёрные проиграли
            answer = messagebox.showinfo('Конец игры', 'Белые выиграли')
            game_over = True
        
        if (game_over):
            self.__init__(self.__canvas, self.__field.x_size, self.__field.y_size)

    def __predict_optimal_move(self, side: SideType) -> list[Move]:
        '''Предсказать оптимальный ход'''
        optimal_moves = []
        best_result = 0
        all_moves_list = self.__get_predicted_moves_list(side)

        field_copy = Field.copy(self.__field)
        for moves in all_moves_list:
            for move in moves:
                self.__handle_move(move, draw=False)

            if (side == SideType.WHITE):
                try:
                    result = self.__field.white_checkers_count / self.__field.black_checkers_count
                except ZeroDivisionError:
                    result = inf
            elif (side == SideType.BLACK):
                try:
                    result = self.__field.black_checkers_count / self.__field.white_checkers_count
                except ZeroDivisionError:
                    result = inf
            
            if (result > best_result):
                best_result = result
                optimal_moves.clear()
                optimal_moves.append(moves)
            elif (result == best_result):
                optimal_moves.append(moves)

            self.__field = Field.copy(field_copy)

        optimal_move = []
        if (optimal_moves):
            for move in choice(optimal_moves):
                if   (side == SideType.WHITE and self.__field.type_at(move.from_x, move.from_y) in BLACK_CHECKERS): break
                elif (side == SideType.BLACK and self.__field.type_at(move.from_x, move.from_y) in WHITE_CHECKERS): break

                optimal_move.append(move)

        return optimal_move

    def __get_predicted_moves_list(self, side: SideType, current_prediction_depth: int = 0, all_moves_list: list[Move] = [], saved_moves_list: list[Move] = [], moves_list: list[Move] = []) -> list[Move]:
        '''Предсказать все возможные ходы'''

        if (saved_moves_list):
            all_moves_list.append(saved_moves_list)
        else:
            all_moves_list.clear()

        if not (moves_list):
            moves_list = self.__get_moves_list(side)

        if (moves_list and current_prediction_depth < MAX_PREDICTION_DEPTH):
            field_copy = Field.copy(self.__field)
            for move in moves_list:
                has_killed_checker = self.__handle_move(move, draw=False)

                required_moves_list = list(filter(lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y, self.__get_required_moves_list(side)))

                # Если есть ещё ход этой же шашкой
                if (has_killed_checker and required_moves_list):
                    self.__get_predicted_moves_list(side, current_prediction_depth, all_moves_list, saved_moves_list + [move], required_moves_list)
                else:
                    self.__get_predicted_moves_list(SideType.opposite(side), current_prediction_depth + 1, all_moves_list, saved_moves_list + [move])

                self.__field = Field.copy(field_copy)

        return all_moves_list

    def __get_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка ходов'''
        moves_list = self.__get_required_moves_list(side)
        if not (moves_list):
            moves_list = self.__get_optional_moves_list(side)
        return moves_list

    def __get_required_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка обязательных ходов'''
        moves_list = []

        # Определение типов шашек
        if (side == SideType.WHITE):
            friendly_checkers = WHITE_CHECKERS
            enemy_checkers = BLACK_CHECKERS
        elif (side == SideType.BLACK):
            friendly_checkers = BLACK_CHECKERS
            enemy_checkers = WHITE_CHECKERS
        else: return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):

                # Для обычной шашки
                if (self.__field.type_at(x, y) == friendly_checkers[0]):
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        if self.__field.type_at(x + offset.x, y + offset.y) in enemy_checkers and self.__field.type_at(x + offset.x * 2, y + offset.y * 2) == CheckerType.NONE:
                            moves_list.append(Move(x, y, x + offset.x * 2, y + offset.y * 2))

                # Для дамки
                elif (self.__field.type_at(x, y) == friendly_checkers[1]):
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        has_enemy_checker_on_way = False

                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue

                            # Если на пути не было вражеской шашки
                            if (not has_enemy_checker_on_way):
                                if (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) in enemy_checkers):
                                    has_enemy_checker_on_way = True
                                    continue
                                # Если на пути союзная шашка - то закончить цикл
                                elif (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) in friendly_checkers):
                                    break
                            
                            # Если на пути была вражеская шашка
                            if (has_enemy_checker_on_way):
                                if (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) == CheckerType.NONE):
                                    moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                                else:
                                    break
                            
        return moves_list

    def __get_optional_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка необязательных ходов'''
        moves_list = []

        # Определение типов шашек
        if (side == SideType.WHITE):
            friendly_checkers = WHITE_CHECKERS
        elif (side == SideType.BLACK):
            friendly_checkers = BLACK_CHECKERS
        else: return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Для обычной шашки
                if (self.__field.type_at(x, y) == friendly_checkers[0]):
                    for offset in MOVE_OFFSETS[:2] if side == SideType.WHITE else MOVE_OFFSETS[2:]:
                        if not (self.__field.is_within(x + offset.x, y + offset.y)): continue

                        if (self.__field.type_at(x + offset.x, y + offset.y) == CheckerType.NONE):
                            moves_list.append(Move(x, y, x + offset.x, y + offset.y))

                # Для дамки
                elif (self.__field.type_at(x, y) == friendly_checkers[1]):
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue

                            if (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) == CheckerType.NONE):
                                moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                            else:
                                break
        return moves_list