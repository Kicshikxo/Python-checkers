class Point:
    def __init__(self, x: int = -1, y: int = -1):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __eq__(self, other):
        if isinstance(other, Point):
            return (
                self.x == other.x and
                self.y == other.y
            )

        return NotImplemented