$(function(){
    $('.notification_detail').click(function(){
        var link = $(this).parent().data('link');
        var ident = $(this).parent().data('ident');
        if(link && ident){
            var readindicator = $(this).parent().find('.notification_read');

            if(readindicator.hasClass('muted')){
                readindicator.removeClass('muted');
            } else {
                readindicator.addClass('muted');
            }

            handleClick(ident, link);

        }
    });

    $('.notification_delete').click(function(){
        var self = $(this);
        var ident = self.parent().parent().data('ident');
        var read = self.parent().find('.notification_read').hasClass('muted');

        var r = true;
        if (!read) {
            r = confirm("You are trying to delete a unread notification, are you sure?");
        }

        if (r) {
            $.post("api/removenotification", {
                notification: ident,
                value: true
            })
                .done(function(data) {
                    if (data.success) {
                        location.reload(true);
                    }
                })
                .fail(function() {
                    console.log("Failed removing notification");
                });
        }
    });
    $('.notification_read').click(function(){
        var self = $(this);
        var ident = self.parent().parent().data('ident');
        var value = self.hasClass('muted');


        $.post("api/readnotification", {
            notification: ident,
            value: !value
        })
            .done(function(data) {
                if (data.success) {
                    location.reload(true);
                }
            })
            .fail(function() {
                console.log("Failed marking as read notification");
            });       
    });
});