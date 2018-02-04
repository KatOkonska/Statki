from app.classes.settings import *
from app.classes.board import Board
from app.classes.ship import Ship
from app.classes.point import Point
import copy
from random import randint

class Player:
    InstanceCounter = 0
    Id = 0
    def __init__(self, Nick, IsBot = False):
        self.Id = Player.InstanceCounter
        self.Nick = Nick
        self.IsBot = IsBot
        self.HasTurn = False
        self.Enemy = None
        self.AvailableShips = [[Ship(0,0, shipType) for i in range(0, ShipCounts[shipType])]  for shipType in ShipTypes]
        self.BotShipIDs = []
        self.LastShipIndex = 0
        self.Board = Board(Settings.BoardSize)
        Player.InstanceCounter += 1
        if (self.IsBot):
            randVal = randint(0, BotPlacingDefinitions.__len__()-1)
            for shipType in ShipTypes:
                if shipType.value < self.AvailableShips.__len__():
                    for i in range(0, self.AvailableShips[shipType.value].__len__()):
                        placement = BotPlacingDefinitions[randVal][shipType][i]
                        self.TryPlaceShip(self.AvailableShips[shipType.value][i], placement[0], placement[1], placement[2])
                        self.BotShipIDs.append(self.AvailableShips[shipType.value][i].Id)

    def MarkEnemy(self, player):
        self.Enemy = player

    def IsReady(self):
        isReady = True
        log = ""
        for shipType in ShipTypes:
            if shipType.value < self.AvailableShips.__len__():
                for ship in self.AvailableShips[shipType.value]:
                    log += str(ship.Placed) + " "
                    if (ship.Placed == False):
                        isReady = False
        print("Player: " + self.Nick + " ready: " + str(isReady) + " ships " + log)
        return isReady

    def GetAvailableShipsIDs(self):
        outputArray = []
        for shipType in ShipTypes:
            if shipType.value < self.AvailableShips.__len__():
                for item in self.AvailableShips[shipType.value]:
                    itemDict = {"Id": -1, "X": -1, "Y": -1, "Size": -1, "Orientation": 0}
                    itemDict["Id"] = item.Id
                    itemDict["X"] = item.StartingPosition.x
                    itemDict["Y"] = item.StartingPosition.y
                    itemDict["Size"] = item.Size
                    itemDict["Orientation"] = item.Orientation
                    outputArray.append(itemDict)
        return outputArray

    def GetPlacedShipsIDs(self):
        outputArray = []
        for shipType in ShipTypes:
            if shipType.value < self.AvailableShips.__len__():
                for otherShip in self.AvailableShips[shipType.value]:
                    if (otherShip.Placed):
                        outputArray.append(otherShip.Id)
        return outputArray

    def TryPlaceShip(self, ship, x, y, orientation):
        if (self.CanPlaceShip(ship, x, y, orientation)):
            ship.Placed = True
            return True
        else:
            return False

    def CanPlaceShip(self, ship, x, y, orientation):
        if (ship.Placed == True):
            return False

        ship.MoveShip(x, y)
        if ship.Orientation != orientation:
            self.RotateShip(ship)

        if self.CollidesWithBoard(ship, self.Board):
            return False

        isOk = True

        for shipType in ShipTypes:
            if shipType.value < self.AvailableShips.__len__():
                for otherShip in self.AvailableShips[shipType.value]:
                    if (otherShip.Placed):
                        if isOk:
                            isOk = not self.CollidesWithShip(ship, otherShip)

        return isOk

    def CollidesWithShip(self, shipA, shipB):
        if (shipA.Placed == False or shipB.Placed == False):
            return  False
        rect1 = shipA.GetShipBoundingBox()
        rect2 = shipB.GetShipBoundingBox()
        if (rect1.x < rect2.x + rect2.width and
            rect1.x + rect1.width > rect2.x and
            rect1.y < rect2.y + rect2.height and
            rect1.height + rect1.y > rect2.y):
            return True;

    def CollidesWithBoard(self, ship, board):
        if ship.Orientation == ShipOrientation.HORIZONTAL.value:
            return ship.StartingPosition.x + ship.Size > board.Size and ship.StartingPosition.y > board.Size
        else:
            return ship.StartingPosition.y + ship.Size > board.Size and ship.StartingPosition.x > board.Size

    def RotateShip(self, ship):
        ship.RotateShip()

    def CreatePlayerBoard(self):
        return Board(Settings.BoardSize)

    def HasAnyShips(self):
        anyStanding = False
        for shipType in ShipTypes:
            if shipType.value < self.AvailableShips.__len__():
                for ship in self.AvailableShips[shipType.value]:
                    for segment in ship.Segments:
                        if (not segment.IsHit):
                            anyStanding = True
        return anyStanding

    def GetMyBoardDataDict(self):
        myBoard = copy.deepcopy(self.Board.GetData())
        for shipType in ShipTypes:
            if shipType.value < self.AvailableShips.__len__():
                for ship in self.AvailableShips[shipType.value]:
                    for segment in ship.Segments:
                        if (segment.IsHit):
                            myBoard[segment.Position.x][segment.Position.y] = BoardDisplay.SHIP_SHOT.value
                        else:
                            myBoard[segment.Position.x][segment.Position.y] = BoardDisplay.PLACED.value
        outputDict = {}
        for x in range(0, len(myBoard)):
            for y in range(0, len(myBoard[x])):
                key = BoardLetters[x] + str(y)
                outputDict.update({key: myBoard[x][y]})
        return outputDict

    def GetEnemyBoardData(self):
        return self.Enemy.Board.GetData()

    def GetEnemyBoardDataDict(self):
        enemyBoard = copy.deepcopy(self.GetEnemyBoardData())
        outputDict = {}
        for x in range(0, len(enemyBoard)):
            for y in range(0, len(enemyBoard[x])):
                key = BoardLetters[x] + str(y)
                outputDict.update({ key :enemyBoard[x][y] })
        return outputDict

    def RevealEnemyBoard(self):
        for ship in self.AvailableShips[ShipTypes.S_1.value]:
            self.RevealEnemyBoardByShip(ship.StartingPosition.x, ship.StartingPosition.y)

    def RevealEnemyBoardByShip(self, x, y):
        for rX in range(x - Settings.ShipRangeReveal, x + Settings.ShipRangeReveal+1):
            for rY in range(y - Settings.ShipRangeReveal, y + Settings.ShipRangeReveal+1):
                if (rX >= 0 and rX < Settings.BoardSize and rY >= 0 and rY < Settings.BoardSize):
                    self.Enemy.Board.Data[rX][rY] = BoardDisplay.UNKNOWN.value
                    for shipType in ShipTypes:
                        if shipType.value < self.Enemy.AvailableShips.__len__():
                            for ship in self.Enemy.AvailableShips[shipType.value]:
                                if (ship.Placed):
                                    print(str(ship.Segments.__len__()))
                                    for segment in ship.Segments:
                                        if segment.Position.x == rX and segment.Position.y == rY:
                                            self.Enemy.Board.Data[rX][rY] = BoardDisplay.PLACED.value

    def ShotEnemyWithShip(self, ship, x, y):
        hitCount = 0
        oldPos = Point(ship.StartingPosition.x, ship.StartingPosition.y)
        ship.MoveShip(x, y)
        for segment in ship.Segments:
            hitCount += self.ShotEnemyBoard(segment.Position.x, segment.Position.y)
        if hitCount <= 0:
            self.HasTurn = False
            self.Enemy.HasTurn = True
            ship.MoveShip(oldPos.x, oldPos.y)
            if (self.Enemy.IsBot):
                for shipType in ShipTypes:
                    if shipType.value < self.Enemy.AvailableShips.__len__():
                        for enemyShip in self.Enemy.AvailableShips[shipType.value]:
                            if (enemyShip.Id == self.Enemy.BotShipIDs[self.LastShipIndex]):
                                self.Enemy.BotShot(enemyShip)
        else:
            ship.MoveShip(oldPos.x, oldPos.y)

    def ShotEnemyBoard(self, x, y):
        print("ID: " + self.Nick + " ShotEnemyBoard: " + str(x) + " : " + str(y))
        hits = 0
        if (x < Settings.BoardSize and y < Settings.BoardSize):
            self.Enemy.Board.Data[x][y] = BoardDisplay.MISS.value
            for shipType in ShipTypes:
                if shipType.value < self.Enemy.AvailableShips.__len__():
                    for ship in self.Enemy.AvailableShips[shipType.value]:
                        if (ship.Placed):
                            for segment in ship.Segments:
                                print(str(ship.Id) + " x: "+ str(segment.Position.x) + " y: " +  str(segment.Position.y))
                                if segment.Position.x == x and segment.Position.y == y:
                                    if (not segment.IsHit):
                                        segment.IsHit = True
                                        hits += 1
                                    ''' Mark places around shot position '''
                                    if (x-1 >= 0 and y-1>=0):
                                        self.Enemy.Board.Data[x-1][y-1] = BoardDisplay.UNKNOWN.value
                                    if (x+1 < Settings.BoardSize and y+1<Settings.BoardSize):
                                        self.Enemy.Board.Data[x+1][y+1] = BoardDisplay.UNKNOWN.value
                                    if (x+1 < Settings.BoardSize and y - 1 >= 0):
                                        self.Enemy.Board.Data[x+1][y-1] = BoardDisplay.UNKNOWN.value
                                    if (x - 1 >= 0 and y+1<Settings.BoardSize):
                                        self.Enemy.Board.Data[x-1][y+1] = BoardDisplay.UNKNOWN.value
                                    if (x-1 >= 0):
                                        self.Enemy.Board.Data[x-1][y] = BoardDisplay.VALUABLE.value
                                    if (x+1 < Settings.BoardSize):
                                        self.Enemy.Board.Data[x+1][y] = BoardDisplay.VALUABLE.value
                                    if ( y - 1 >= 0):
                                        self.Enemy.Board.Data[x][y-1] = BoardDisplay.VALUABLE.value
                                    if (y+1<Settings.BoardSize):
                                        self.Enemy.Board.Data[x][y+1] = BoardDisplay.VALUABLE.value
                                    self.Enemy.Board.Data[x][y] = BoardDisplay.SHIP_SHOT.value
                            if (not ship.IsAlive()):
                                for segment in ship.Segments:
                                    ''' Mark places around segment position '''
                                    if (segment.Position.x-1 >=0 and segment.Position.y-1>=0):
                                        self.Enemy.Board.Data[segment.Position.x-1][segment.Position.y-1] = BoardDisplay.UNKNOWN.value
                                    if (segment.Position.x+1 < Settings.BoardSize and segment.Position.y+1<Settings.BoardSize):
                                        self.Enemy.Board.Data[segment.Position.x+1][segment.Position.y+1] = BoardDisplay.UNKNOWN.value
                                    if (segment.Position.x+1 < Settings.BoardSize and segment.Position.y - 1 >= 0):
                                        self.Enemy.Board.Data[segment.Position.x+1][segment.Position.y-1] = BoardDisplay.UNKNOWN.value
                                    if (segment.Position.x - 1 >= 0 and segment.Position.y+1<Settings.BoardSize):
                                        self.Enemy.Board.Data[segment.Position.x-1][segment.Position.y+1] = BoardDisplay.UNKNOWN.value
                                    if (segment.Position.x-1 >= 0):
                                        self.Enemy.Board.Data[segment.Position.x-1][segment.Position.y] = BoardDisplay.UNKNOWN.value
                                    if (segment.Position.x+1 < Settings.BoardSize):
                                        self.Enemy.Board.Data[segment.Position.x+1][segment.Position.y] = BoardDisplay.UNKNOWN.value
                                    if (segment.Position.y - 1 >= 0):
                                        self.Enemy.Board.Data[segment.Position.x][segment.Position.y-1] = BoardDisplay.UNKNOWN.value
                                    if (segment.Position.y+1<Settings.BoardSize):
                                        self.Enemy.Board.Data[segment.Position.x][segment.Position.y+1] = BoardDisplay.UNKNOWN.value
                                for segment in ship.Segments:
                                    self.Enemy.Board.Data[segment.Position.x][segment.Position.y] = BoardDisplay.SHIP_SHOT.value

        return hits

    def BotShot(self, ship):
        print(self.Nick)
        shotPosition = self.GetMostValuableShotPosition(ship)
        self.ShotEnemyWithShip(ship, shotPosition.x, shotPosition.y)
        if self.HasTurn:
            self.LastShipIndex += 1
            if (self.LastShipIndex > self.BotShipIDs.__len__() - 1):
                self.LastShipIndex = 0

            ''' Get next ship and shot with it. '''
            for shipType in ShipTypes:
                if shipType.value < self.AvailableShips.__len__():
                    for ship in self.AvailableShips[shipType.value]:
                        if (ship.Id == self.BotShipIDs[self.LastShipIndex]):
                            self.BotShot(ship)

    def GetMostValuableShotPosition(self, ship):
        print("BotShot " + str(ship.StartingPosition.x) + " " + str(ship.StartingPosition.y))
        position = Point(0,0)
        value = 0
        for y in range(0, Settings.BoardSize):
            for x in range(0, Settings.BoardSize):
                print("BotShot BoardDisplay.PLACED.value X: " + str(x) + " Y: " + str(y))
                if (self.Enemy.Board.Data[x][y] == BoardDisplay.PLACED.value):
                    print("BotShot BoardDisplay.PLACED.value" + str(x) + " " + str(y))
                    position.x = x
                    position.y = y
                    return position
                elif (self.Enemy.Board.Data[x][y] == BoardDisplay.VALUABLE.value):
                    print("BotShot BoardDisplay.VALUABLE.value" + str(x) + " " +  str(y))
                    position.x = x
                    position.y = y
                    value = Settings.BoardSize+1
                elif (self.Enemy.Board.Data[x][y] == BoardDisplay.EMPTY.value):
                    newValue = 0
                    oldPos = Point(ship.StartingPosition.x, ship.StartingPosition.y)
                    ship.MoveShip(x, y)
                    for segment in ship.Segments:
                        if (segment.Position.x >= 0 and segment.Position.x < Settings.BoardSize and segment.Position.y >= 0 and  segment.Position.y < Settings.BoardSize):
                            if (self.Enemy.Board.Data[segment.Position.x][segment.Position.y] == BoardDisplay.EMPTY.value):
                                newValue += 1
                    if newValue > value:
                        value = newValue
                        position.x = x
                        position.y = y
                        print("BotShot BoardDisplay.EMPTY.value" + str(y) + " " +  str(x))
                    ship.MoveShip(oldPos.x, oldPos.y)
        return position
