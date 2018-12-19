$(document).ready(function() {
    $('#newGame').click(function(event){
        event.preventDefault();
        createGame()
    });
    
    favicon = new Favico({
        position  :'up',
        animation :'pop',
        bgColor   :'#dd2c00',
        textColor :'#fff0e2'
    });

    loadEmojis();

    var gameId = getUrlParameter("gameId");
    if(gameId) {
        var playerId = getUrlParameter("playerId");
        if(playerId) {
            loadGame(gameId, playerId);
        } else {
            joinGameId(gameId);
        }
    }
})

function loadGame(gameId, playerId) {
    config.playerId = playerId.replace("#", "");
    config.gameId = gameId.replace("#", "");

    $("#mainView").remove();
    $('#gameView').show();

    $("#inviteLinkInput").val(config.clientGameUrl + "?gameId=" + config.gameId);
    $("#inviteLinkBtn").click(function(event){
        toastr.info("Link copied to clipboard");
    });
    var clipboard = new ClipboardJS('.btn');

    loadBoard();
    
    updateGame();
    timerId = setInterval(update, 1000);
    
    $('.play-again').click(function(e) {
        location.reload();
    });
    
    toastr.success("Game loaded");
}

function update() {
    updateGame();
}

function abortTimer() {
    clearInterval(timerId);
}

function parserJson(data) {
    if('ERROR' in data) {
        if (data.ERROR === "NOT YOUR TURN") {
            toastr.error("Please wait, it seems it's not your turn. Thank you :)")
        } else {
            toastr.error(data.ERROR);
        }
        return;
    }

        config.player = data.id;

    data.grid = String(data.grid.replace(new RegExp("\n", 'g'),""));
    for (var x = 0; x < 7; x++) {
        for (var y = 0; y < 6; y++) {
                board[y][x] = data.grid.charAt(7 * y + x);
            }
    }

    var stateMessage = "...";

    // Opponent state
    if(data["player" + (1-data.id) + "Status"]) {
        stateMessage = "Opponent is playing";
        $("#linkDiv").hide()
    } else {
        stateMessage = "Opponent is not connected";
        $("#linkDiv").show()
    }

    if(data.isWin === "-1") {            // During party
        // Player changes
        var currentPlayer = data.currentPlayer;
        if(lastPlayer !== currentPlayer) {
            favicon.badge(currentPlayer === config.player ? "!" : "")
        }
        lastPlayer = currentPlayer;

        // Player hat to play
        if(currentPlayer === config.player) {
            stateMessage = "Your turn";
            document.title = "Connect four - Your turn";
        } else {
            document.title = "Connect four";
        }
    } else {                            // End of party
        var restartGame = "<a onclick='resetGame()' href='#'>Restart game</a>";
        var winnerTxt = (data.isWin === config.player ? "You" : "Opponent") + " won";
        stateMessage = winnerTxt + " - ";
        document.title = "Connect four - " + winnerTxt;
    }

    var stateMessageDiv = $('#stateMessage');
    stateMessageDiv.text(stateMessage);
    stateMessageDiv.append(restartGame);

    drawBoard(data.player0Emoji, data.player1Emoji, data["player" + data.isWin + "Emoji"]);
    setEmojiSelectorButton(data["player" + data.id + "Emoji"]);
}

function loadEmojis() {
    var client = new XMLHttpRequest();
    client.open('GET', 'assets/emojisRaw.txt');
    client.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200) {
                var emojis = client.responseText.split("\n");
                var nbOfEmojis = emojis.length;
                var index = [];
                while (true) {
                    var i = Math.floor(Math.random() * (nbOfEmojis - 1));
                    index.push(i);
                    index = uniqueArray(index);
                    if (index.length === 32)
                        break;
                }
                var menu = $(".emojiSelectorMenu");
                menu.empty();
                index.forEach(function(e){
                    menu.append("<i class='em-svg emojiSelectorItem " + emojis[e] + "'></i>")
                });

                $(".emojiSelectorButton").click(function(e) {
                    emojiSelectorShow()
                });
                $(".emojiSelectorDiv").click(function(e) {
                    emojiSelectorHide()
                });

            }
        }
    };

    client.send();
}


function createGame() {
    toastr.info("Creating new game...");
    $.ajax({
        url: config.serverUrl + "/createGame",
        success : function(data) {
            console.log(data);
            if(data.playerID && data.gameID) {
                console.log("coucou")
                window.location.href = config.clientGameUrl + "?gameId=" + data.gameID + "&playerId=" + data.playerID
            } else {
                toastr.error("Game creation failed");
            }
        },
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable");
        }
    })
}

function joinGameId(gameId) {
    if(!gameId)
        return;
    
    $.ajax({
        url: config.serverUrl + "/joinGame/" + gameId,
        success : function(data) {
            if(data.playerID && data.gameID) {
                window.location.href = config.clientGameUrl + "?gameId=" + data.gameID + "&playerId=" + data.playerID
            } else {
                toastr.error("Join game failed")
            }
        },
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable");
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
            toastr.error("Server unreachable");
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
            toastr.error("Server unreachable");
        }
    })
}

function quitGame() {
    $.ajax({
        url: config.serverUrl + "/quitGame/" + config.playerId,
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable");
        }
    })
}

function changeEmoji(emoji) {
    $.ajax({
        url: config.serverUrl + "/setEmoji/" + config.playerId + "/" + emoji,
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable");
        }
    })
}

function resetGame() {    
    $.ajax({
        url: config.serverUrl + "/resetGame/" + config.playerId,
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable");
        }
    })
}