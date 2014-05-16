function bindPostCommentHandler(firstname, lastname, username) {
    $('#comment_form input.submit-preview').remove();

    $('#comment_form').submit(function() {
        if ($.trim($('#id_comment').val())){
            $('#submit_button').button('loading');
            $.ajax({
                type: "POST",
                data: $('#comment_form').serialize(),
                url: "comments/post/",
                cache: false,
                dataType: "html",
                success: function(html, textStatus) {
                    var total = parseInt($('#comments_total').html()) + 1;
                        //Update total comments
                        $('#comments_total').html(total);
                        $('#submit_button').button('reset');
                        $('#comment_form').hide();
                        $('#fillForm').hide();
                        $('#commentInserted').fadeIn(1000);
                        //Manually insert previous inserted comment
                        if (!firstname.trim() && !lastname.trim()){
                            $('#newComments').prepend('<blockquote><p style="font-size: 16px">' + $('#id_comment').val() + '</p><small>' + username +' posted a while ago</small></blockquote>').hide().fadeIn(1000);
                        }
                        else{
                            $('#newComments').prepend('<blockquote><p style="font-size: 16px">' + $('#id_comment').val() + '</p><small>' + firstname + ' ' + lastname +' posted a while ago</small></blockquote>').hide().fadeIn(1000);
                        }
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        alert('Your comment was unable to be posted at this time.  We apologise for the inconvenience.');
                        $('#submit_button').button('reset');
                        $('#fillForm').hide();

                    }
                });
}
else{
    $('#fillForm').slideDown();
    $('#id_comment').focus();
}
return false;
});
}