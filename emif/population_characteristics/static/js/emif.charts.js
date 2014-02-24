/***
* This function will draw the graphs 
* Should provide an abstractoin to the API's

*/ 
/* This should allow generic components 
 * should decorate other class
*/ 

function Scale()
{
    this.getBins = function(){
    };

}

function Filters()
{
    this.getBins = function(){
    };
}

/** This class only works for documentation process
 ** Thus, you will know what kind of classes you have to implement.
 */ 
function RepresentData(divArg, dataArg)
{
    this.translateData = function(objects){
    };

    this.draw = function(div, dataset){
    };

}


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

            dataset = [[], 
                 
                 ];

            g.translateData(_data);
            g.draw('#pc_chart_place', dataset);
            

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
