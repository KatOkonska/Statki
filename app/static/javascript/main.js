// Client-side Javascript in the HTML
var roomNumber = -1;
var playerJoinedRoomSource;

var playerNick = ""
var enemyNick = ""

function createSource_playerJoinedRoom() {
    console.log("createSource_playerJoinedRoom");
    playerJoinedRoomSource = new EventSource("/playerJoinedRoom?" + "roomNumber=" + roomNumber);

    playerJoinedRoomSource.onopen = function() {
        //alert('connection is opened.'+playerJoinedRoomSource.readyState);
    };

    playerJoinedRoomSource.onerror = function() {
        //alert('error: '+playerJoinedRoomSource.readyState);
    };

    playerJoinedRoomSource.onmessage = function(e) {
        currentPlayers = JSON.parse(e.data)
        if (currentPlayers.length > 1) {
            if (enemyNick == "") {
                var index = currentPlayers.indexOf(playerNick);
                if (index > -1) {
                    currentPlayers.splice(index, 1);
                    enemyNick = currentPlayers[0];
                    $("#room").find("#opponentSection").find("#opponentName").text("Hello, " + enemyNick + " !");
                    window.confirm("Player: " + enemyNick + " has joined the room.");
                }
            }
        }
    };
}

function setRoomNumber(number) {
    console.log("setRoomNumber");
    roomNumber = number
}

function setPlayerName(name) {
    console.log("setPlayerName");
    playerNick = name
}


window.onload = function() {

    setRoomNumber('{{roomData['
        roomNumber ']}}');

    setPlayerName('{{user['

        name ']}}')
    createSource_playerJoinedRoom();

}

var boardLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
var currentShipSize = 0;
var currentShipRotation = 0; // 0 = - and 1 = |
var currentShipCanBePlaced = false;
var placedShips = []; // empty array

var htmlData = {
    "gameMode": "singlePlayer",

    "roomNumber": "8"
}

function onGameStartSuccess(responseData) {
    console.log("Data recieved from server: " + responseData);
};

function askServer_placeShip(playerID, x, y, size, rotation) {
    var htmlData = {
        "gameMode": "singlePlayer",

        "roomNumber": "8"
    }
}

function askServer_shotEnemy(playerID, x, y, size, rotation) {
    var htmlData = {
        "gameMode": "singlePlayer",

        "roomNumber": "8"
    }
}

function askServer_getMyBoard(playerID) {
    var htmlData = {
        "gameMode": "singlePlayer",

        "roomNumber": "8"
    }
}

function askServer_getEnemyBoard(playerID) {
    var htmlData = {
        "gameMode": "singlePlayer",

        "roomNumber": "8"
    }
}

function startGame() {
    console.log("Data sent to server: " + JSON.stringify(htmlData));

    $.ajax({
        type: 'POST',
        url: 'gameManager',
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify(htmlData),
        success: function(data) {
            onGameStartSuccess(data);
        }
    });
};

function changeColor(x, y, color) {
    console.log("Data recieved from server: " + x + " " + y + " " + color);
    $("#room").find("#opponentSection").find("#board").find("#" + boardLetters[parseInt(x) + parseInt(y)]).css('background-color', 'yellow');
}

function clearTilesSelection() {
    for (y = 0; y < 15; y++) {
        for (x = 0; x < 15; x++) {
            $("#room").find("#playerSection").find("#board").find("#" + boardLetters[x] + y).css('background-color', 'white');
        }
    }
}

function redrawPlacedShips() {
    placedShips.forEach(highlightPlacedShip)
}

function highlightPlacedShip(item, index) {
    if (parseInt(item["rotation"]) == 0) {
        for (i = 0; i < parseInt(item["size"]); i++) {
            $("#room").find("#playerSection").find("#board").find("#" + boardLetters[parseInt(item["posX"]) + parseInt(i)] + item["posY"]).css('background-color', 'green');
        }
    } else {
        for (i = 0; i < parseInt(item["size"]); i++) {
            $("#room").find("#playerSection").find("#board").find("#" + boardLetters[parseInt(item["posX"])] + (parseInt(item["posY"]) + i)).css('background-color', 'green');
        }
    }
}

function setCurrentShipSize(size) {
    currentShipSize = size;
}

function placeCurrentShip(x, y) {
    if (currentShipCanBePlaced) {
        placedShips.push({
            posX: x,
            posY: y,
            size: currentShipSize,
            rotation: currentShipRotation
        });
        currentShipSize = 0;
        currentShipCanBePlaced = false;
    }
}

function checkBoundingBoxCollision(rect1, rect2) {
    if (rect1.x < rect2.x + rect2.width && rect1.x + rect1.width > rect2.x && rect1.y < rect2.y + rect2.height && rect1.height + rect1.y > rect2.y) {
        return true;
    }
}

function shotEnemyPosition(x, y) {
    console.log("Bum bum X: " + parseInt(x) + " Y: " + parseInt(y));
}

function tryPlaceCurrentShip(x, y) {
    if (currentShipSize <= 0) {
        return;
    }

    clearTilesSelection();
    redrawPlacedShips();

    if (currentShipRotation == 0) {
        currentShipCanBePlaced = true;
        // Check against the board borders.
        if (parseInt(x) + currentShipSize < 15 + 1) {
            // Then against other ships.
            for (var i = 0, len = placedShips.length; i < len; i++) {
                var rect1 = {
                    x: parseInt(x),
                    y: parseInt(y),
                    width: currentShipSize,
                    height: 1
                };;
                var rect2;

                if (parseInt(placedShips[i]["rotation"]) == 0) {
                    rect2 = {
                        x: parseInt(placedShips[i]["posX"]) - 1,
                        y: parseInt(placedShips[i]["posY"]) - 1,
                        width: parseInt(placedShips[i]["size"]) + 2,
                        height: 3
                    };
                } else {
                    rect2 = {
                        x: parseInt(placedShips[i]["posX"]) - 1,
                        y: parseInt(placedShips[i]["posY"]) - 1,
                        width: 3,
                        height: parseInt(placedShips[i]["size"]) + 2
                    };
                }
                if (checkBoundingBoxCollision(rect1, rect2)) {
                    currentShipCanBePlaced = false;
                }
            }
        } else {
            currentShipCanBePlaced = false;
        }

        if (currentShipCanBePlaced) {
            for (i = 0; i < currentShipSize; i++) {
                $("#room").find("#playerSection").find("#board").find("#" + boardLetters[parseInt(x) + parseInt(i)] + y).css('background-color', 'green');
            }
        } else {
            for (i = 0; i < currentShipSize; i++) {
                if (i < (15 - x)) {
                    $("#room").find("#playerSection").find("#board").find("#" + boardLetters[parseInt(x) + parseInt(i)] + y).css('background-color', 'red');
                }
            }
        }
    } else {
        // Check against the board borders.
        if (parseInt(y) + currentShipSize < 15 + 1) {
            for (i = 0; i < currentShipSize; i++) {
                $("#room").find("#playerSection").find("#board").find("#" + boardLetters[parseInt(x)] + (parseInt(y) + i)).css('background-color', 'green');
            }
            currentShipCanBePlaced = true;
        } else {
            for (i = 0; i < (15 - y); i++) {
                $("#room").find("#playerSection").find("#board").find("#" + boardLetters[parseInt(x)] + (parseInt(y) + i)).css('background-color', 'red');
            }
            currentShipCanBePlaced = false;
        }
    }
}