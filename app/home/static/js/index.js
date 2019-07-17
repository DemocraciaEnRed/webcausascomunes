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
    document.getElementById('links').onclick = function(event) {
        event = event || window.event
        var target = event.target || event.srcElement,
            link = target.src ? target.parentNode : target,
            options = {
                index: link, event: event,
                onslide: function (index, slide) {
                    self = this;
                    var initializeAdditional = function (index, data, klass, self) {
                        var text = self.list[index].getAttribute(data),
                        node = self.container.find(klass);
                        node.empty();
                        if (text) {
                            node[0].appendChild(document.createTextNode(text));
                        }
                    };
                    initializeAdditional(index, 'data-description', '.description', self);
                }
            },
            links = this.getElementsByTagName('a')
        blueimp.Gallery(links, options)
    }


    blueimp.Gallery(document.getElementById('links').getElementsByTagName('a'), {
        container: '#blueimp-gallery-carousel',
        carousel: true
    })
}