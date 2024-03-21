
var current_page = window.location.href;

var nav_links = document.querySelectorAll('.navbar a');

for (var i=0 ; i<nav_links.length;i++) {
    var link = nav_links[i];
    var linkUrl = link.href;

    if (current_page === linkUrl){
        link.classList.add('active');
    }

    
}


let eyeicon = document.getElementById("eyeicon");
let eyeicon2 = document.getElementById("eyeicon2");
let password = document.getElementById("password");
let verify_password = document.getElementById("verify_password");

eyeicon.onclick = function(){
    if(password.type == "password"){
        password.type = "text";
        eyeicon.src ="/static/eye-open.png"
    }else{
        password.type = "password";
        eyeicon.src ="/static/eye-close.png"
    }
}

eyeicon2.onclick = function(){
    if(verify_password.type == "password"){
        verify_password.type = "text";
        eyeicon2.src ="/static/eye-open.png"
    }else{
        verify_password.type = "password";
        eyeicon2.src ="/static/eye-close.png"
    }
}
