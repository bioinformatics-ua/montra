/*
 * Author: Ricardo Ribeiro <ribeiro.r@ua.pt> 
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