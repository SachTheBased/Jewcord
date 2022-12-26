function login() {
  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value;
  var xhttp = new XMLHttpRequest();
  
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      out = JSON.parse(xhttp.responseText);
      localStorage.setItem('token', out["status"]);
      window.location.href = "https://Chat.sachsthebased.repl.co/chat";
    }
  };

  xhttp.open("POST", "https://Chat.sachsthebased.repl.co/api/v1/login", true);
  xhttp.send(JSON.stringify({"username": username, "password": password}));
}