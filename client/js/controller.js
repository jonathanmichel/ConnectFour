$(document).ready(function() {
    $('#newGame').click(function(event){
        event.preventDefault()
        createGame()
    })
    
    favicon = new Favico({
        position  :'up',
        animation :'pop',
        bgColor   :'#dd2c00',
        textColor :'#fff0e2'
    })
        
    var gameId = getUrlParameter("gameId")
    if(gameId != null || gameId != undefined) {
        var playerId = getUrlParameter("playerId")
        if(playerId != null || playerId != undefined) {
            var player = getUrlParameter("player")
            loadGame(gameId, playerId, player)
        } else {
            joinGameId(gameId)
        }
    }
})

function loadGame(gameId, playerId, player) {        
    config.playerId = playerId
    config.gameId = gameId
    config.player = player
    
    $("#mainView").remove()
    $('#gameView').show()
    
    if(player == 0) {
        $("#inviteLinkInput").val(config.clientGameUrl + "?gameId=" + config.gameId)
        $("#inviteLinkBtn").click(function(event){
            toastr.info("Link copied to clipboard")
        })
        var clipboard = new ClipboardJS('.btn')
    } else {
        $("#linkDiv").remove();
    }
    
    loadBoard()
    
    updateGame()
    timerId = setInterval(update, 1000)
    
    $('.play-again').click(function(e) {
        location.reload()
    })
    
    toastr.success("Game loaded")
}

function update() {
    updateGame()
}

function abortTimer() {
    clearInterval(timerId)
}

function parserJson(data) {
    if('ERROR' in data) {
        toastr.error(data.ERROR)
        return
    }

    data.grid = String(data.grid.replace(new RegExp("\n", 'g'),""))
    for (var x = 0; x < 7; x++) {
        for (var y = 0; y < 6; y++) {
                board[y][x] = data.grid.charAt(7 * y + x)
            }
    }

    if(data.isWin == "0") {
        var currentPlayer = parseInt(data.player)
        // Player changed
        if(lastPlayer != currentPlayer) {
            favicon.badge(currentPlayer == config.player ? "!" : "")
        }  
        
        if(currentPlayer == config.player) {
            $('#stateMessage').text("Your turn")
            document.title = "Connect four - Your turn"
        } else {
            $('#stateMessage').text("Waiting for opponent")
            document.title = "Connect four"
        }
        lastPlayer = currentPlayer;
    }

    var restartGame = "<a onclick='resetGame()' href='#'>Restart game</a>"
    switch(data.isWin) {
        case "Token.PLAYER0":
        case "Token.PLAYER1":
            var winnerId = data.isWin.substr(data.isWin.length-1)
            $('#stateMessage').text((winnerId == config.player ? "You" : "Opponent") + " won - ")
            $('#stateMessage').append(restartGame)
            //$('.board_button').unbind()
            break;
    }
    updateBoard()
}


function createGame() {
    toastr.info("Creating new game...")
    $.ajax({
        url: config.serverUrl + "/createGame",
        success : function(data) {
            if(data.playerID != 0 && data.gameID != 0) {            
                window.location.href = config.clientGameUrl + "?gameId=" + data.gameID + "&playerId=" + data.playerID + "&player=0"
            } else {
                toastr.error("Game creation failed")
            }
        },
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable")
        }
    })
}

function joinGameId(gameId) {
    if(gameId == null || gameId == undefined)
        return
    
    $.ajax({
        url: config.serverUrl + "/joinGame/" + gameId,
        success : function(data) {
            if(data.playerID != 0 && data.gameID != 0) {           
                window.location.href = config.clientGameUrl + "?gameId=" + data.gameID + "&playerId=" + data.playerID + "&player=1"
            } else {
                toastr.error("Join game failed")
            }
        },
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable")
        }
    })
}

function updateGame() {
    $.ajax({
        url: config.serverUrl + "/getGame/" + config.playerId,
        success : function(data) {
            parserJson(data)
        },
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable")
        }
    })
}

function sendAction(position) {
    $.ajax({
        url: config.serverUrl + "/play/" + config.playerId + "/" + position,
        success : function(data) {
            parserJson(data)
        },
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable")
        }
    })
}

function quitGame() {
    $.ajax({
        url: config.serverUrl + "/quitGame/" + config.playerId,
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable")
        }
    })
}

function resetGame() {    
    $.ajax({
        url: config.serverUrl + "/resetGame/" + config.playerId,
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable")
        }
    })
}