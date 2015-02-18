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

// Load the configurations

/***
* This configuration will say what type of charts the tool will draw
*
*/

function PCConfs ()
{
    this.getSettings = function(fingerprintId){
        var result = {};

        $.ajax({
          dataType: "json",
          url: "population/settings/" + fingerprintId + "/",
          async: false,
          type: "POST",
          data: {result: result, publickey: global_public_key},
          success: function (data){result=data;}
        });
        return JSON.parse(result.conf).charts;

    };
};

function ChartLayout ()
{
    var configs = null
    this.getChartTitles = function(fingerprintId){
        var configs = new PCConfs();
        var charts = configs.getSettings(fingerprintId);
        var charts_titles = [];
        charts.forEach(function(a){
            if (a.title.fixed_title!= 'None')
                charts_titles.push({'tooltip': a.tooltip ,'title': a.title.fixed_title})
            else
                charts_titles.push({'tooltip': a.tooltip ,'title': a.title['var']})
        });
        return charts_titles;
    };

    this.getFilters = function(graph_type, fingerprintId){
        // TODO
        return null;
    };

    this.getScales = function(graph_type, fingerprintId){
        // TODO
        return null;
    };

    this.getAxis = function(graph_type, fingerprintId){
        // TODO
        return null;
    };


};



