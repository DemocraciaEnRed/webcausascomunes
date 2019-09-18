// to top right away
if ( window.location.hash ) scroll(0,0);
// void some browsers issue
setTimeout( function() { scroll(0,0); }, 1);

$(document).ready(function(){
    if(window.location.hash) {
        $('html, body').animate({
          scrollTop: $(window.location.hash).offset().top - $("#navbar").innerHeight()
        }, 1000);
    }
})