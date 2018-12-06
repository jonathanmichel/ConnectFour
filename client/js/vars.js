var config = {
    playerId: 0,
    gameId: 0,
    player: 1,
    drawMsg: "This game is a draw.",
    playerPrefix: "You are player ",
    winPrefix: "The winner is: ",
    countToWin: 4,
    serverPort : 13769,
    serverUrl : "http://tcp.eu.ngrok.io:",
    
};

var board = [['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x']];

var currentPlayer = config.startingPlayer;

var timerId;