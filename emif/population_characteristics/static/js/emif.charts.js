/**********************************************************************
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

***********************************************************************/

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
function RepresentData(wrapper)
{

    this.wrapper = wrapper;


    this.translateData = function(objects){
        return this.wrapper.translateData(objects);
    };

    this.draw = function(div, dataset){
        return this.wrapper.draw(div, dataset);
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

            g = new GraphicChartC3D3();
            w_g = new RepresentData(g);

            g.div = div;
            g.dataValues = data;
            g.init(div, data);

            dataset = [[],

                 ];
            w_g.translateData(_data);


            w_g.draw('#pc_chart_place', dataset);


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
