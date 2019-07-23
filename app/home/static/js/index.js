// to top right away
if ( window.location.hash ) scroll(0,0);
// void some browsers issue
setTimeout( function() { scroll(0,0); }, 1);

$(document).ready(function(){
    $('.scrollTo').click(function(e) {
        e.preventDefault();
        var sectionTo = $(this).attr('href');
        $('html, body').animate({
          scrollTop: $(sectionTo).offset().top
        }, 1000);
    });
    if(window.location.hash) {
        $('html, body').animate({
          scrollTop: $(window.location.hash).offset().top
        }, 1000);
    }

    initBlueimp();
})

//https://github.com/blueimp/Gallery
function initBlueimp(){
    blueimp.Gallery(document.getElementById('links').getElementsByTagName('a'), {
        container: '#blueimp-gallery-carousel',
        carousel: true
    })
}