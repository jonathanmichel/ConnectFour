var config = {
    playerId: 0,
    gameId: 0,
    player: 1,
    clientGameUrl : window.location.href.replace(window.location.search, ""),
    serverUrl : "https://connectfour.serveo.net" 
}

var board = [['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x']]

var lastPlayer

var timerId

var favicon