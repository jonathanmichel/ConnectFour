function loadBoard() {
    var infDiv = $("#gameBoard");
    var content = "<table class='board' align='center' id='board'>"
    for(var i=0; i<6; i++){
        content += '<tr>';
        for(var j=0; j<7; j++) {
            content += "<td><i class='em-svg em-white_large_square board_button'></i></td>"
        }
        content += '</tr>';
    }
    content += "</table>"
    
    infDiv.append(content);
    // Click listener
    $(".board_button").click(function(e) {
        var x_pos = $(this).closest('tr').find('td').index($(this).closest('td'))
        sendAction(x_pos)
    })
}

function setEmojiSelectorButton(emoji) {
    var button = $(".emojiSelectorButton")
    button.removeClass();
    button.attr('class', 'em-svg emojiSelectorButton ' + emoji)
}

function emojiSelectorShow() {
    $(".emojiSelectorDiv").show();
    $(".emojiSelectorItem").click(function(e) {
        var emoji = $(this).closest('i').attr('class').split(" ")[2];
        changeEmoji(emoji);
        emojiSelectorHide();
    })
}

function emojiSelectorHide() {
    $(".emojiSelectorDiv").hide();
}

function clearBoard() {
    $("#gameBoard").remove();
}

function updateBoard(emoji0, emoji1) {
    for (var y = 0; y <= 5; y++) {
        for (var x = 0; x <= 6; x++) {
            var cell = $("tr:eq(" + y + ")").find('td').eq(x);
            var item = cell.children('i');
            item.attr("class", "em-svg board_button");
            switch(board[y][x]) {
                case '0':
                    item.addClass(emoji0);
                    break;
                case '1':
                    item.addClass(emoji1);
                    break;
                case 'x':
                    item.addClass("em-white_large_square");
                    break;
            }
        }
    }
}