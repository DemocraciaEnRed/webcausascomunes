// to top right away
if ( window.location.hash ) scroll(0,0);
// void some browsers issue
setTimeout( function() { scroll(0,0); }, 1);

//https://github.com/blueimp/Gallery
function initBlueimp(onopened){
    blueimp.Gallery(document.getElementById('links').getElementsByTagName('a'), {
        container: '#blueimp-gallery-carousel',
        carousel: true,
        onopened: onopened
    })
}

function hashScroll() {
    if(window.location.hash) {
        $('html, body').animate({
          scrollTop: $(window.location.hash).offset().top
        }, 1000);
    }
}

var navbar_anchor = $("#navbar").innerHeight();
var navbar = $("#navbar");

function scrollHandler(){
/*     if ($(this).scrollTop() >= ($("#propuestas").offset().top) - 150) {
        //$(window).off('scroll', scrollHandler);
    } */
    if ($(this).scrollTop() >= navbar_anchor && !navbar.hasClass('scrolling') ) {    
        navbar.addClass('scrolling');
    } else if ($(this).scrollTop() < navbar_anchor && navbar.hasClass('scrolling')) {   
        navbar.removeClass('scrolling');
    }
}

$(document).ready(function(){
    initBlueimp(hashScroll);

    $( window ).scroll(scrollHandler);

    $('.scrollTo').click(function(e) {
        e.preventDefault();
        var sectionTo = $(this).attr('href');
        $('html, body').animate({
          scrollTop: $(sectionTo).offset().top
        }, 1000);
    });
    
})
