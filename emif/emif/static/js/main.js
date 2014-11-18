/**
 * Hack in support for Function.name for browsers that don't support it.
 * IE, I'm looking at you.
**/
if (Function.prototype.name === undefined && Object.defineProperty !== undefined) {
    Object.defineProperty(Function.prototype, 'name', {
        get: function() {
            var funcNameRegex = /function\s([^(]{1,})\(/;
            var results = (funcNameRegex).exec((this).toString());
            return (results && results.length > 1) ? results[1].trim() : "";
        },
        set: function(value) {}
    });
}

var MAX_RESULTS = 10;

function showExportMessage(){
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
var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    var i=0;
    $.each(strs, function(i, str) {
      if (substrRegex.test(str.query)) {
        // the typeahead jQuery plugin expects suggestions to a
        // JavaScript object, refer to typeahead docs for more info
        matches.push({ value: str.query });
      }

    });

    cb(matches.slice(0, MAX_RESULTS));
  };
};

$(function(){
    if ($(".search-query").length > 0){
        $('.search-query').canclear();
    }

    handleQuickSearch();
});

function handleQuickSearch(){
 $( ".search-query" ).autocomplete({
source: "api/searchsuggestions",
minLength: 2,
open: function() {
$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
},
close: function() {
$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
}
});
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
            $('#notification_env').css('color', 'black');
            $('#notification_badge').show();
        } else {
            $('#notification_env').css('color', 'grey');
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
        notification.message + '<br /> <div class="clearfix"><div class="notification_origin"><i class="fa fa-user"></i> ' + notification.origin + " at " + notification.createddate +
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
