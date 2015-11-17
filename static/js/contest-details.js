$(document).ready(function(){
    $('.entries').slick({
        slidesToShow: 3,
        variableWidth: true,
        autoplay: true,
        lazyLoad: 'ondemand'
    });
    Dropzone.options.dropzoneSubmitPhoto = {
        paramName: "image",
        maxFilesize: 2 // MB
    };
});
