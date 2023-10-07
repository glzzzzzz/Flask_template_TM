console.log("Script bien chargé")

var currentUrl = window.location.href;

var navLinks = document.querySelectorAll('.navbar a');

for (var i=0 ; i<navLinks.length;i++) {
    var link = navLinks[i];
    var linkUrl = link.href;

    if (currentUrl === linkUrl){
        link.classList.add('active');
    }
}