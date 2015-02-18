/*# -*- coding: utf-8 -*-
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
#*/
$(function(){


});

  var session_times = [{
        key: "Session Time per day(in hours)",
        values: []
        }
      ];
  var view_times = [{
        key: "Views per day(in hours)",
        values: []
        }
      ];

  function addSession(label, value){
    session_times[0].values.push({"label": label, "value": value});
  }
  function addView(label, value){
    view_times[0].values.push({"label": label, "value": value});
  }
function drawSessionTimes(){
      // Session time graph
    nv.addGraph(function() {
    var chart = nv.models.discreteBarChart()
        .x(function(d) { return d.label })    //Specify the data accessors.
        .y(function(d) { return d.value })
        .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
        .tooltips(true)        //Don't show tooltips
        .showValues(false)       //...instead, show the bar value right on top of each bar.
        .transitionDuration(350)
        .showXAxis(false)
        ;

    chart.yAxis.axisLabel("Hours")

    d3.select('#session_time svg')
        .datum(session_times)
        .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
  });
}

function drawViewTimes(){
    // User views graph
    nv.addGraph(function() {
    var chart = nv.models.discreteBarChart()
        .x(function(d) { return d.label })    //Specify the data accessors.
        .y(function(d) { return d.value })
        .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
        .tooltips(true)        //Don't show tooltips
        .showValues(false)       //...instead, show the bar value right on top of each bar.
        .transitionDuration(350)
        .showXAxis(false)
        ;

    d3.select('#users_views svg')
        .datum(view_times)
        .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
  });
}
