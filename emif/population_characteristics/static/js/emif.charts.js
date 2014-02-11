/***
* This function will draw the graphs 
* Should provide an abstractoin to the API's

*/ 






 (function( $ )
 {

   
    var methods = {
        init : function( options, api ) {

            var self = this;
            

        },
        draw : function( options ) {
            
        },

    };

    $.fn.graphicChart = function(method) {
        // Method calling logic
        if ( methods[method] ) {
        return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
        return methods.init.apply( this, arguments );
        } else {
        $.error( 'Method ' + method + ' does not exist on jQuery.graphicChart' );
        }
        return this;
    };
}( jQuery ));


