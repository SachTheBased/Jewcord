function signup() {
  var username = document.getElementById('usernameVal').value;
  var password = document.getElementById('passwordVal').value;
  var email = document.getElementById('emailVal').value;
  var xhttp = new XMLHttpRequest();
  
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      res = JSON.parse(xhttp.responseText);
      localStorage.setItem('token', res["token"]);
      window.location.href = "/chats/0/0";
    }
  };

  xhttp.open("POST", "/api/v1/signup", true);
  xhttp.send(JSON.stringify({"name": username, "password": password, "email": email}));
}