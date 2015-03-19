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

(function ( $ ) {
    $.fn.errornavigator = function( options ) {
         var self = this;
         var errors = [];
         var index = 0;

         var settings = $.extend({
            delete_color: "#000000"
        }, options );

         var public_functions = {
            addError  : function(error){
                errors.push(error);

                public_functions.updatePager();
            },
            nextError : function(){

                if(index < errors.length){
                    index++;

                    // Slide to correct id
                    document.getElementById(errors[index]).scrollIntoView(true);
                    // Offset up(because of navbar)
                    window.scrollBy(0,-50);

                    public_functions.updatePager();

                    if(index != 0)
                        $("#prevError").attr("disabled", false);
                }

                if(index == errors.length-1){
                    $("#nextError").attr("disabled", true);
                }

            },
            prevError : function(){
                if(index > 0){
                    index--;

                    // Slide to correct id
                    document.getElementById(errors[index]).scrollIntoView(true);
                    // Offset up(because of navbar)
                    window.scrollBy(0,-50);

                    public_functions.updatePager();

                    $("#nextError").attr("disabled", false);
                }

                if(index == 0){
                    $("#prevError").attr("disabled", true);
                }
            },
            reset   : function(){
                index = -1;
                errors= [];
            },
            showErrorPager : function(){
                self.fadeIn('fast');

                self.attr("style", "z-index: 2000; position:fixed; bottom:20px; right: 20px;");

                var content ='<div class="btn-group"><button id="prevError" class="btn btn-danger"><i class="icon-arrow-up"></i></button>'+
                             '<span id="messageError" class="btn btn-danger disabled">Errors: -/-</span>'+
                             '<button id="nextError" class="btn btn-danger"><i class="icon-arrow-down"></i></button>'+
                             '</div>';

                self.html(content);
                 $('#prevError').click(function(){
                                console.log("prev error");

                    public_functions.prevError();

                 });
                 $('#nextError').click(function(){
                                console.log("next error");

                    public_functions.nextError();

                 });

                $("#prevError").attr("disabled", true);

                if(errors.length == 1){
                    $("#nextError").attr("disabled", true);
                }
            },
            updatePager : function(){
                $('#messageError').text("Errors: "+(index+1)+"/"+errors.length);
            },
            hideErrorPage : function(){
                self.fadeOut('fast');
            }
         };

        return public_functions;
    };
}( jQuery ));
