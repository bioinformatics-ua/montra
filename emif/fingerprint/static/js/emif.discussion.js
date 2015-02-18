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
*/
function bindPostCommentHandler(firstname, lastname, username, owners, fingerprint_id, fingerprint_name) {
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

                            notify_owner(owners, $('#id_comment').val(), username, fingerprint_id, fingerprint_name);
                        }
                        else{
                            $('#newComments').prepend('<blockquote><p style="font-size: 16px">' + $('#id_comment').val() + '</p><small>' + firstname + ' ' + lastname +' posted a while ago</small></blockquote>').hide().fadeIn(1000);

                            notify_owner(owners, $('#id_comment').val(), firstname + ' ' + lastname, fingerprint_id, fingerprint_name);
                        }
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        bootbox.alert('Your comment was unable to be posted at this time.  We apologise for the inconvenience.');
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

function notify_owner(owners, comment, user_commented, fingerprint_id, fingerprint_name){
    var owners_array = owners.replace(/\s{2,}/g, ' ').replace(/\//g,'').split(' ');

    // For each owner of this database (since it can be shared)
    for(var i=0;i < owners_array.length;i++){
        //var valid_email = /([\w_\-.]+@[\w_\-.]+)/g;
        //var is_valid = valid_email.test(owners_array[i]);
        // If email is valid, send email warning about comment
        //if (is_valid){
            console.log('Email is valid: ' + owners_array[i]);

                $.post( "api/notify_owner",
                {
                    fingerprint_id: fingerprint_id,
                    fingerprint_name: fingerprint_name,
                    owner: owners_array[i],
                    comment: comment,
                    user_commented: user_commented
                }
                  ).done(function() {
                    console.log('Sent notification to owner about comment.');
                  })
                  .fail(function() {
                    console.log('Error sending notification to owner about comment.')
                  });

        // Otherwise warn about username not being a valid email
        //} else {
        //    console.log('Email '+owners_array[i]+" is invalid.")
        //}
    }

}
