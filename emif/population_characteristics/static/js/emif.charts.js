/***
* This function will draw the graphs 
* Should provide an abstractoin to the API's

*/ 
/* This should allow generic components 
 * should decorate other class
*/ 

 (function( $ )
 {

    var div='';
    var data='';
   
    var methods = {
        init : function( options, _div, _data ) {

            var self = this;
            var div = _div;
            var data = _data;

        },
        drawBarChart : function( options, _div, _data ) {
            console.log('who is this: ' + this);
            console.log('who is this: ' + self);
            console.log(div);
            console.log(data);
            g = new GraphicChartD3();

            g.div = div;
            g.dataValues = data;
            g.init(div, data);

            console.log('This is the data that we got: ' +  _data);

            dataset = [[{'xvalue':'2000', 'yvalue':200}, 
                  {'xvalue':'2001', 'yvalue':300},
                  {'xvalue':'2002', 'yvalue':.356}], 
                 
                 ];

            g.translateData(_data);
            g.draw('#d3test', dataset);
            

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



$(document).ready(
    function(){




    }
);
