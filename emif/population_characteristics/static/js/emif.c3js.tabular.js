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

(function ( $ ) {

    var __row_length;
    var __col_map;

    var __renderHeaderRows = function(config){
        var tmp = [];

        var data = config.data;
        var x_var = data.x;
        var columns = data.columns;
        var col_length = columns.length;
        for(var i=0;i<col_length;i++){
            var column = columns[i][0];
            if(column != 'x' && columns[i].length > 1){
                if(columns[i].length > __row_length){
                    __row_length=columns[i].length;
                }
                tmp.push('<th>'+column+'</th>');
            }
        }
        return tmp.join('');
    }
    var __countValid = function(){
        if(__col_map == undefined)
            return undefined;
        var count=0;
        for(prop in __col_map){
            if(__col_map[prop] == true)
                count++;
        }
        return count;

    }
    var __renderRows = function(config){
        var tmp = [];

        var data = config.data;
        var x_var = data.x;
        var columns = data.columns;
        var col_length = columns.length;

        __col_map = {};
        for(var i=0;i<col_length;i++){
            __col_map[i] = true;
        }
        var categories;
        try{
            categories = config.axis.x.categories;
            if(categories == undefined){
                categories = [];
            }
        }
        catch(ex){
            categories = [];
        }

        var cat_length = categories.length;

        for(var j=1;j<__row_length;j++){
            var tmp2 = [];

            for(var i=0; i<col_length;i++){
                if((columns[i] != undefined && columns[i].length > 1)
                    || columns[i][0] == 'x'){

                    var column = columns[i][j];

                    var cheader = columns[i][0];

                    if(cheader == 'x'){
                        __col_map[i] = false;
                        if(cat_length == 0)
                            tmp2.unshift('<td>'+column+'</td>');
                        else
                            tmp2.unshift('<td>'+categories[j-1]+'</td>');
                    } else {
                        if(!isNaN(column)){
                            column = parseFloat(column).toFixed(2);
                        }
                        tmp2.push('<td>'+column+'</td>');
                    }
                } else {
                    __col_map[i] = false;
                }

            }

            tmp.push("<tr>"+tmp2.join('')+"</tr>");
        }
        return tmp.join('');
    }

    /* Returns the render of the table */
    var __renderTable = function(config){
        var tmp =[];
        tmp.push('<div id="export_btns"></div><br />')
        tmp.push('<table id="tabular_table" data-pagination="true" class="table table-bordered">');
        tmp.push('<thead>');
            tmp.push('<tr>')
                tmp.push('<th rowspan="2">'+config.axis.x.label.text+'</th>');
                tmp.push('<th id="rowcategories">'+config.axis.y.label.text+'</th>');
            tmp.push('</tr>')
            tmp.push('<tr>')
                tmp.push(__renderHeaderRows(config));
            tmp.push('</tr>')
        tmp.push('</thead>');
        tmp.push('<tbody>');
            tmp.push(__renderRows(config));
        tmp.push('</tbody>');
        tmp.push('</table>');
        return tmp.join('');
    }
    /* Main brain function */
    $.fn.c3js_to_tabular = function(c3conf, options) {

        __row_length = 0;
         var self = this;

         var settings = $.extend({
            'callback': undefined,
            'empty_callback': undefined
        }, options );

        var render = __renderTable(c3conf);

        $(self).html(render);

        var cv = __countValid();
        $('#rowcategories').attr('colspan', cv);

        var trs = $('tbody tr', $(self) );
        if(trs.length == 0){
            $('tbody', $(self) ).html('<tr><td colspan="'+(cv+1)+'"><center>There is no data available.</center></td></tr>');
            if(settings.empty_callback){
                settings.empty_callback();
            }
        }else {
            if(settings.callback){
                settings.callback();
            }
        }

        return this;

    };
}( jQuery ));
