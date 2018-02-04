from flask import render_template, request, redirect, Response

import string
import random
import json

from app import app

from app.classes.settings import *
from app.classes.room import Room
from app.classes.player import Player

CurrentRooms = []

def InitializeNewRoom():
    newRoom = Room()
    CurrentRooms.append(newRoom)
    return newRoom.RoomId

@app.route('/')
@app.route('/index')
def index():
    opponent = {'name': 'Adolf'}

    ''' Create new player '''
    randomName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        #''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    newPlayer = Player(randomName)

    ''' Get room number from GET request '''
    roomNumber = request.args.get('roomNumber', default=-1, type=int)
    user = {'name': randomName}

    ''' Get game mode from GET request '''
    botEnabled = request.args.get('botEnabled', default=0, type=int)

    ''' Check for if bot was requested '''
    if botEnabled > 0:
        ''' Create new bot '''
        botName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        newBot = Player("Bot_"+botName, True)
        opponent["name"] = "Bot_" + newBot.Nick
        roomIndex = InitializeNewRoom()
        CurrentRooms[roomIndex].AddPlayer(newPlayer)
        CurrentRooms[roomIndex].AddPlayer(newBot)
        roomData = {'roomNumber': CurrentRooms[roomIndex].RoomId}
        return render_template('index.html', user=user, opponent=opponent, roomData=roomData)

    ''' Try to place player in desired room '''
    if roomNumber >= 0 < len(CurrentRooms):
        CurrentRooms[roomNumber].AddPlayer(newPlayer)
        roomData = {'roomNumber': CurrentRooms[roomNumber].RoomId}
        return render_template('index.html', user=user, opponent=opponent, roomData=roomData)

    ''' Try to place player in any free room then '''
    for room in CurrentRooms:
        if room.IsFree:
            roomData = {'roomNumber': room.RoomId}
            room.AddPlayer(newPlayer)
            return render_template('index.html', user=user, opponent=opponent, roomData=roomData)

    ''' Placing was impossible, create new room and add first player to that room '''
    roomIndex = InitializeNewRoom()
    CurrentRooms[roomIndex].AddPlayer(newPlayer)
    roomData = {'roomNumber':    CurrentRooms[roomIndex].RoomId}
    return render_template('index.html', user=user, opponent= opponent, roomData=roomData)

@app.route('/shipPlacing',methods = ['POST'])
def shipPlacing():
    pass
    if request.method == 'POST':
        print("Data recieved: ", request.get_json())
        requestData = request.get_json()
        for key, value in requestData.items():
            print(key," ", value)
        responseData = {'kaczka': 'kwa kwa', 'pies': 'hau hau'}
        return json.dumps(responseData)
    else:
        return ("Bad method")


@app.route('/gameManager',methods = ['POST'])
def gameManager():
    if request.method == 'POST':
        requestData = request.get_json()
        responseData = {'kaczka': 'kwa kwa', 'pies': 'hau hau'}
        return json.dumps(responseData)
    else:
        return ("Bad method")

@app.route('/getPlayerData',methods = ['POST'])
def getPlayerData():
    playerNick = ""
    roomNumber = -1
    if request.method == 'POST':
        requestData = request.get_json()

        for key, value in requestData.items():
            if key == "roomNumber":
                roomNumber = int(value)
            if key == "playerNick":
                playerNick = value

        for player in CurrentRooms[roomNumber].CurrentPlayers:
            if player.Nick == playerNick:
                responseData = {
                        'Nick': player.Nick,
                        'HasTurn': player.HasTurn,
                        'AvailableShips': player.GetAvailableShipsIDs(),
                        'PlacedShips': player.GetPlacedShipsIDs()
                    }

                return json.dumps(responseData)
        return ("Room doesn't contain player with nick: " + str(playerNick))
    else:
        return ("Wrong request method - POST required, got: " + str(request.method))


@app.route('/shotEnemy',methods = ['POST'])
def shotEnemy():
    playerNick = ""
    roomNumber = -1
    shipId = -1
    x = -1
    y = -1
    if request.method == 'POST':
        requestData = request.get_json()

        for key, value in requestData.items():
            if key == "roomNumber":
                roomNumber = int(value)
            if key == "playerNick":
                playerNick = value
            if key == "shipId":
                shipId = value
            if key == "x":
                x = value
            if key == "y":
                y = value

        for player in CurrentRooms[roomNumber].CurrentPlayers:
            if player.Nick == playerNick:
                for shipType in ShipTypes:
                    for ship in player.AvailableShips[shipType.value]:
                        if (ship.Id == shipId):
                            player.ShotEnemyWithShip(ship, x, y)
                            responseData = {
                                'Data': json.dumps(player.GetEnemyBoardDataDict())
                            }
                            return json.dumps(responseData)
                return ("Player doesn't contain ship with id: " + str(shipId))
        return ("Room doesn't contain player with nick: " + str(playerNick))
    else:
        return ("Wrong request method - POST required, got: " + str(request.method))


@app.route('/placeShipOnBoard',methods = ['POST'])
def placeShipOnBoard():
    playerNick = ""
    roomNumber = -1
    shipId= -1
    x= -1
    y= -1,
    orientation = -1
    if request.method == 'POST':
        requestData = request.get_json()

        for key, value in requestData.items():
            if key == "roomNumber":
                roomNumber = int(value)
            if key == "playerNick":
                playerNick = value
            if key == "shipId":
                shipId = value
            if key == "x":
                x = value
            if key == "y":
                y = value
            if key == "orientation":
                orientation = value

        for player in CurrentRooms[roomNumber].CurrentPlayers:
            if player.Nick == playerNick:
                for shipType in ShipTypes:
                    for ship in player.AvailableShips[shipType.value]:
                        if (ship.Id == shipId):
                            placed = player.TryPlaceShip(ship, x, y, orientation)
                            isReady = player.IsReady()
                            gameStarted = CurrentRooms[roomNumber].IsGameRunning()
                            responseData = {
                                'Placed':placed ,
                                'IsReady' : isReady,
                                'GameStarted' : gameStarted
                            }
                            return json.dumps(responseData)
                return ("Player doesn't contain ship with id: " + str(shipId))
        return ("Room doesn't contain player with nick: " + str(playerNick))
    else:
        return ("Wrong request method - POST required, got: " + str(request.method))

@app.route('/getPlayerBoard',methods = ['POST'])
def getPlayerBoard():
    playerNick = ""
    roomNumber = -1

    if request.method == 'POST':
        requestData = request.get_json()

        for key, value in requestData.items():
            if key == "roomNumber":
                roomNumber = int(value)
            if key == "playerNick":
                playerNick = value

        for player in CurrentRooms[roomNumber].CurrentPlayers:
            if player.Nick == playerNick:
                responseData = {
                    'Data': json.dumps(player.GetMyBoardDataDict())
                }
                return json.dumps(responseData)
        return ("Room doesn't contain player with nick: " + str(playerNick))
    else:
        return ("Wrong request method - POST required, got: " + str(request.method))

@app.route('/getEnemyBoard',methods = ['POST'])
def getEnemyBoard():
    playerNick = ""
    roomNumber = -1

    if request.method == 'POST':
        requestData = request.get_json()

        for key, value in requestData.items():
            if key == "roomNumber":
                roomNumber = int(value)
            if key == "playerNick":
                playerNick = value

        for player in CurrentRooms[roomNumber].CurrentPlayers:
            if player.Nick == playerNick:
                responseData = {
                    'Data': json.dumps(player.GetEnemyBoardDataDict())
                }
                return json.dumps(responseData)
        return ("Room doesn't contain player with nick: " + str(playerNick))
    else:
        return ("Wrong request method - POST required, got: " + str(request.method))


def playerJoinedRoomStreamGenerator(data):
    print(data)
    output =  'retry: 1000' + '\n'
    output += 'event: message' + '\n'
    output += 'data: ' + data + '\n'
    output += '\n'
    yield output

@app.route("/playerJoinedRoom")
def playerJoinedRoomStream():
    roomNumber = request.args.get('roomNumber', default=-1, type=int)
    if roomNumber < 0:
        return Response(playerJoinedRoomStreamGenerator("NONE"), mimetype="text/event-stream")
    outPlayerList = []
    i = 0
    for player in CurrentRooms[roomNumber].CurrentPlayers:
        outPlayerList.append(player.Nick)
        i+=1
    return Response(playerJoinedRoomStreamGenerator(json.dumps(list(outPlayerList), ensure_ascii = False)), mimetype="text/event-stream")


def turnHasChangedStreamGenerator(data):
    output =  'retry: 1000' + '\n'
    output += 'event: message' + '\n'
    output += 'data: ' + data + '\n'
    output += '\n'
    yield output

@app.route("/turnHasChanged")
def turnHasChangedStream():
    roomNumber = request.args.get('roomNumber', default=-1, type=int)
    playerNick = request.args.get('playerNick', default="", type=str)

    outputData = { "IsPlayerTurn" : False, "HasGameEnded" : False, "Winner": ""}
    for player in CurrentRooms[roomNumber].CurrentPlayers:
        if (player.Nick == playerNick):
            outputData["IsPlayerTurn"] = player.HasTurn
            outputData["HasGameEnded"] = (not player.HasAnyShips()) or not (player.Enemy.HasAnyShips())
            if ((not player.HasAnyShips()) and (player.Enemy.HasAnyShips())):
                outputData["Winner"] = player.Enemy.Nick
            elif(( player.HasAnyShips()) and (not player.Enemy.HasAnyShips())):
                outputData["Winner"] = player.Nick

    return Response(turnHasChangedStreamGenerator(json.dumps(outputData, ensure_ascii = False)), mimetype="text/event-stream")


def hasGameStartedStreamGenerator(data):
    output =  'retry: 1000' + '\n'
    output += 'event: message' + '\n'
    output += 'data: ' + data + '\n'
    output += '\n'
    yield output

@app.route("/hasGameStarted")
def hasGameStartedStream():
    roomNumber = request.args.get('roomNumber', default=-1, type=int)
    outputData = { "HasGameStarted" :  CurrentRooms[roomNumber].IsGameRunning() }
    return Response(hasGameStartedStreamGenerator(json.dumps(outputData, ensure_ascii = False)), mimetype="text/event-stream")

