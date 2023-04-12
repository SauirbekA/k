
// https://api.telegram.org/bot5970994672:AAHR5Mux2ikEkRm5VmHK-s--LBSsCK_1x6k/sendMessage?chat_id=-1001821458102&text=hi_i_am

// https://api.telegram.org/bot5970994672:AAHR5Mux2ikEkRm5VmHK-s--LBSsCK_1x6k/sendMessage?chat_id=1057757081&text=hi_i_am

// https://api.telegram.org/bot5970994672:AAHR5Mux2ikEkRm5VmHK-s--LBSsCK_1x6k/getUpdates


// alert('Welcome to our site')

//bot token
var telegram_bot_id = "5970994672:AAHR5Mux2ikEkRm5VmHK-s--LBSsCK_1x6k";
//chat id
var chat_id = 1057757081;
var u_name, email, message;
var ready = function () {
    u_name = document.getElementById("name").value;
    email = document.getElementById("email").value;
    message = document.getElementById("message").value;
    message = "Name: " + u_name + "\nEmail: " + email + "\nMessage: " + message;
};
var sender = function () {
    ready();
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://api.telegram.org/bot" + telegram_bot_id + "/sendMessage",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "cache-control": "no-cache"
        },
        "data": JSON.stringify({
            "chat_id": chat_id,
            "text": message
        })
    };
    $.ajax(settings).done(function (response) {
        console.log(response);
    });
    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("message").value = "";
    return false;
};