from enum import Enum

class Settings:
    RoomSize = 2
    BoardSize = 15
    ShipRangeReveal = 1

class BoardDisplay(Enum):
    EMPTY = 0
    PLACED = 1
    SHIP_SHOT = 2
    MISS = 3
    USELESS = 4
    VALUABLE = 5

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

BotPlacingDefinitions = {
    0:{
        ShipTypes.S_1:[
            [1,  1, ShipOrientation.HORIZONTAL],
            [13, 13, ShipOrientation.HORIZONTAL],
            [13,  1,  ShipOrientation.HORIZONTAL],
            [1,  13,  ShipOrientation.HORIZONTAL]
        ],
        ShipTypes.S_2: [
            [ 3,3,   ShipOrientation.HORIZONTAL],
            [ 11, 7, ShipOrientation.VERTICAL],
            [ 7,12,  ShipOrientation.VERTICAL]
        ],
        ShipTypes.S_3: [
            [13, 7, ShipOrientation.HORIZONTAL],
            [3, 7, ShipOrientation.VERTICAL]
        ],
        ShipTypes.S_4: [
            [9,  6,  ShipOrientation.HORIZONTAL]
        ]
    }
}
ShipSizes = {ShipTypes.S_1: 1, ShipTypes.S_2: 2, ShipTypes.S_3: 3, ShipTypes.S_4: 4, ShipTypes.S_5: 5}
ShipCounts = {ShipTypes.S_1: 4, ShipTypes.S_2: 3, ShipTypes.S_3: 2, ShipTypes.S_4: 1, ShipTypes.S_5: 0}
BoardLetters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']



