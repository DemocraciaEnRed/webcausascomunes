var navbar_anchor = $("#navbar").innerHeight();
var navbar = $("#navbar");

function toggleNavbarFixed(){
    if ($(this).scrollTop() >= navbar_anchor && !navbar.hasClass('scrolling') ) {    
        navbar.addClass('scrolling');
    } else if ($(this).scrollTop() < navbar_anchor && navbar.hasClass('scrolling')) {   
        navbar.removeClass('scrolling');
    }
}

$(document).ready(function(){
    $( window ).scroll(toggleNavbarFixed);
    
    $('#navbarMenu').on('show.bs.collapse', function () {
        if ( $('#dropdown-novedades').hasClass('show') ) {
            $('#dropdown-novedades').dropdown('toggle');
        }
    })

    $('#dropdown-novedades').on('show.bs.dropdown', function () {
        $('#navbarMenu').collapse('hide');
    });
});
