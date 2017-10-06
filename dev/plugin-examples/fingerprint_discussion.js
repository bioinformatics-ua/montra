confs = {
    icon: '<i class="fa fa-comment"></i>',
    name: "Discussion"
};
plugin = function(sdk) {
    sdk.html('Loading...');
    sdk.refresh();
    var context = sdk.container();
    var getComment = function(comment){
        return '<div class="comment">\
            <blockquote>\
                <p style="font-size: 16px">' + comment.comment + '</p>\
                <small>' + comment['user_name'] + ' posted on ' + comment['submit_date'] + '</small>\
            </blockquote>\
        </div>';
    }
    var base = function(data) {
        var tmp = '<div class="span8 offset2">';
        if (data.length == 0) {
            tmp += '<center><p>No comments yet.</p></center>';
        } else {
            tmp += '<center><span class="comments_total">' + data.length + '</span> comments</center>';
        }

        tmp += '<div class="clearfix span12 comment_form">\
                    <fieldset>\
                        <textarea rows="5" name="comment" class="id_comment span12" placeholder="Insert your comment or question here..." autofocus></textarea>\
                        <button style="margin-left:0px;" class="submit_button span12 btn btn-primary" type="submit"  data-loading-text="Sending comment...">Post comment</button>\
                    </fieldset>\
                </div>';

        tmp += '<div style="margin-top:10px" class="clearfix span12"><div class="newComments"></div>';

        for (var i = 0; i < data.length; i++) {
            tmp += getComment(data[i]);
        }

        tmp += '</div></div>';

        return tmp;
    };

    var fp = FingerprintProxy.getInstance();
    var store = fp.getStore();

    store.getComments().then(function(response) {
        sdk.html(base(response.comments));
        sdk.refresh();
        $('.submit_button', context).click(function() {
            var comment = $('.id_comment', context).val();

            if (comment && comment.trim().length > 20) {
                store.putComment({
                    comment: comment
                }).then(function(response) {
                    console.log(response);
                    $('.newComments', context).append(getComment(response.comment));
                }).catch(function(ex){
                    bootbox.alert("Unable to add new comment, please try again.");
                });
            } else {
                bootbox.alert("A comment must have more then 20 characters.");
            }

        });
    });
};
