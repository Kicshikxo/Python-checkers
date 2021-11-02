from checkers.enums import CheckerType

class Checker:
    def __init__(self, x: int, y: int, type: CheckerType = CheckerType.NONE):
        self.__x = x
        self.__y = y
        self.__type = type

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def type(self):
        return self.__type

    def change_type(self, type: CheckerType):
        '''Изменение типа шишки'''
        self.__type = type