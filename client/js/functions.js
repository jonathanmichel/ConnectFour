var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.href.split('?')[1];
    if(!sPageURL)
        return undefined;
    var    sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
}

var uniqueArray = function(arrArg) {
    return arrArg.filter(function(elem, pos,arr) {
        return arr.indexOf(elem) == pos;
    });
};