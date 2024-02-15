var x = document.getElementById("login")
var y = document.getElementById("register")
var z = document.getElementById("btn")

function register() {
    x.style.left = "-400px";
    y.style.left = "50px";
    z.style.left = "110px";

    document.getElementById("login_button").style.color = "#999";
    document.getElementById("register_button").style.color = "black";

}

function login() {
    x.style.left = "50px";
    y.style.left = "450px";
    z.style.left = "0px";

    document.getElementById("login_button").style.color = "black";
    document.getElementById("register_button").style.color = "#999";
}