var config = {
    playerId: "",
    gameId: "",
    clientGameUrl : window.location.href.replace(window.location.search, "").replace("#", ""),
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