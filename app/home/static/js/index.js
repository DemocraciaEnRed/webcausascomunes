// to top right away
if ( window.location.hash ) scroll(0,0);
// void some browsers issue
setTimeout( function() { scroll(0,0); }, 1);

var carousel;

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

function initSliderPropuestas() {
    return $('#carousel').flickity({
        groupCells: true
    });
}

function scrollHandler(){
    if ($(this).scrollTop() >= ($("#propuestas").offset().top) - 150) {
        carousel.flickity('playPlayer');
        $(window).off('scroll', scrollHandler);
    }
}

$(document).ready(function(){
    initBlueimp(hashScroll);

    carousel = initSliderPropuestas();
    $( window ).scroll(scrollHandler);

    $('.scrollTo').click(function(e) {
        e.preventDefault();
        var sectionTo = $(this).attr('href');
        $('html, body').animate({
          scrollTop: $(sectionTo).offset().top
        }, 1000);
    });
    
})
