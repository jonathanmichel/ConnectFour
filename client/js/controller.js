$(document).ready(function() {
    var clipboard = new ClipboardJS('.btn');
    
     // Ask server port
    var reg = new RegExp('^\d*')
    var port;
    while(true) {
        port = prompt("Choose port :", "15576");
        if(reg.test(port))
            break;
    }
    config.serverPort = port;

    joinGame(getUrlParameter("gameId"));
    
    window.addEventListener('beforeunload', function(e) {
        quitGame();
        //e.preventDefault(); //per the standard
        //e.returnValue = ''; //required for Chrome
    });
});

function loadGame() {
    //*/
    $('#player').text(config.playerPrefix + (config.player + 1) + " ");
    
    var content = "<input id='gameUrl' value='http://techiteasy.ch/game?gameId=" + config.gameId + "'><button class='btn' data-clipboard-target='#gameUrl'>Copy to clipboard</button>";
    $('#player').append(content);
    
    loadBoard();
    
    updateGame();
    timerId = setInterval(update, 1000);
        
    // Click on the board
    $('.board_button').click(function(e) {
        var x_pos = $(this).closest('tr').find('td').index($(this).closest('td'));

        // todo Send x position
        sendAction(x_pos);
    });

    $('.play-again').click(function(e) {
        location.reload();
    });
}

function update() {
    updateGame();
}

function abortTimer() {
    clearInterval(timerId);
}

function parserJson(data) {
    data.grid = String(data.grid.replace(new RegExp("\n", 'g'),""));
        for (var x = 0; x < 7; x++) {
            for (var y = 0; y < 6; y++) {
                    board[y][x] = data.grid.charAt(7 * y + x);
                }
        }

        if(data.isWin == "0") {
            if(parseInt(data.player) == config.player)
                $('#state').text("Your turn");
            else
                $('#state').text("Waiting for opponent");
        }

        var restartGame = "<a onclick='resetGame()' href='#'>Restart game</a>";

        switch(data.isWin) {
            case "Token.PLAYER0":
                $('#state').text("Player 1 won - ");
                $('#state').append(restartGame);
                break;
            case "Token.PLAYER1":
                $('#state').text("Player 2 won - ");
                $('#state').append(restartGame);
            break;
        }
    updateBoard();
}

function newGame() {
    $.ajax({
        url: getServerUrl() + "/createGame"
    }).then(function(data) {
        if(data.playerID != 0 && data.gameID != 0) {
            config.playerId = data.playerID;
            config.gameId = data.gameID;
            config.player = 0;
            
            var copyInput = document.getElementById("gameId");
            copyInput.value = data.gameID;
            copyInput.select();
            document.execCommand("copy");
            
            loadGame();
        } else {
            console.log("Create game failed");
        }
    });
}

function joinGame() {
    var gameId = prompt("Enter game ID");
    joinGame(gameId);    
}

function joinGame(gameId) {
    if(gameId == null || gameId == undefined)
        return;
    
     $.ajax({
        url: getServerUrl() + "/joinGame/" + gameId
    }).then(function(data) {
        if(data.playerID != 0 && data.gameID != 0) {
            config.playerId = data.playerID;
            config.gameId = data.gameID;
            config.player = 1;
            loadGame();
        } else {
            console.log("Join game failed");
        }
    });
}

function getServerUrl() {
    return config.serverUrl + config.serverPort;
}

function quitGame() {
    $.ajax({
        url: getServerUrl() + "/quitGame/" + config.playerId
    });
}

function updateGame() {
    $.ajax({
        url: getServerUrl() + "/getGame/" + config.playerId
    }).then(function(data) {
        parserJson(data);
    });
}

function sendAction(position) {
    var url = getServerUrl() + "/play/" + config.playerId + "/" + position;    
    $.ajax({
        url: url
    }).then(function(data) {
        parserJson(data);
    });

}

function resetGame() {
    $.ajax({ 
        url: getServerUrl() + "/resetGame/" + config.playerId
    });
}