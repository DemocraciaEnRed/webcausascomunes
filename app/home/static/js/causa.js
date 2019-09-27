// to top right away
if ( window.location.hash ) scroll(0,0);
// void some browsers issue
setTimeout( function() { scroll(0,0); }, 1);

function hashScroll() {
    if(window.location.hash) {
		console.log($(window.location.hash).offset().top, $("#navbar").innerHeight(), $("#nav-secondary").innerHeight())
        $('html, body').animate({
          scrollTop: $(window.location.hash).offset().top + 3 - $("#navbar").innerHeight() - $("#nav-secondary").innerHeight()
        }, 1000);
    }
}

/*$(window).resize(function(){
    header_hei = $('header').outerHeight(true)
    section_hei = $('.portada-seccion').outerHeight(true)
    $('.bgimg').height(header_hei + section_hei)
})*/

$(function(){
    $(window).resize()
	setTimeout(hashScroll, 500)
	// a veces 500ms no alcanza a esperar cargar
	setTimeout(hashScroll, 1000)
})