/**********************************************************************
# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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
***********************************************************************/



function getFingerprintID_new(){
  return global_fingerprint_id;
};


$(document).ready(
    function(){

        var result = {}

        $.ajax({
          dataType: "json",
          url: "population/jerboafiles/"+getFingerprintID_new()+"/",
          async: false,
          data: { publickey: global_public_key, result: result },
          type: "POST",

          success: function (data){result=data;}
        });
        result.conf.forEach(function(d){
            var context = $('<tr>').prependTo('#jerboafiles');
            var node = $('<td colspan="3"/>')
                        .append($('<span/>').html("<p>File name: " + d.file_name
                            + "</p><p>Description: " + d.comments
                            + "</p><p>Last update: " + d.latest_date ));
            context.append(node);
            //node.appendTo(context);
        });


    }
);



/*jslint unparam: true, regexp: true */
/*global window, $ */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$(function () {

    'use strict';
    var csrftoken = $.cookie('cssrftoken');
    // Change this to the location of your server-side upload handler:
    var url = 'population/jerboaupload/'+getFingerprintID_new()+"/",
        uploadButton = $('<button/>')
            .addClass('btn btn-primary')
            .prop('disabled', true)
            .text('Processing...')
            .on('click', function () {
                var $this = $(this),
                    data = $this.data();
                $this
                    .off('click')
                    .text('Abort')
                    .on('click', function () {
                        $this.remove();
                        data.abort();
                    });
                data.submit().always(function () {
                    $this.remove();
                });
            });
    $('#jerboaupload').fileupload({
        url: url,
        crossDomain: true,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        dataType: 'json',
        autoUpload: false,
        acceptFileTypes: /(\.|\/)(tsv|txt)$/i,
        maxFileSize: 20000000, // 20 MB
        // Enable image resizing, except for Android and Opera,
        // which actually support image resizing, but fail to
        // send Blob objects via XHR requests:
        disableImageResize: /Android(?!.*Chrome)|Opera/
            .test(window.navigator.userAgent),
        previewMaxWidth: 100,
        previewMaxHeight: 100,
        previewCrop: true
    }).on('fileuploadadd', function (e, data) {
        console.log('File Upload - fileuploadadd');
        data.context = $('<tr>').prependTo('#jerboafiles');
        $.each(data.files, function (index, file) {
            var node = $('<td>').text(file.name);

            node.appendTo(data.context);

            var node2 = $('<td class="fmessage">');

            node2.appendTo(data.context);

            if (!index) {
                uploadButton.clone(true).data(data).appendTo(data.context).wrap('<td style="width: 100px;">');
            }

        });
    }).on('fileuploadprocessalways', function (e, data) {
        console.log('File Upload - fileuploadprocessalways');
        var index = data.index,
            file = data.files[index],
            node = $(data.context.find('.fmessage'));
        if (file.preview) {
            node
                .prepend(file.preview);
        }
        if (file.error) {
            node.text(file.error);
        }
        if (index + 1 === data.files.length) {
            data.context.find('button')
                .text('Upload')
                .prop('disabled', !!data.files.error);
        }
    }).on('fileuploadprogressall', function (e, data) {
        console.log('File Upload - progress all');
        var progress = parseInt(data.loaded / data.total * 100, 10);

        bootbox.dialog("<h3>Uploading, please wait.</h3>");

        $('#progress .progress-bar').css(
            'width',
            progress + '%'
        );
    }).on('fileuploaddone', function (e, data) {
        console.log('File Upload - done');
        $.each(data.result.files, function (index, file) {
            var link = $('<a>')
                .attr('target', '_blank')
                .prop('href', file.url);
            $(data.context.children()[index])
                .wrap(link);


            // Trigger the charts
            var url = document.URL;
            if(url.indexOf('pc/') == -1)
                url = url + "pc/"
            window.location.assign(url);


        });
    }).on('fileuploadfail', function (e, data) {
        $.each(data.result.files, function (index, file) {
            var error = $('<span/>').text(file.error);
            $(data.context.children()[index])
                .append('<br>')
                .append(error);
        });
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');

    $('#fileupload_hook').bind('change', function (e) {
        $('#jerboaupload').fileupload('add', {
            fileInput: $(this)
        });
    });
});
