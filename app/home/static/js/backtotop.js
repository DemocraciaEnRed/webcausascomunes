$(document).ready(function(){
    $(window).scroll(function() {
        if ($(this).scrollTop() > 200) {
            $('.backtotop').fadeIn(200);
        } else {
            $('.backtotop').fadeOut(200);
        }
    });
    
    $('.backtotop').click(function(e) {
        e.preventDefault();        
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    })
});