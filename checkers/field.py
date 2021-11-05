from checkers.enums import CheckerType
from checkers.checker import Checker
from checkers.constants import WHITE_CHECKERS, BLACK_CHECKERS
from checkers.point import Point

from functools import reduce

class Field:
    def __init__(self, x_size: int, y_size: int):
        self.__x_size = x_size
        self.__y_size = y_size
        self.__generate()

    @property
    def x_size(self) -> int:
        return self.__x_size

    @property
    def y_size(self) -> int:
        return self.__y_size

    @property
    def size(self) -> int:
        return max(self.x_size, self.y_size)

    @classmethod
    def copy(cls, field_instance):
        '''Создаёт копию поля из образца'''
        field_copy = cls(field_instance.x_size, field_instance.y_size)

        for y in range(field_instance.y_size):
            for x in range(field_instance.x_size):
                field_copy.at(x, y).change_type(field_instance.type_at(x, y))

        return field_copy

    def __generate(self):
        '''Генерация поля с шашками'''
        self.__checkers = [[Checker() for x in range(self.x_size)] for y in range(self.y_size)]
        
        for y in range(self.y_size):
            for x in range(self.x_size):
                if ((y + x) % 2):
                    if (y < 3):
                        self.__checkers[y][x].change_type(CheckerType.BLACK_REGULAR)
                    elif (y >= self.y_size - 3):
                        self.__checkers[y][x].change_type(CheckerType.WHITE_REGULAR)

    def type_at(self, x: int, y: int) -> CheckerType:
        '''Получение типа шашки на поле по координатам'''
        return self.__checkers[y][x].type

    def at(self, x: int, y: int) -> Checker:
        '''Получение шашки на поле по координатам'''
        return self.__checkers[y][x]

    def is_within(self, x: int, y: int) -> bool:
        '''Определяет лежит ли точка в пределах поля'''
        return (0 <= x < self.x_size and 0 <= y < self.y_size)

    @property
    def white_checkers_count(self) -> int:
        '''Количество белых шашек на поле'''
        return sum(reduce(lambda acc, checker: acc + (checker.type in WHITE_CHECKERS), checkers, 0) for checkers in self.__checkers)

    @property
    def black_checkers_count(self) -> int:
        '''Количество чёрных шашек на поле'''
        return sum(reduce(lambda acc, checker: acc + (checker.type in BLACK_CHECKERS), checkers, 0) for checkers in self.__checkers)

    @property
    def white_score(self) -> int:
        '''Счёт белых'''
        return sum(reduce(lambda acc, checker: acc + (checker.type == CheckerType.WHITE_REGULAR) + (checker.type == CheckerType.WHITE_QUEEN) * 3, checkers, 0) for checkers in self.__checkers)
    
    @property
    def black_score(self) -> int:
        '''Счёт чёрных'''
        return sum(reduce(lambda acc, checker: acc + (checker.type == CheckerType.BLACK_REGULAR) + (checker.type == CheckerType.BLACK_QUEEN) * 3, checkers, 0) for checkers in self.__checkers)