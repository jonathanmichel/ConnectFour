$(document).on('click', '.panel-heading span.icon_minim', function (e) {
    /*
    var $this = $(this);
    if (!$this.hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideUp();
        $this.addClass('panel-collapsed');
        $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
    } else {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.removeClass('panel-collapsed');
        $this.removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
    */
});

$(document).on('focus', '.panel-footer input.chat_input', function (e) {
    /*
    var $this = $(this);
    if ($('#minim_chat_window').hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideDown();
        $('#minim_chat_window').removeClass('panel-collapsed');
        $('#minim_chat_window').removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
    */
});

$('#btn-input').keyup(function(e){
    if(e.which === 13) {
        sendMessage();
    }
});

var setMessages = function(array) {
    clearMessages();
    array.forEach(function(element) {
        createMessage(element.playerID, element.text, element.timestamp)
    });
};

var clearMessages = function() {
    $('#msg_container_base').empty()
};

var createMessage = function(playerId, text, datetime) {
    var msgKind = "sent";
    var author = "You";
    console.log("p:" + playerId);
    console.log("c:" + config.playerId)
    if(playerId !== config.playerId) {
        msgKind = "receive";
        author = "Little red shit";
    }

    $('#msg_container_base').append(
        "<div class='row msg_container base_" + msgKind +"'>\n" +
        "    <div class='col-md-10 col-xs-10'>\n" +
        "        <div class='messages message_" + msgKind + "'>\n" +
        "            <p>" + text + "</p>\n" +
        "            <time datetime='" + datetime + "'>" + author + " • <span class='time_elapsed'>51 min</span></time>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>");
    // 2009-11-13T20:00
};

var sendMessage = function() {
    var input = $('#btn-input');
    sendMessageText(input.val());
    input.val('')
};

var sendMessageText = function(text) {
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: config.serverUrl + "/chat",
        data: JSON.stringify({ playerID : config.playerId, text : text }),
        error : function (XMLHttpRequest, textStatus, errorThrown) {
            toastr.error("Server unreachable");
        }
    });
};

/*
<div class="row msg_container base_receive">
    <div class="col-md-10 col-xs-10">
        <div class="messages msg_receive">
            <p>Ta mère</p>
            <time datetime="2009-11-13T20:00">Anna • 51 min</time>
        </div>
    </div>
</div>
 */




