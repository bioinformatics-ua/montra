function showExportMessage() {
    $('#exporting-message').fadeIn('fast');


    // Validation of quicksearch
    $('#quicksearch').submit(function() {

        var quick_search = $('#edit-search-block-form--3', $(this)).val().trim();

        if (!quick_search || quick_search.length == 0)
            return false;

        return true;
    });

    setTimeout(function() {
        $('#exporting-message').fadeOut('fast');
    }, 4000);
}

$(function() {
    refreshNotificationCenter();
});

function refreshNotificationCenter() {
    $('#notification_badge').hide();

    $.get("api/notifications", function(data) {
        console.log("Loading notification center");

        if (data.unread && data.unread != 0) {
            $('#notification_badge').text(data.unread);
            $('#notification_badge').show();
        }
        if (data.notifications) {
            resetNotificationCenter();
            for (var i = 0; i < data.notifications.length; i++) {
                insertNotification(data.notifications[i]);
            }

            if(data.notifications.length == 0){
                $('#notification_center').html('<center> <div class="notification">There\'s no new notifications.</div></center>'); 
            }
        }

    });
}

function resetNotificationCenter() {
    $('#notification_center').html('');
}

function insertNotification(notification) {

    var new_notification = '<hr /><table><tr id="not_id_' + notification.id + '" class="notification_line"><td><div class="notification';

    if (!notification.read) {
        new_notification += ' notification_unread ';
    }

    if (notification.href && notification.href != 'None') {
        new_notification += '" onclick="handleClick('+notification.id+', \'' + notification.href + '\');';

    }
    new_notification += '">' +
        notification.message + '<br /> <div class="clearfix"><div class="notification_origin pull-right">by ' + notification.origin + " at " + notification.createddate +
        '</div></div></div></td><td class="notification_options"><i title="';

    if (notification.read)
        new_notification += 'Mark as unread" class="muted ';
    else
        new_notification += 'Mark as read" class="';

    new_notification += 'markread fa fa-eye"></i><br /><br /><i title="Remove Notification" class="removenotification fa fa-times"></i> </td</tr></table>'

    $('#notification_center').append(new_notification);

    var removenot = $('#not_id_' + notification.id + ' .removenotification');
    var readnot = $('#not_id_' + notification.id + ' .markread');
    removenot.tooltip({
        container: 'body',
        placement: 'right'
    });
    readnot.tooltip({
        container: 'body',
        placement: 'right'
    });

    removenot.click(function() {
        markRemoved(notification.id)
    });
    readnot.click(function() {
        markRead(notification.id, null);
    });

}

function markRead(not_id, callback) {
    var readnot = $('#not_id_' + not_id + ' .markread');
    var value = readnot.hasClass('muted');

    $('.markread').tooltip('hide');
    $('.removenotification').tooltip('hide');

    $.post("api/readnotification", {
        notification: not_id,
        value: !value
    })
        .done(function(data) {
            if (data.success) {
                refreshNotificationCenter();

                if(callback != null){
                    callback();
                }
            }
        })
        .fail(function() {
            console.log("Failed marking as read notification");
        });
}

function markRemoved(not_id) {
    var removenot = $('#not_id_' + not_id + ' .removenotification');
    var readnot = $('#not_id_' + not_id + ' .markread');
    var value = readnot.hasClass('muted');

    $('.markread').tooltip('hide');
    $('.removenotification').tooltip('hide');

    var r = true;

    if (!value) {
        r = confirm("You are trying to delete a unread notification, are you sure?");
    }

    if (r) {
        $.post("api/removenotification", {
            notification: not_id,
            value: true
        })
            .done(function(data) {
                if (data.success) {
                    refreshNotificationCenter();
                }
            })
            .fail(function() {
                console.log("Failed removing notification");
            });
    }
}
// Mark as read on opening link
function handleClick(not_id, href){

    var readnot = $('#not_id_' + not_id + ' .markread');
    var value = readnot.hasClass('muted');   

    var callback = function(){ window.location.href = href; };
    if(!value){
        console.log('MARK AS READ')
        markRead(not_id, callback);
    }
    else 
        callback();

}

$('.dropdown-menu').on('click', function(e) {
    if ($(this).hasClass('dropdown-menu-form')) {
        e.stopPropagation();
    }
});