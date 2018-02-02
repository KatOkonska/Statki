from app.classes.settings import *
class Room:
    InstanceCounter = 0

    def __init__(self):
        self.RoomId = Room.InstanceCounter
        self.RoomSize = Settings.RoomSize
        self.CurrentPlayers = []
        self.IsFree = True
        self.AndItIsGoodForYou = True
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

    def StartGame(self):
        for Player in self.CurrentPlayers:
            readyPlayers = 0
            if Player.IsReady:
                readyPlayers += 1
            if readyPlayers == len(self.CurrentPlayers):
                self.MarkEnemies(self)
                return "Game has begun."
            else:
                return "Not all players are ready!"
