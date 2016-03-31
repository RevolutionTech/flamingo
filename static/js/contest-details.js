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
        variableWidth: true,
        autoplay: true,
        lazyLoad: 'ondemand'
    });

    function showErrorModal(status_text, response_text) {
        $('#error-modal > .error-type').text(status_text);
        $('#error-modal > .error-message').text(response_text);
        $('#error-modal').foundation('reveal', 'open');
    }

    function error_occurred_during_uploading(files) {
        var error_occurred = false;
        $.each(files, function(i, file) {
            if (file.status === Dropzone.ERROR) {
                error_occurred = true;
                return false;
            }
        });
        return error_occurred;
    }
    Dropzone.options.dropzoneSubmitPhoto = {
        paramName: "image",
        maxFilesize: 2, // MB
        init: function() {
            this.on("error", function(file, errorMessage, serverResponse) {
                if (typeof serverResponse === 'undefined') {
                    showErrorModal("Upload Error", errorMessage);
                } else {
                    showErrorModal(serverResponse['status'] + " " + serverResponse['statusText'], errorMessage);
                }
            });
            this.on("queuecomplete", function() {
                // Refresh the page to see uploaded contents, if no errors occurred
                if (!error_occurred_during_uploading(this.files)) {
                    location.reload();
                }
            });
        }
    };

    $('.entry .button').click(function() {
        // Ignore pressing this button if it's already selected
        // (this saves making an outgoing request)
        if (!$(this).hasClass('secondary')) return;

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

        // Find voting buttons
        var this_button = $(this);
        var other_voting_button = $(this).parents('.row').find('.' + other_vote_type + '-button');

        // Make the request
        var entry_vote_count = $(this).parents('.row').find('.entry-vote-count');
        jQuery.post(vote_url, {})
            .done(function(resp) {
                // Highlight selected voting button
                this_button.removeClass('secondary');
                if (vote_type === 'upvote') {
                    other_voting_button.removeClass('alert');
                    this_button.addClass('success');
                } else if (vote_type === 'downvote') {
                    other_voting_button.removeClass('success');
                    this_button.addClass('alert');
                }

                // Unhighlight other voting button
                other_voting_button.addClass('secondary');

                // Update voting count
                entry_vote_count.text(resp['vote_count']);
            })
            .fail(function(resp) {
                // Show the error from the server
                showErrorModal(resp['status'] + " " + resp['statusText'], resp['responseText']);
            });
    });
});
