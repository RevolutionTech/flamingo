$(document).ready(function(){
    'use strict';

    // CSRF
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

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

    $('.entry .button').click(function() {
        // Ignore pressing this button if it's already selected
        // (this saves making an outgoing request)
        if (!$(this).hasClass('disabled')) return;

        // Determine vote_url
        var entry_id = $(this).parents('.entry').attr('id');
        var vote_type, other_vote_type;
        if ($(this).hasClass('upvote-button')) {
            vote_type = 'upvote';
            other_vote_type = 'downvote';
        } else if ($(this).hasClass('downvote-button')) {
            vote_type = 'downvote';
            other_vote_type = 'upvote';
        } else {
            throw "Unknown voting button.";
        }
        var vote_url = "/contest/details/" + contest_slug + "/entry/" + entry_id + "/" + vote_type + "/";

        // Disable other voting button
        $(this).parents('.row').find('.' + other_vote_type + '-button').addClass('disabled');

        // Enable selected voting button
        $(this).removeClass('disabled');

        // Make the request and update voting count
        var entry_vote_count = $(this).parents('.row').find('.entry-vote-count');
        jQuery.post(vote_url, {}, function(resp) {
            entry_vote_count.text(resp['vote_count']);
        });
    });
});
