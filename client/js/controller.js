
$(document).ready(function() {
    // Setup game
    var reg = new RegExp('^[1-2]$');
    var id;
    while(true) {
        id = prompt("Choose player 1 or 2 ?");
        if(reg.test(id))
            break;
    }
    config.playerId = id - 1;
    $('#player').text(config.playerPrefix + (config.playerId + 1));
    
    resetGame();
    getGame();
    var tid = setInterval(update, 1000);
    
    function update() {
        getGame();
    }
    
    function abortTimer() {
      clearInterval(tid);
    }

    // Click on the board
    $('.board_button').click(function(e) {
        var x_pos = $(this).closest('tr').find('td').index($(this).closest('td'));

        // todo Send x position
        sendAction(config.playerId, x_pos);
    });

    $('.play-again').click(function(e) {
        location.reload();
    });

});

function getGame() {
    $.ajax({
        url: "http://tcp.ngrok.io:17582/getGame"
    }).then(function(data) {
        data = String(data.replace(new RegExp("\n", 'g'),""));
        for (var x = 0; x < 7; x++) {
            for (var y = 0; y < 6; y++) {
                    board[y][x] = data.charAt(7 * y + x);
                }
        }
        printBoard();
    });
}


function sendAction(player, position) {
    /*
    # return 1 if success
    # return 2 if not your turn
    # return 3 if not in grid
    # return 4 if line full
    # return 5 player not 0 or 1
    # return 6 player 0 win
    # return 7 player 1 win
    */
    var url = "http://tcp.ngrok.io:17582/play/" + player + "/" + position;    
    $.ajax({
        url: url
    }).then(function(data) {
        switch(data) {
            case '1':
                $('#state').text("Nice move !");
                break;
            case '2':
                $('#state').text("Wait your turn bitch");
                console.log("atasioth");
                break;
            case '3':
                console.log("Not in grid");
                break;
            case '4':
                $('#state').text("Line is full asshole");
                break;
            case '5':
                console.log("Invalid player");
                break;
            case '6':
                $('#state').text("Player 1 win");
                break;
            case '7':
                $('#state').text("Player 2 win");
                break;
            default:
                console.log("WTF?");
                break;
        }
    });
}

function resetGame() {
    $.ajax({ 
        url: "http://tcp.ngrok.io:17582/resetGame"
    });
}