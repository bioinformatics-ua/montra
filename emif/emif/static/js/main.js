/*
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
*/
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

    handleWizards();
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

function handleWizards(){
    $.get("api/wizards", function(data) {
        console.log("Loading wizards, if any");
        wizards = data.wizards;
        wizards_len = wizards.length;
        if (wizards && wizards_len != 0) {
            line = "";

            for(var i=0;i<wizards_len;i++){
                line += '<tr>\
                            <td>'+wizards[i].name+'</td>\
                            <td class="pull-center">\
                                <input type="radio" name="'+wizards[i].id+'" value="0" checked />\
                            </td>\
                            <td class="pull-center"><input type="radio" name="'+wizards[i].id+'" value="1" />\
                            </td>\
                        </tr>';
            }

            bootbox.dialog('<div class="modal-header">\
                                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
                                <h3>New questionnaire types</h3>\
                            </div>\
                            <div class="medium-margin">\
                                <p>New questionnaire types have been created. Below it is possible to add them to the user preferences.</p>\
                                <form id="wizard_form">\
                                    <table class="table">\
                                        <thead>\
                                        <tr>\
                                            <th>Questionnaire Type</th>\
                                            <th class="pull-center">Ignore</th>\
                                            <th class="pull-center">Interested</th>\
                                        </tr>\
                                        </thead>\
                                        <tbody>\
                                        '+line+'</tbody>\
                                    </table>\
                                </form>\
                            </div>', [{
                "label" : "Save new interests",
                "class" : "btn-success",
                "callback": function() {
                    $.post('api/wizards', $('#wizard_form').serialize())
                        .done(function(data) {
                            console.log(data.success);
                        })
                        .fail(function(data) {
                            bootbox.alert('Could not save preferences for new questionnary types, please try again. If the problem persists contact the administrator.')
                        })
                }
            }]);
        }

    });
}

$(function() {
    refreshNotificationCenter();

    $('[data-clamp]').each(function () {
        var elem = $(this);
        var parentPanel = elem.data('clamp');

        var resizeFn = function () {
            var sideBarNavWidth = $(parentPanel).width() - parseInt(elem.css('paddingLeft')) - parseInt(elem.css('paddingRight')) - parseInt(elem.css('marginLeft')) - parseInt(elem.css('marginRight')) - parseInt(elem.css('borderLeftWidth')) - parseInt(elem.css('borderRightWidth'));
            elem.css('width', sideBarNavWidth);
        };

        resizeFn();
        $(window).resize(resizeFn);
    });
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

function askForAnswer(answer){
    var this_share = bootbox.dialog(
                    '<div style="margin: -10px -10px 10px -10px;" class="modal-header">'+
                    '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'+
                    '<h3>Request answer</h3>'+
                    '</div>'+
                    "This question doesn't have an answer, do you want to request the owner of this database to answer this question ?<br/><br/>"+
                    '<strong>Note:</strong> The database owner will be notified of this request.<br /><br />'+
                    '<textarea rows="4" id="request_comment'+answer+'" class="span5" type="text" placeholder="Rationale behind this answer request (optional)">',
        [{
                label: "Request",
                class: "btn-success",
                callback: function () {
                    var request_comment = $('#request_comment'+answer).val();

                  $.post("api/requestanswer", {
                        fingerprint_id: global_fingerprint_id,
                        question: answer,
                        comment : request_comment
                      })
                      .done(function(response) {
                        if(response.success){
                            bootbox.alert('A request for this answer was sent to the owner of the database.');
                        } else {
                            bootbox.alert("There was a problem requesting this answer. please try again. If the problem persists contact the database owner.")
                        }
                      })
                      .fail(function(){
                        console.log('Failed sending request for answer');
                      });
                }
        }]
    );
}
