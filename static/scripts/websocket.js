const ws = new WebSocket("wss://Chat-Websockets.sachsthebased.repl.co");

ws.onopen = (event) => {
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      out = JSON.parse(xhttp.responseText);
      var identify = {
        "type": 0,
        "token": localStorage.getItem("token"),
        "servers": out["status"]["servers"]
      }
      console.log(identify);
      ws.send(JSON.stringify(identify));
    }
  };

  xhttp.open("GET", "https://Chat.sachsthebased.repl.co/api/v1/users/@me", true);
  xhttp.setRequestHeader('token', localStorage.getItem("token"));
  xhttp.send();
}
  
ws.onmessage = (event) => {
  var data = JSON.parse(event.data);
  var vals = window.location.pathname.split("/")

  console.log(vals)
  
  // if (data["server"]) == 
  document.getElementById("messages").innerHTML += `<div id="message"><span id="author">${data["author"]["username"]}</span><br><span id="content">${data["content"]}</span></div><br><br>`;
  document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}