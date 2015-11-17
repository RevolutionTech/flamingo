$(document).ready(function(){
    $('.entries').slick({
        slidesToShow: 3,
        variableWidth: true,
        autoplay: true,
        lazyLoad: 'ondemand'
    });
    Dropzone.options.dropzoneSubmitPhoto = {
        paramName: "image",
        maxFilesize: 2, // MB
        init: function() {
            this.on("queuecomplete", function(file) {
                // Refresh the page to see uploaded contents
                location.reload();
            });
        }
    };
});
