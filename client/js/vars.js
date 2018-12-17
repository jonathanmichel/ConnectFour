var config = {
    playerId: 0,
    gameId: 0,
    player: 1,
    serverUrl : "https://connectfour.serveo.net" //http://tcp.eu.ngrok.io: http://localhost:
}

//var server = "http://localhost/connectFour/"
//var server = "file:///C:/Users/jonat/Documents/ConnectFour/client/"
var server = "http://techiteasy.ch/"

var board = [['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x']]

var lastPlayer

var timerId

var favicon