from app.classes.settings import *
from app.classes.segment import Segment
from app.classes.point import Point

class Ship:

    def __init__(self, x, y, shipType):
        self.Orientation = ShipOrientation.HORIZONTAL
        self.Type = shipType
        self.Size = ShipSizes[self.Type]
        self.IsAlive = True
        self.Placed = False
        self.StartingPosition = Point(x,y)
        if self.Orientation == ShipOrientation.HORIZONTAL:
            self.Segments = [Segment(self.StartingPosition.x + i, self.StartingPosition.y) for i in range(self.Size)]
        else:
            self.Segments = [Segment(self.StartingPosition.x, self.StartingPosition.y + i) for i in range(self.Size)]

    def MoveShip(self, x, y):
        self.StartingPosition.x = x
        self.StartingPosition.y = y
        if self.Orientation == ShipOrientation.HORIZONTAL:
            for i in self.Segments.__len__():
                self.Segments[i].Position(self.StartingPosition.x+i, self.StartingPosition.y)
        else:
            for i in self.Segments.__len__():
                self.Segments[i].Position(self.StartingPosition.x, self.StartingPosition.y + i)

    def RotateShip(self):
        if self.Orientation == ShipOrientation.HORIZONTAL:
            self.Orientation = ShipOrientation.VERTICAL
            for i in self.Segments.__len__():
                self.Segments[i].Position(self.StartingPosition.x, self.StartingPosition.y + i)
        else:
            self.Orientation = ShipOrientation.HORIZONTAL
            for i in self.Segments.__len__():
                self.Segments[i].Position(self.StartingPosition.x+i, self.StartingPosition.y)