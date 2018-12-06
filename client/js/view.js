function loadBoard() {
    $("#menu").remove();
    var infDiv = $("#info");
    var content = "<table class='board' align='center' id='board'>"
    for(var i=0; i<6; i++){
        content += '<tr>';
        for(var j=0; j<7; j++) {
            content += "<td><i class='em-svg em-black_large_square board_button'></i></td>"
        }
        content += '</tr>';
    }
    content += "</table>"
    
    infDiv.append(content);
}

function clearBoard() {
    $("#board").remove();
}

function updateBoard() {
    for (var y = 0; y <= 5; y++) {
        for (var x = 0; x <= 6; x++) {
            var cell = $("tr:eq(" + y + ")").find('td').eq(x);
            var item = cell.children('i');
            item.attr("class", "em-svg board_button");
            switch(board[y][x]) {
                case '0':
                    item.addClass("em-airplane");
                    break;
                case '1':
                    item.addClass("em-bulb");
                    break;
                case 'x':
                    item.addClass("em-black_large_square");
                    break;
            }
        }
    }
}