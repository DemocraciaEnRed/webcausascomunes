//https://github.com/blueimp/Gallery
function initBlueimp(onopened){
    blueimp.Gallery(document.getElementById('links').getElementsByTagName('a'), {
        container: '#blueimp-gallery-carousel',
        carousel: true,
        onopened: onopened || null
    })
}

$(document).ready(function(){
    initBlueimp();
})
