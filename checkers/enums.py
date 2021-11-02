from enum import Enum, auto

class SideType(Enum):
    WHITE = auto()
    BLACK = auto()

class CheckerType(Enum):
    NONE = auto()
    WHITE_REGULAR = auto()
    BLACK_REGULAR = auto()
    WHITE_QUEEN = auto()
    BLACK_QUEEN = auto()