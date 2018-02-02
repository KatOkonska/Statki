from enum import Enum

class Settings:
    RoomSize = 2
    BoardSize = 20

class BoardDisplay(Enum):
    EMPTY = 0
    PLACED = 1
    SHOT = 2

class ShipOrientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class ShipTypes(Enum):
    __order__ = 'S_1 S_2 S_3 S_4 S_5'
    S_1 = 0
    S_2 = 1
    S_3 = 2
    S_4 = 3
    S_5 = 5

ShipSizes = {ShipTypes.S_1: 1, ShipTypes.S_2: 2, ShipTypes.S_3: 3, ShipTypes.S_4: 4, ShipTypes.S_5: 5}
ShipCounts = {ShipTypes.S_1: 4, ShipTypes.S_2: 3, ShipTypes.S_3: 2, ShipTypes.S_4: 1, ShipTypes.S_5: 0}
