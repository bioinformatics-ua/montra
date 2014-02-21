/**********************************************************************
# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
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

var eventToCatch = 'click';

/* Population Characteristics */


function FingerprintPCAPI()
{

    this.getGenericFilter = function()
    {

        var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/genericfilter/Var",
          async: false,
          data: result,
          success: function (data){result=data;},
        });
        return result;

    };
};


function PopulationCharacteristics (type) 
{
    this.handle_type_chart = function(e)     {
        e.preventDefault();
        e.stopPropagation();
        console.log("Type of graph is: "); 

    };


    this.handle_data = function(data){
                    


    };


};




$(document).ready(
    function(){

        var result = {}

        $.ajax({
          dataType: "json",
          url: "docsmanager/docfiles/"+getFingerprintID_new()+"/",
          async: false,
          data: result,
          success: function (data){result=data;},
        });
        console.log(result);
        result.conf.forEach(function(d){
            var context = $('<tr>').appendTo('#files');
            var node = $('<td/>')
                        .append($('<span/>').html("<p>File name: " + d.file_name
                            + "</p><p>Description: " + d.comments 
                            + "</p><p>Last update: " + d.latest_date ));
            context.append(node);
            //node.appendTo(context);    
        });
        

    }
);


/********************************************************
**************** Document Manager - Uploads, etc 
*********************************************************/


/* JQuery Plugin for Population Characteristics */
 
 
 (function( $ )
 {



    var methods = {
        init : function( options ) { 
            console.log("init");
            console.log(options);
            $(".chart_pc" ).on(eventToCatch, options.handle_type_chart);
        },
        draw : function( options ) {
            
           
        },
        
    };

    $.fn.populationCharts = function(method) {
        // Method calling logic
        if ( methods[method] ) {
        return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
        return methods.init.apply( this, arguments );
        } else {
        $.error( 'Method ' + method + ' does not exist on jQuery.populationCharts' );
        }
        return this;
    };
}( jQuery ));

$(document).ready(
    function(){

        var pc = new PopulationCharacteristics("pc");

        $("#populationcharacteristics").populationCharts(pc);
        $("#populationcharacteristics").populationCharts('draw', pc);    
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
    var csrftoken = $.cookie('csrftoken');
    // Change this to the location of your server-side upload handler:
    var url2 = 'docsmanager/uploadfile/'+getFingerprintID_new()+"/",
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
    $('#fileupload').fileupload({
        url: url2,
        crossDomain: true,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        dataType: 'json',
        autoUpload: false,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png|pdf|docx|xls|doc|docx|tsv|txt)$/i,
        maxFileSize: 5000000, // 5 MB
        // Enable image resizing, except for Android and Opera,
        // which actually support image resizing, but fail to
        // send Blob objects via XHR requests:
        disableImageResize: /Android(?!.*Chrome)|Opera/
            .test(window.navigator.userAgent),
        previewMaxWidth: 100,
        previewMaxHeight: 100,
        previewCrop: true
    }).on('fileuploadadd', function (e, data) {
        data.context = $('<tr><td><div class="span3"/>').appendTo('#files');
        $.each(data.files, function (index, file) {
            var node = $('<p/>')
                    .append($('<span/>').text(file.name));
            if (!index) {
                node
                    .append('<br>')
                    .append(uploadButton.clone(true).data(data));
            }
            node.appendTo(data.context);
        });
    }).on('fileuploadprocessalways', function (e, data) {
        var index = data.index,
            file = data.files[index],
            node = $(data.context.children()[index]);
        if (file.preview) {
            node
                .prepend('<br>')
                .prepend(file.preview);
        }
        if (file.error) {
            node
                .append('<br>')
                .append(file.error);
        }
        if (index + 1 === data.files.length) {
            data.context.find('button')
                .text('Upload')
                .prop('disabled', !!data.files.error);
        }
    }).on('fileuploadprogressall', function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progress .progress-bar').css(
            'width',
            progress + '%'
        );
    }).on('fileuploaddone', function (e, data) {
        $.each(data.result.files, function (index, file) {
            var link = $('<a>')
                .attr('target', '_blank')
                .prop('href', file.url);
            $(data.context.children()[index])
                .wrap(link);
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
});