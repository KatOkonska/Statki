from app.classes.settings import *
from app.classes.segment import Segment
from app.classes.point import Point

class Ship:
    InstanceCounter = 0
    Id = 0
    def __init__(self, x, y, shipType):
        self.Id = Ship.InstanceCounter
        self.Orientation = ShipOrientation.HORIZONTAL.value
        self.Type = shipType
        self.Size = ShipSizes[self.Type]
        self.IsAlive = True
        self.Placed = False
        self.StartingPosition = Point(x,y)
        self.Segments = None
        if self.Orientation == ShipOrientation.HORIZONTAL.value:
            self.Segments = [Segment(self.StartingPosition.x + i, self.StartingPosition.y) for i in range(0, self.Size)]
        else:
            self.Segments = [Segment(self.StartingPosition.x, self.StartingPosition.y + i) for i in range(0, self.Size)]
        Ship.InstanceCounter += 1

    def GetShipBoundingBox(self):
        boundingBox = {"x": 0, "y":0, "width":0, "height":0}
        if (self.ShipOrientation == ShipOrientation.HORIZONTAL.value):
            boundingBox["x"] =  self.StartingPosition.x - 1
            boundingBox["y"] =  self.StartingPosition.y - 1
            boundingBox["width"] =  self.Size + 2
            boundingBox["height"] = 3
            return boundingBox
        else:
            boundingBox["x"] =  self.StartingPosition.x - 1
            boundingBox["y"] =  self.StartingPosition.y - 1
            boundingBox["width"] = 3
            boundingBox["height"] = self.Size + 2
            return  boundingBox
        return None

    def MoveShip(self, x, y):
        self.StartingPosition.x = x
        self.StartingPosition.y = y
        if self.Orientation == ShipOrientation.HORIZONTAL.value:
            for i in range(0,self.Segments.__len__()):
                self.Segments[i].Position.x  = self.StartingPosition.x + i
                self.Segments[i].Position.y = self.StartingPosition.y
        else:
            for i in range(0,self.Segments.__len__()):
                self.Segments[i].Position.x  = self.StartingPosition.x
                self.Segments[i].Position.y = self.StartingPosition.y + i

    def RotateShip(self):
        if self.Orientation == ShipOrientation.HORIZONTAL.value:
            self.Orientation = ShipOrientation.VERTICAL.value
            for i in range(0,self.Segments.__len__()):
                self.Segments[i].Position.x  = self.StartingPosition.x
                self.Segments[i].Position.y = self.StartingPosition.y + i
        else:
            self.Orientation = ShipOrientation.HORIZONTAL
            for i in range(0,self.Segments.__len__()):
                self.Segments[i].Position.x  = self.StartingPosition.x + i
                self.Segments[i].Position.y = self.StartingPosition.y