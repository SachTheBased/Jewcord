function get_messages () {
    var server = JSON.stringify(window.location.href).split("/")[4];
    var channel = JSON.stringify(window.location.href).split("/")[5][0]; // js being weird
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
             var res = JSON.parse(xhttp.responseText);
             var messages = res["messages"];

            for (let pos = 0; pos < messages.Length; pos++) {
                var display = document.getElementById("messages");
                var message = messages[pos];

                message_display = `<div id="message">
    <div id="author">${message["author"]["name"]}</div><br>
    <div id="content">message["content"]</div>
</div>
`;
                display += message_display;
            }
        }
    };

    xhttp.open("GET", `/api/v1/chats/${server}/${channel}/messages`, true);
    xhttp.setRequestHeader('token', localStorage.getItem("token"));
    xhttp.send();
}

function send_message(content) {
    var server = JSON.stringify(window.location.href).split("/")[4];
    var channel = JSON.stringify(window.location.href).split("/")[5][0];
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
    }

    xhttp.open("POST", `/api/v1/chats/${server}/${channel}/messages`, true);
    xhttp.setRequestHeader('token', localStorage.getItem("token"));
    xhttp.send(JSON.stringify({"content": content, "embeds": [], "files": []}));
}

get_messages();

var form = document.getElementById("form");
form.addEventListener("submit", event => {
    event.preventDefault();
    send_message(document.getElementById('sendMSG').value);
    document.getElementById('sendMSG').value = ""
});