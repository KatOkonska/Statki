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
    S_1 = 0
    S_2 = 1
    S_3 = 2
    S_4 = 3
    S_5 = 5

ShipSizes = {}
ShipSizes[ShipTypes.S_1] = 1
ShipSizes[ShipTypes.S_2] = 2
ShipSizes[ShipTypes.S_3] = 3
ShipSizes[ShipTypes.S_4] = 4
ShipSizes[ShipTypes.S_5] = 5
