from flask import render_template, request, redirect, Response

import string
import random
import json

from app import app

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
    randomName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    newPlayer = Player(randomName)

    ''' Get room number from GET request '''
    roomNumber = request.args.get('roomNumber', default=-1, type=int)
    user = {'name': randomName}

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

@app.route('/gameManager',methods = ['POST'])
def gameManager():
    if request.method == 'POST':
        print("Data recieved: ", request.get_json())
        requestData = request.get_json()
        for key, value in requestData.items():
            print(key," ", value)
        responseData = {'kaczka': 'kwa kwa', 'pies': 'hau hau'}
        return json.dumps(responseData)
        #return request.data
    else:
        return ("Bad method")

def event_stream(data):
    print(data)
    output =  'event: message' + '\n'
    output += 'data: ' + data + '\n'
    output += '\n'
    yield output

@app.route("/playerJoinedRoom")
def stream():
    roomNumber = request.args.get('roomNumber', default=-1, type=int)
    print(roomNumber)
    if roomNumber < 0:
        return Response(event_stream("NONE"), mimetype="text/event-stream")

    outPlayerList = []
    i = 0
    for player in CurrentRooms[roomNumber].CurrentPlayers:
        outPlayerList.append(player.Nick)
        i+=1
    print(isinstance(outPlayerList, list))
    return Response(event_stream(json.dumps(list(outPlayerList), ensure_ascii = False)), mimetype="text/event-stream")
