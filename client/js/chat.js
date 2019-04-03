$('#btn-input').keyup(function(e){
    if(e.which === 13) {
        sendMessage();
    }
});

$('#msg_container').on('shown.bs.collapse', function (e) {
    $('#collapseChatButton').text("-");
    $('#notificationDivChat').html('');
    updateNotificationChat();
});

$('#msg_container').on('hide.bs.collapse', function (e) {
    $('#collapseChatButton').text("+");
});

var updateNotificationChat = function() {
    if($('#msg_container').hasClass('show')) {
        lastMessageRead = lastMessageReceived;
    } else {
        if (lastMessageRead !== lastMessageReceived) {
            $('#notificationDivChat').html('<span class="badge badge-danger">!</span>');
        }
    }
}

var setMessages = function(array) {
    if(array.length != 0) {
        var lastElement = array[array.length - 1];
        lastMessageReceived = lastElement.timestamp + lastElement.text;
        console.log(lastElement.timestamp);
    }
    updateNotificationChat();

    clearMessages();
    array.forEach(function(element) {
        createMessage(element.playerID, element.text, element.timestamp)
    });
    $("#msg_container_base").scrollTop($("#msg_container_base").prop("scrollHeight"));
};

var clearMessages = function() {
    $('#msg_container_base').empty()
};

var createMessage = function(playerId, text, datetime) {
    var msgKind = "sent";
    var author = "You";
    if(playerId !== config.playerId) {
        msgKind = "receive";
        author = "Little red shit";
    }
    if(playerId === "admin") {
        msgKind = "admin";
        author = "Administrator";
    }
	let today = new Date();
	let hourNow = today.getHours();
	let minNow = today.getMinutes();
	let secNow = today.getSeconds();
	
    let hour = parseInt(datetime);
    let min = datetime.substring(3,5);
    let sec = datetime.substring(6,8);
	
	let deltaHour = hourNow-hour;
	let deltaMin = minNow-min;
	let deltaSec = secNow-sec;
	
	let timeStampToShow = ""
	
	if(deltaHour === 0 && deltaMin === 0)
		timeStampToShow = "A few seconds ago"	
	else if(deltaHour === 0 && deltaMin === 1)
		timeStampToShow = deltaMin+" minute ago"
	else if(deltaHour === 0 && deltaMin !== 0)
		timeStampToShow = deltaMin+" minutes ago"	
	else if(deltaHour === 1)
		timeStampToShow = deltaHour+" hour ago"
	else if(deltaHour !== 0)
		timeStampToShow = deltaHour+" hours ago"

    $('#msg_container_base').append(
        "<div class='row msg_container base_" + msgKind +"'>\n" +
        "    <div class='col-md-10 col-xs-10'>\n" +
        "        <div class='messages message_" + msgKind + "'>\n" +
        "            <p>" + text + "</p>\n" +
        "            <time datetime='" + datetime + "'>" + author + " • <span class='time_elapsed'>"+timeStampToShow+"</span></time>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>");
    // 2009-11-13T20:00
};

var sendMessage = function() {
    var input = $('#btn-input');
    if(input.val())
        sendMessageText(input.val());
    input.val('')
};

var sendMessageText = function(text) {
    if(text === "")
        return;

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