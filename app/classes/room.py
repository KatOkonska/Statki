from app.classes.settings import *
class Room:
    InstanceCounter = 0

    def __init__(self):
        self.RoomId = Room.InstanceCounter
        self.RoomSize = Settings.RoomSize
        self.CurrentPlayers = []
        self.IsFree = True
        Room.InstanceCounter +=1

    def AddPlayer(self, newPlayer):
        if not self.IsFree:
            return
        self.CurrentPlayers.append(newPlayer)
        if len(self.CurrentPlayers) < self.RoomSize:
            self.IsFree = True
        else:
            self.IsFree = False

    def ClearRoom(self):
        self.CurrentPlayers.clear()
        self.IsFree = True

    def MarkEnemies(self):
        for PlayerA in self.CurrentPlayers:
            for PlayerB in self.CurrentPlayers:
                if PlayerA.Id != PlayerB.Id:
                    PlayerA.MarkEnemy(PlayerB)

    def IsGameRunning(self):
        readyPlayers = 0
        isRunning = False
        for player in self.CurrentPlayers:
            if player.IsReady():
                readyPlayers += 1
        print("readyPlayers " + str(readyPlayers))
        if readyPlayers == self.CurrentPlayers.__len__() and readyPlayers > 0:
            self.MarkEnemies()
            self.CurrentPlayers[0].HasTurn = True
            isRunning = True

        if (isRunning):
            for player in self.CurrentPlayers:
                player.RevealEnemyBoard()

        return isRunning

