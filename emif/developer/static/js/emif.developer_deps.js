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
function hasFlash(){
    try {
        if( new ActiveXObject('ShockwaveFlash.ShockwaveFlash') ) return true;
    } catch(e){
      if(navigator.mimeTypes ["application/x-shockwave-flash"] != undefined) return true;
    }
    return false;
}

$(function(){
    $('#deps').dataTable({
        "oLanguage": {
            "sEmptyTable": "No version dependencies found"
        }
    });

    $('#version-details').submit(function(event){
        var files = $('#depuploader')[0].files;

        if(files.length == 0){
            event.preventDefault();
            event.stopPropagation();

            bootbox.confirm('You must choose files to be uploaded first!');

            return false;
        }

    });
    $('.deletedep').click(function(event){
        var self = $(this);

        var filename = self.data('filename');
        var pluginversion = self.data('pluginversion');

        bootbox.confirm('Are you sure you want to delete \''+filename+'\'', function(result){
            if(result === true){
                $.post('developer/deletedep/', {
                    filename: filename,
                    pluginversion: pluginversion
                })
                .done(function(result) {
                    if(result.success){
                        self.closest('tr').remove();
                    }
                    else{
                        bootbox.alert("Couldn't remove the dependency.");
                    }

                })
                .fail(function() {
                    bootbox.alert("Couldn't remove the dependency.");
                });
            }
        });
    });
    if(hasFlash())
        $('.copy-button').each(function (i){
            new ZeroClipboard($(this));
        });
    else
        $('.copy-button').hide();

$(document).on('change', '.btn-file :file', function() {
  var input = $(this),
      numFiles = input.get(0).files ? input.get(0).files.length : 1,
      label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
  input.trigger('fileselect', [numFiles, label]);
});

$(document).ready( function() {
    $('.btn-file :file').on('fileselect', function(event, numFiles, label) {

        var input = $(this).parents('.btn-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;

        if( input.length ) {
            input.val(log);
        } else {
            if( log ) alert(log);
        }

    });
});
});
