$('.scrollTo').click(function() {
    var sectionActive = $('#nav-secondary .nav-link.active').attr('href')
    var sectionTo = $(this).attr('href');
    var scrollTo = $(sectionTo).offset().top;

    if (isMobile){
        //si estamos arriba del tdo o en "de qué se trata" el offset top
        //no cuenta con que el body pierde el height cuando el nav se convierte en fixed
        if (!sectionActive || sectionActive=='#definicion')
            scrollTo -= $('.nav-secondary').height()
        //offsetear el anchor de a donde scrolleamos con el height del nav
        if (sectionTo != '#definicion')
            scrollTo -= $('.nav-secondary').height() - 1;
    }

    $('html, body').animate({
      scrollTop: scrollTo
    }, 500);
});

var isMobile = false;
var scroller_anchor = $(".portada-seccion").offset().top + $(".portada-seccion").innerHeight();
var scrollItem = $("#nav-secondary");

checkScroll();

$(window).resize(function(){
    checkScroll()
});

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
    var navHei =  $('.nav-secondary').height();
    $('#nav-secondary .nav-link').each(function () {
        var currLink = $(this);
        var refElement = $(currLink.attr("href"));
        var refElTop = refElement.position().top - navHei;
        if (refElTop <= scrollPos && refElTop + refElement.outerHeight() > scrollPos) {
            $('#nav-secondary .nav-link').removeClass("active");
            currLink.addClass("active");
        }
        else {
            currLink.removeClass("active");
        }
    });
}

function checkScroll() {
    if ($(window).width() <= 768 && !isMobile) {
        isMobile = true;
        $(window).scroll(scrollHandler);
    } else if ($(window).width() > 768 && isMobile) {
        isMobile = false;
        $(window).off("scroll", scrollHandler);
        scrollItem.removeClass('position-fixed');
    }
}


// TODO: comportamiento swipe horizontal para mobile
