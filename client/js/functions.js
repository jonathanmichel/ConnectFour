function printBoard() {
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