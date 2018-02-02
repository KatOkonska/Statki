from app.classes.settings import *
from app.classes.board import Board
from app.classes.ship import Ship
from app.classes.point import Point

class Player:
    InstanceCounter = 0
    Id = 0
    def __init__(self, Nick):
        self.Id = self.InstanceCounter
        self.Nick = Nick
        self.HasTurn = False
        self.Enemy = None
        self.AvailableShips = [[Ship(0,0, shipType) for i in ShipCounts]  for shipType in ShipTypes]
        self.PlacedShips = []
        self.Board = Board(Settings.BoardSize)
        self.InstanceCounter += 1

    def CanPlaceShip(self, ship, x, y):
        if (self.CollidesWithBoard(ship, self.Board)):
            return False

        isOk = True

        for otherShip in self.PlacedShips:
            if isOk:
                isOk = self.CollidesWithShip(ship, otherShip)

        return isOk

    def CollidesWithShip(self, shipA, shipB):
        pass
        pointsA = []
        if shipA.Orientation == ShipOrientation.HORIZONTAL:
            pointsA = [Point(shipA.StartingPosition.x + i, shipA.StartingPosition.y) for i in range(shipA.Size)]
        else:
            pointsA = [Point(shipA.StartingPosition.x, shipA.StartingPosition.y + i) for i in range(shipA.Size)]


    def CollidesWithBoard(self, ship, board):
        if ship.Orientation == ShipOrientation.HORIZONTAL:
            return ship.StartingPosition.x + ship.Size < board.Size and ship.StartingPosition.y < board.Size
        else:
            return ship.StartingPosition.y + ship.Size < board.Size and ship.StartingPosition.x < board.Size

    def PlaceShip(self, ship, x, y):
        ship.Placed = True;
        ship.MoveShip(x,y)

    def RotateShip(self, ship):
        ship.RotateShip()

    def SetEnemy(self, Enemy):
        self.Enemy = Enemy

    def CreatePlayerBoard(self):
        return Board(Settings.BoardSize)

    def UpdatePlayerBoard(self):
        for Ship in self.PlacedShips:
            self.Board.DisplayShip(Ship)

    def ShotEnemyShips(self, x, y):
        for ship in self.Enemy.PlacedShips:
            for segment in ship.Segments:
                if segment.Position.x == x and segment.Position.y == y:
                    segment.IsHit = True
        self.Enemy.UpdatePlayerBoard()