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
    $('#nav-secondary .nav-link').each(function () {
        var currLink = $(this);
        var refElement = $(currLink.attr("href"));
        if (refElement.position().top <= scrollPos && refElement.position().top + refElement.outerHeight() > scrollPos) {
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
