var config = {
        PlayerName: "Player",
        PlayerId: 1,
        drawMsg: "This game is a draw.",
        playerPrefix: "You are player ",
        winPrefix: "The winner is: ",
        countToWin: 4,
    };

var board = [['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x'],
             ['x','x','x','x','x','x','x']];

var currentPlayer = config.startingPlayer;
