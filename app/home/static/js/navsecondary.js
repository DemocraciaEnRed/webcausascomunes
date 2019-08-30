$('.scrollTo').click(function() {
    var sectionActive = $('#nav-secondary .nav-link.active').attr('href')
    var sectionTo = $(this).attr('href');
    var scrollTo = $(sectionTo).offset().top - $('.nav-secondary').outerHeight() - $('#navbar').outerHeight();

    $('html, body').animate({
      scrollTop: scrollTo
    }, 1000);
});

var isMobile = false;
var scroller_anchor = $(".portada-seccion").offset().top + $(".portada-seccion").innerHeight() - $("#navbar").outerHeight();
var scrollItem = $("#nav-secondary");

function scrollHandler() {
    if ($(this).scrollTop() >= scroller_anchor && !scrollItem.hasClass('position-fixed') ) {    
        scrollItem.addClass('position-fixed');
    } else if ($(this).scrollTop() < scroller_anchor && scrollItem.hasClass('position-fixed')) {   
        scrollItem.removeClass('position-fixed');
    }
    setMenuItemActive();
}

function setMenuItemActive(){
    var scrollPos = $(document).scrollTop();
    var navHei =  $('#nav-secondary').outerHeight();
    var navbarHei = $('#navbar').outerHeight();
    $('#nav-secondary .nav-link').each(function () {
        var currLink = $(this);
        var refElement = $(currLink.attr("href"));
        var refElTop = refElement.position().top - navHei - navbarHei;
        if (refElTop <= scrollPos && refElTop + refElement.outerHeight() > scrollPos) {
            $('#nav-secondary .nav-link').removeClass("active");
            currLink.addClass("active");
            if (isMobile){
                //$('#nav-secondary').animate({scrollLeft: currLink.offset().left}, 200);
                // TODO add auto swipeable 
            }
        }
        else {
            currLink.removeClass("active");
        }
    });
}

function checkWidth() {
     if ($(window).width() <= 768) {
        isMobile = true; 
    } else {
        isMobile = false;
    }
}

$(document).ready(function(){
    $(window).scroll(scrollHandler);
    checkWidth();

    $(window).resize(function(){
        checkWidth()
    });
});
