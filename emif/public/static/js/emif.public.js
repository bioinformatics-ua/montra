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
#*/

$(function(){
    var cbtns = $('.copy-button');

    cbtns.each(function (i){

      addClipboard(this);
    });

    $('.tooltippable').tooltip({'container': 'body'});
});

function addClipboard(element){
    if(hasFlash()){
    var base = $('#base_link').attr('href');

    $(element).attr('data-clipboard-text', base+$(element).data('clipboard-text'))
    var client = new ZeroClipboard($(element));
    } else {
        $(element).hide();
    }
}
function hasFlash(){
    try {
        if( new ActiveXObject('ShockwaveFlash.ShockwaveFlash') ) return true;
    } catch(e){
      if(navigator.mimeTypes ["application/x-shockwave-flash"] != undefined) return true;
    }
    return false;
}

function shareByEmail(url){
    var this_share = bootbox.dialog(
                    '<div style="margin: -10px -10px 10px -10px;" class="modal-header">'+
                    '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'+
                    '<h3>Send Private Link by Email</h3>'+
                    '</div>'+
                    'It is possible to send this private link to a group of emails. Below, please write the emails you want to send this private link to.<br /><br />'+
                    'It is possible to paste a list of comma separated emails.<br />'+
                    '<input type="text" data-role="tagsinput" class="emailsinput" placeholder="Add Emails">'+
                    '<div style="display: none;" id="salert'+url+'" class="alert">&nbsp;</div>',
        [{
                label: "Send",
                class: "btn-success",
                callback: function () {
                    var emails = $('.emailsinput').tagsinput('items');
                    var plid = url;
                    var salert = $('#salert'+url);

                    if(emails.length > 0){
                        salert.text('Sending emails, please wait');
                        salert.attr('class', 'alert alert-info');
                        salert.fadeIn('fast');

                        $.ajax({
                          type: 'POST',
                          url: 'api/plinkemails',
                          data: {
                            emails: emails,
                            plid: plid
                          },
                          success: function(data){
                            if(data.success == true){
                                salert.text('Emails sent successfully.');
                                salert.attr('class', 'alert alert-success');
                            } else {
                                salert.text('Emails couldn\'t be sent, please contact the administrator.');
                                salert.attr('class', 'alert alert-danger');
                            }
                            //this_share.modal('hide');
                          },
                          error: function(data){
                                salert.text('Emails couldn\'t be sent, please contact the administrator.');
                                salert.attr('class', 'alert alert-danger');
                          },
                          async:true
                        });
                    }
                    return false;
                }
        }],
        {
            onShow: function(){
                $('.emailsinput').tagsinput({
                  // Comma, Enter, Space
                  confirmKeys: [13, 44, 32]
                });
                $('.emailsinput').on('beforeItemAdd', function(event) {
                  var re = /([\w_\-.]+@[\w_\-.]+)/g;
                  var is_valid = re.test(event.item);

                  if(!is_valid)
                    event.cancel=true;
                  // event.cancel: set to true to prevent the item getting added
                });
            }
        }
    );
}
