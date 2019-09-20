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
          scrollTop: $(window.location.hash).offset().top - $("#navbar").innerHeight()
        }, 1000);
    }
}

$(document).ready(function(){
    initBlueimp(hashScroll);
    
    $('.scrollTo').click(function(e) {
        e.preventDefault();
        var sectionTo = $(this).attr('href');
        $('html, body').animate({
          scrollTop: $(sectionTo).offset().top - ($("#navbar").innerHeight() - $("#navbarMenu").innerHeight())
        }, 1000);
    });
    
	var widthMedium = 768;
	var viewportWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
	var waitForIframe = setInterval(function(){
		if ($('.twitter-timeline-rendered').length){
			$('.twitter-timeline-rendered').css('height', viewportWidth < widthMedium ? '500px' : '90%')
			clearInterval(waitForIframe)
		}
	}, 700);
})
