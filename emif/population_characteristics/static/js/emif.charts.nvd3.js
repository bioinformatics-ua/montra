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
function GraphicChartD3(divArg, dataArg)
{
  /** Passes the initial arguments required to start and d3
  Also , this should be used to know if
  */
  var div = divArg;
  var dataValues = dataArg;
  var self = this;
  this.init = function(){

    console.log('this in GraphCharD3'  + this);
  };

  this.translate_data = function(objects){


    /*** Lets translate our data model to the d3 support data model */


  };

  this.draw = function(div, dataset){
     nv.addGraph(function() {
               var chart = nv.models.discreteBarChart()
                   .x(function(d) { return d.label })
                   .y(function(d) { return d.value })
                   .staggerLabels(false)
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

   };
};





