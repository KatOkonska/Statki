from app.classes.settings import *

class Board:
    def __init__(self, Size):
        self.Size = Size
        self.Data = [[0 for x in range(self.Size)] for y in range(self.Size)]

    def DisplayShip(self, ship):
        if not ship.Placed:
            return

        if ship.Orientation == ShipOrientation.HORIZONTAL:
            for i in ship.Segments.__len__():
                if ship.Segments[i].IsHit:
                    self.Data[ship.StartingPosition.x + i][self.StartingPosition.y] = BoardDisplay.SHOT
                else:
                    self.Data[ship.StartingPosition.x + i][self.StartingPosition.y] = BoardDisplay.PLACED
        else:
            for i in ship.Segments.__len__():
                if ship.Segments[i].IsHit:
                    self.Data[ship.StartingPosition.x][self.StartingPosition.y+i] = BoardDisplay.SHOT
                else:
                    self.Data[ship.StartingPosition.x][self.StartingPosition.y+i] = BoardDisplay.PLACED

    def Clear(self):
        for x in range(0, len(self.Data)):
            for y in range(0, len(self.Data[x])):
                self.Data[x][y] = BoardDisplay.EMPTY