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







/********************************************************
**************** Document Manager - Uploads, etc 
*********************************************************/


/* JQuery Plugin for Population Characteristics */
 
 
 (function( $ )
 {


    function exampleData() {
      return  [ 
         {
           key: "Cumulative Return",
           values: [
             { 
               "label" : "2000" ,
               "value" : 30000
             } , 
             { 
               "label" : "2001" , 
               "value" : 35000
             } , 
             { 
               "label" : "2002" , 
               "value" : 25000
             } , 
             { 
               "label" : "2003" , 
               "value" : 29000
             } , 
             { 
               "label" : "2004" ,
               "value" : 31000
             } , 
             { 
               "label" : "2005" , 
               "value" : 35000
             } , 
             { 
               "label" : "2006" , 
               "value" : 40000
             } , 
             { 
               "label" : "2007" , 
               "value" : 60000
             }
           ]
         }
       ];
     };


    var methods = {
        init : function( options ) { 
            console.log("init");
            console.log(options);
            $(".chart_pc" ).on(eventToCatch, options.handle_type_chart);
        },
        draw : function( options ) {
            
            nv.addGraph(function() {
               var chart = nv.models.discreteBarChart()
                   .x(function(d) { return d.label })
                   .y(function(d) { return d.value })
                   .staggerLabels(true)
                   .tooltips(true)
                   .showValues(true)
             
               d3.select('#chart svg')
                   .datum(exampleData())
                 .transition().duration(500)
                   .call(chart);
             
               nv.utils.windowResize(chart.update);
             
               return chart;
             });
             
            $("#chart h1").append("Number of patients yearly")
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
