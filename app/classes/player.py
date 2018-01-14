from app.classes.settings import Settings
from app.classes.board import Board

class Player:
    InstanceCounter = 0

    def __init__(self, Nick):
        self.Id = self.InstanceCounter
        self.Nick = Nick
        self.HasTurn = False
        self.Enemy = None
        self.AvailableShips = []
        self.PlacedShips = []
        self.Board = Board(Settings.BoardSize)
        self.InstanceCounter += 1

    def PlaceShip(self, ship, x, y):
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
                if (segment.Position.x == x and segment.Position.y == y):
                    segment.IsHit = True
        self.Enemy.UpdatePlayerBoard()