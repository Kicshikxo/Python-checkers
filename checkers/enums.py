from enum import Enum, auto

class SideType(Enum):
    WHITE = auto()
    BLACK = auto()

    def opposite(side):
        if (side == SideType.WHITE):
            return SideType.BLACK
        elif (side == SideType.BLACK):
            return SideType.WHITE
        raise ValueError()

class CheckerType(Enum):
    NONE = auto()
    WHITE_REGULAR = auto()
    BLACK_REGULAR = auto()
    WHITE_QUEEN = auto()
    BLACK_QUEEN = auto()