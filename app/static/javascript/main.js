// Client-side Javascript in the HTML
var roomNumber = -1;

var playerJoinedRoomSource = null;
var hasGameStartedSource = null;
var turnStatusSource = null;

var player;
var playerNick = ""

var currentShipSize = 0;
var currentShipRotation = 0; // 0 = - and 1 = |
var currentShipCanBePlaced = false;

var isPlayerTurn = false;
var currentlyShootingShipIndex = 0;
var currentlyShootingShip;

var enemyNick = ""

var boardLetters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']

var currentEnemyBoard = null
var lastMarkedX = -1;
var lastMarkedY = -1;
function hideElementByReference(element)
{
    element.style.display = 'none'; //or
    element.style.visibility = 'hidden';
}

function createSource_playerJoinedRoom()
{
    if (playerJoinedRoomSource != null){
        return;
    }

    console.log("createSource_playerJoinedRoom");
    playerJoinedRoomSource = new EventSource("/playerJoinedRoom?"+"roomNumber="+roomNumber);

    playerJoinedRoomSource.onopen = function(){
        //alert('connection is opened.'+playerJoinedRoomSource.readyState);
    };

    playerJoinedRoomSource.onerror = function(){
        //alert('error: '+playerJoinedRoomSource.readyState);
    };

    playerJoinedRoomSource.onmessage = function(e)
     {
        currentPlayers = JSON.parse(e.data)
        if (currentPlayers.length > 1)
        {
            if (enemyNick == "")
            {
                var index = currentPlayers.indexOf(playerNick);
                if (index > -1) {
                    currentPlayers.splice(index, 1);
                    enemyNick = currentPlayers[0];
                    $("#gameRoom").find("#opponentSection").find("#usernameSection").find("#username").text("Twój przeciwnik to: " + enemyNick + " !");
                    window.confirm("Player: " + enemyNick + " has joined the room.");
                    playerJoinedRoomSource.close();
                    createSource_hasGameStarted();
                }
            }
        }
    };
}


function createSource_hasGameStarted()
{
    if (hasGameStartedSource != null){
        return;
    }

    console.log("createSource_hasGameStarted");
    hasGameStartedSource = new EventSource("/hasGameStarted?"+"roomNumber="+roomNumber);

    hasGameStartedSource.onopen = function(){
        //alert('connection is opened.'+playerJoinedRoomSource.readyState);
    };

    hasGameStartedSource.onerror = function(){
        //alert('error: '+playerJoinedRoomSource.readyState);
    };

    hasGameStartedSource.onmessage = function(e)
     {
        gameStatus = JSON.parse(e.data)

        if (gameStatus.HasGameStarted)
        {
            hasGameStartedSource.close();
            StartGame();
        }
    };
}

function createSource_turnStatus()
{
    if (turnStatusSource != null){
        return;
    }

    console.log("createSource_turnStatus");
    turnStatusSource = new EventSource("/turnHasChanged?"+"roomNumber="+roomNumber+"&playerNick="+playerNick);

    turnStatusSource.onopen = function(){
        //alert('connection is opened.'+playerJoinedRoomSource.readyState);
    };

    turnStatusSource.onerror = function(){
        //alert('error: '+playerJoinedRoomSource.readyState);
    };

    turnStatusSource.onmessage = function(e)
     {
        turnStatus = JSON.parse(e.data)
        if (turnStatus.HasGameEnded === true)
        {
            window.confirm("Game won by: " + turnStatus.Winner);
            askServer_getEnemyBoard();
            askServer_getMyBoard();
            playerJoinedRoomSource.close();
            hasGameStartedSource.close();
            turnStatusSource.close();
            return
        }

        askServer_getMyBoard();
        askServer_getEnemyBoard();

        if (turnStatus.IsPlayerTurn && !isPlayerTurn)
        {
            isPlayerTurn = turnStatus.IsPlayerTurn;
            if (currentlyShootingShipIndex > player.PlacedShips.length - 1)
            {
                currentlyShootingShipIndex = 0;
            }
            console.log(currentlyShootingShipIndex);
            console.log(player.PlacedShips[currentlyShootingShipIndex]);
            currentlyShootingShip = player.PlacedShips[currentlyShootingShipIndex];
            console.log(currentlyShootingShip.Size);
            askServer_getMyBoard();
            askServer_getEnemyBoard();

            window.confirm("Your move!");

            $('html, body').animate({
                scrollTop: $("#gameRoom").find("#opponentSection").find("#gameSection").find("#boardSection").offset().top
            }, 500);
        }
        else if (!turnStatus.IsPlayerTurn)
        {

            isPlayerTurn = false;
            $('html, body').animate({
                scrollTop: $("#gameRoom").find("#playerSection").find("#gameSection").find("#boardSection").find("#board").offset().top
            }, 500);
        }
    };
}

function setRoomNumber(number)
{
    console.log("setRoomNumber");
    roomNumber = number
}

function setPlayerName(name)
{
    console.log("setPlayerName");
    playerNick = name
}

function onGameStartSuccess(responseData)
{
    console.log("Data recieved from server: " + responseData);
};

function askServer_GetPlayerData()
{
   var htmlData =
    {
        "playerNick": playerNick,
        "roomNumber": roomNumber
    }

    console.log("Data sent to server: " + JSON.stringify(htmlData));

    $.ajax
    (
        {
            type : 'POST',
            url: 'getPlayerData',
            headers:
            {
                "Content-Type":"application/json"
            },
            data: JSON.stringify(htmlData),
            success: function(data)
            {
                onGetPlayerDataSuccess(data);
            }
        }
    );
}

function onGetPlayerDataSuccess(responseData)
{
    console.log("Data recieved from server: " + responseData);
    player = JSON.parse(responseData);
    console.log("Parsed player: " + player);
};

function askServer_placeShip(ship)
{

    var htmlData =
    {
        "playerNick": playerNick,
        "roomNumber": roomNumber,
        "shipId": ship.Id,
        "x":ship.X,
        "y":ship.Y,
        "orientation":ship.Orientation
    }

    $.ajax
    (
        {
            type : 'POST',
            url: 'placeShipOnBoard',
            headers:
            {
                "Content-Type":"application/json"
            },
            data: JSON.stringify(htmlData),
            success: function(data)
            {
                onPlaceShipOnBoardSuccess(data);
            }
        }
    );
}

function placeCurrentShip(x, y)
{
    if (currentShipCanBePlaced)
    {
        player.AvailableShips[player.AvailableShips.length-1].X = parseInt(x);
        player.AvailableShips[player.AvailableShips.length-1].Y = parseInt(y);
        player.AvailableShips[player.AvailableShips.length-1].Orientation = parseInt(currentShipRotation);
        askServer_placeShip(player.AvailableShips[player.AvailableShips.length-1])
    }
}

function onPlaceShipOnBoardSuccess(responseData)
{
    console.log(responseData);
    var output = JSON.parse(responseData);
    if (output.Placed === true)
    {
        player.PlacedShips.push(player.AvailableShips[player.AvailableShips.length-1]);
        currentShipSize = 0;
        currentShipCanBePlaced = false;
        player.AvailableShips.pop();
         if(output.GameStarted === true)
        {
            StartGame();
        }
    }
    else
    {

    }
}

function markShotPosition(x, y, runFromRedraw)
{
    if (!isPlayerTurn)
    {
        return;
    }

    if (currentlyShootingShip.Size <= 0)
    {
        return;
    }

    lastMarkedX = x;
    lastMarkedY = y;

    if (currentEnemyBoard == null || runFromRedraw === true)
    {
        return
    }
    else
    {
        redrawEnemyBoard(currentEnemyBoard);
    }

    if (currentlyShootingShip.Orientation == 0)
    {
        for (i = 0; i < currentlyShootingShip.Size ; i++)
        {
            if(i < (15-x))
            {
                $("#gameRoom").find("#opponentSection").find("#gameSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(x)+parseInt(i)]+y).css('background-color','red');
            }
        }
    }
    else
    {
        for (i = 0; i < currentlyShootingShip.Size ; i++)
        {
            if(i < (15-y))
            {
                $("#gameRoom").find("#opponentSection").find("#gameSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(x)]+(parseInt(y)+i)).css('background-color','red');
            }
        }
    }

}

function shotEnemyPosition(x, y)
{
    if (!isPlayerTurn)
    {
        return;
    }

    if (currentlyShootingShip.Size <= 0)
    {
        return;
    }

    askServer_shotEnemy(parseInt(x), parseInt(y));
    //console.log("Bum bum X: " + parseInt(x) + " Y: " + parseInt(y));
}


function askServer_shotEnemy(x, y)
{
    var htmlData =
    {
        "playerNick": playerNick,
        "roomNumber": roomNumber,
        "shipId": currentlyShootingShip.Id,
        "x": parseInt(x),
        "y": parseInt(y),
    }

    console.log("askServer_shotEnemy htmlData: " + JSON.stringify(htmlData));

    $.ajax
    (
        {
            type : 'POST',
            url: 'shotEnemy',
            headers:
            {
                "Content-Type":"application/json"
            },
            data: JSON.stringify(htmlData),
            success: function(data)
            {
                onShotEnemySuccess(data);
            }
        }
    );
}

function onShotEnemySuccess(responseData)
{
    redrawEnemyBoard(JSON.parse(responseData))
    currentlyShootingShipIndex += 1;
     if (currentlyShootingShipIndex > player.PlacedShips.length - 1)
     {
         currentlyShootingShipIndex = 0;
     }
     currentlyShootingShip = player.PlacedShips[currentlyShootingShipIndex];
}


function redrawEnemyBoard(board)
{
    if (board === currentEnemyBoard)
    {
         board = currentEnemyBoard;
    }
    else
    {
        // Fix with different json parse settings
        board.Data.replace('/','');
        board = JSON.parse(board.Data);
        currentEnemyBoard = board;
        // End of fix. :(
    }

    if (lastMarkedX > 0 && lastMarkedY > 0)
    {
        markShotPosition(lastMarkedX, lastMarkedY, true);
    }

    for (x = 0; x < 15; x++)
    {
        for (y= 0; y < 15; y++)
        {
            var tileColor =  $("#gameRoom").find("#opponentSection").find("#gameSection").find("#boardSection").find("#board").find("#"+boardLetters[x]+y).css('background-color');
            var tile = board[boardLetters[x] + y.toString()];
            if(parseInt(tile) === 0) // EMPTY
            {
                tileColor = 'white';
            }
            else if(parseInt(tile) === 1) // PLACED
            {
                tileColor = 'green';
            }
            else if (parseInt(tile) === 2) // SHIP_SHOT
            {
                tileColor = 'red';
            }
            else if (parseInt(tile) === 3) // MISS
            {
                tileColor = 'blue';
            }
            else if (parseInt(tile) === 4) // USELESS
            {
                tileColor = 'gray';
            }
            else if (parseInt(tile) === 5) // VALUABLE
            {
                tileColor = 'yellow';
            }
            $("#gameRoom").find("#opponentSection").find("#gameSection").find("#boardSection").find("#board").find("#"+boardLetters[x]+y).css('background-color', tileColor);
        }
    }
}

function askServer_getMyBoard()
{
    var htmlData =
    {
        "playerNick": playerNick,
        "roomNumber": roomNumber,
    }

    console.log("askServer_getMyBoard htmlData: " + JSON.stringify(htmlData));

    $.ajax
    (
        {
            type : 'POST',
            url: 'getPlayerBoard',
            headers:
            {
                "Content-Type":"application/json"
            },
            data: JSON.stringify(htmlData),
            success: function(data)
            {
                onGetPlayerBoardSuccess(data);
            }
        }
    );
}

function onGetPlayerBoardSuccess(responseData)
{
    redrawMyBoard(JSON.parse(responseData));
}

function redrawMyBoard(board)
{
    // Fix with different json parse settings
    board.Data.replace('/','');
    board = JSON.parse(board.Data);
    // End of fix. :(

    for (x = 0; x < 15; x++)
    {
        for (y= 0; y < 15; y++)
        {
            var tileColor =  $("#gameRoom").find("#playerSection").find("#gameSection").find("#boardSection").find("#board").find("#"+boardLetters[x]+y).css('background-color');
            var tile = board[boardLetters[x] + y.toString()];
            if(parseInt(tile) === 0) // EMPTY
            {
                tileColor = 'white';
            }
            else if(parseInt(tile) === 1) // PLACED
            {
                tileColor = 'green';
            }
            else if (parseInt(tile) === 2) // SHIP_SHOT
            {
                tileColor = 'red';
            }
            else if (parseInt(tile) === 3) // MISS
            {
                tileColor = 'blue';
            }
            else if (parseInt(tile) === 4) // UNKNOWN
            {
                tileColor = 'gray';
            }
            else if (parseInt(tile) === 5) // VALUABLE
            {
                tileColor = 'yellow';
            }
            $("#gameRoom").find("#playerSection").find("#gameSection").find("#boardSection").find("#board").find("#"+boardLetters[x]+y).css('background-color', tileColor);
        }
    }
}


function askServer_getEnemyBoard()
{
    var htmlData =
    {
        "playerNick": playerNick,
        "roomNumber": roomNumber,
    }

    console.log("askServer_getEnemyBoard htmlData: " + JSON.stringify(htmlData));

    $.ajax
    (
        {
            type : 'POST',
            url: 'getEnemyBoard',
            headers:
            {
                "Content-Type":"application/json"
            },
            data: JSON.stringify(htmlData),
            success: function(data)
            {
                 redrawEnemyBoard(JSON.parse(data));
            }
        }
    );
}


function StartGame()
{
     $("#gameRoom").find("#playerSection").find("#gameSection").find("#availableShips").find("#rotateCurrentShip").hide();
     $("#gameRoom").find("#playerSection").find("#gameSection").find("#availableShips").find("#selectNextShip").hide();
    createSource_turnStatus();
};

function changeColor(x, y, color)
{
    $("#gameRoom").find("#opponentSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(x)+parseInt(y)]).css('background-color', 'yellow');
}

function clearTilesSelection()
{
    for (y = 0; y < 15; y++)
    {
        for (x= 0; x < 15; x++)
        {
            $("#gameRoom").find("#playerSection").find("#boardSection").find("#board").find("#"+boardLetters[x]+y).css('background-color', 'white');
        }
    }
}

function redrawPlacedShips()
{
    player.PlacedShips.forEach(highlightPlacedShip)
}

function highlightPlacedShip(item, index)
{
    if (parseInt(item["Orientation"])==0)
    {
        for (i = 0; i < parseInt(item["Size"]); i++)
        {
            $("#gameRoom").find("#playerSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(item["X"])+parseInt(i)]+item["Y"]).css('background-color','green');
        }
    }
    else
    {
        for (i = 0; i < parseInt(item["Size"]); i++)
        {
            $("#gameRoom").find("#playerSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(item["X"])]+(parseInt(item["Y"])+i)).css('background-color','green');
        }
    }
}

function selectNextShip()
{
    if (player.AvailableShips.length > 0)
    {
        currentShipSize = player.AvailableShips[player.AvailableShips.length-1].Size;
        $("#gameRoom").find("#playerSection").find("#gameSection").find("#availableShips").find("#selectNextShip").text("Połóż kolejny statek rozmiaru: " + currentShipSize);
    }
}

function rotateCurrentShip()
{
    if (currentShipSize <= 0)
    {
        return;
    }
    if (currentShipRotation===0)
    {
        currentShipRotation = 1
    }
    else
    {
        currentShipRotation = 0
    }
}

function checkBoundingBoxCollision(rect1, rect2)
{
    if (rect1.x < rect2.x + rect2.width && rect1.x + rect1.width > rect2.x && rect1.y < rect2.y + rect2.height && rect1.height + rect1.y > rect2.y)
    {
       return true;
    }
}


function tryPlaceCurrentShip(x,y)
{
    if (!enemyNick || 0 === enemyNick.length)
    {
        return;
    }

    if (currentShipSize <= 0)
    {
        return;
    }

    clearTilesSelection();
    redrawPlacedShips();

    if (currentShipRotation==0)
    {
        currentShipCanBePlaced = true;
        // Check against the board borders.
        if(parseInt(x) + currentShipSize < 15+1)
        {
            // Then against other ships.
            for (var i = 0, len =  player.PlacedShips.length; i < len; i++)
            {
                var rect1 = {x: parseInt(x), y: parseInt(y), width: currentShipSize, height: 1};;
                var rect2;

                if(parseInt( player.PlacedShips[i].Orientation) == 0)
                {
                    rect2 = {x: parseInt( player.PlacedShips[i].X)-1 , y: parseInt( player.PlacedShips[i].Y)-1, width: parseInt( player.PlacedShips[i].Size)+2, height: 3};
                }
                else
                {
                    rect2 = {x: parseInt( player.PlacedShips[i].X)-1 , y: parseInt( player.PlacedShips[i].Y)-1, width: 3, height: parseInt( player.PlacedShips[i].Size)+2};
                }
                if (checkBoundingBoxCollision(rect1, rect2))
                {
                    currentShipCanBePlaced = false;
                }
            }
        }
        else
        {
            currentShipCanBePlaced = false;
        }

        if (currentShipCanBePlaced)
        {
            for (i = 0; i < currentShipSize; i++)
            {
                $("#gameRoom").find("#playerSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(x)+parseInt(i)]+y).css('background-color','green');
            }
        }
        else
        {
            for (i = 0; i < currentShipSize; i++)
            {
                if(i < (15-x))
                {
                    $("#gameRoom").find("#playerSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(x)+parseInt(i)]+y).css('background-color','red');
                }
            }
        }
    }
    else
    {
        currentShipCanBePlaced = true;
        // Check against the board borders.
        if(parseInt(y) + currentShipSize < 15+1)
        {
            // Then against other ships.
            for (var i = 0, len =  player.PlacedShips.length; i < len; i++)
            {
                var rect1 = {x: parseInt(x), y: parseInt(y), width: 1, height: currentShipSize};;
                var rect2;

                if(parseInt( player.PlacedShips[i].Orientation) == 0)
                {
                    rect2 = {x: parseInt( player.PlacedShips[i].X)-1 , y: parseInt( player.PlacedShips[i].Y)-1, width: parseInt( player.PlacedShips[i].Size)+2, height: 3};
                }
                else
                {
                    rect2 = {x: parseInt( player.PlacedShips[i].X)-1 , y: parseInt( player.PlacedShips[i].Y)-1, width: 3, height: parseInt( player.PlacedShips[i].Size)+2};
                }
                if (checkBoundingBoxCollision(rect1, rect2))
                {
                    currentShipCanBePlaced = false;
                }
            }
        }
        else
        {
            currentShipCanBePlaced = false;
        }

        if (currentShipCanBePlaced)
        {
            for (i = 0; i < currentShipSize; i++)
            {
                $("#gameRoom").find("#playerSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(x)]+(parseInt(y)+i)).css('background-color','green');
            }
        }
        else
        {
            for (i = 0; i < currentShipSize; i++)
            {
                if(i < (15-y))
                {
                    $("#gameRoom").find("#playerSection").find("#boardSection").find("#board").find("#"+boardLetters[parseInt(x)]+(parseInt(y)+i)).css('background-color','red');
                }
            }
        }
    }
}
