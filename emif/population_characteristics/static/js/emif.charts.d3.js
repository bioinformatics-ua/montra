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
  this.div = divArg;
  this.dataValues = dataArg;
  this.xscale = null ;
  this.yscale = null ;
  this.self = this;
  this.init = function(){

    console.log('this in GraphCharD3'  + this);
  };

  this.translateData = function(objects){

    console.log(objects);
    /*** Lets translate our data model to the d3 support data model */
    xscale = {'bins':5}
    xscale.bins = 25;
    var i = 1;
    dataset = [[],

                 ];
    objects.values.forEach(function(row){
      dataset[0].push({'xvalue':row.Value1, 'yvalue':parseInt(row.Count)});

    });

  };

  this.draw = function(div, dataset){

      var margin = {top: 20, right: 20, bottom: 30, left: 60},
          width = 460 - margin.left - margin.right,
          height = 500 - margin.top - margin.bottom;

      var formatPercent = d3.format("000.0");

      var x = d3.scale.ordinal()
          .rangeRoundBands([0, width], .1);



      var y = d3.scale.linear()
          .range([height, 0]);

      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left");
          //.ticks(d3.time.years, 10)
          //.tickFormat(formatPercent);
           var xAxis = null;
           var self = this;
    function zoom() {

        svg.select(".xaxis").call(xAxis);
        svg.select(".yaxis").call(yAxis);
        svg.selectAll(".svg rect").attr("transform", "translate(" + d3.event.translate[0] + ",0)scale(" + d3.event.scale + ", 1)");
        this.xscale.bins = this.xscale.bins +10;

    };

      var svg = d3.select(div).append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        svg.call(d3.behavior.zoom().on("zoom",  function () {
          zoom();

    }));

      dataset.forEach(function (data) {
        console.log("THIS IS MY DATA: " + data);
        console.log(data);

        x.domain(data.map(function(d) {  return d.xvalue; }));
        y.domain([0, d3.max(data, function(d) { return d.yvalue; })]);

      xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom")
          .tickValues(x.domain().filter(function(d, i) {return !(i % this.xscale.bins); }))
          .tickSize(-width)
          .tickPadding(8);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .append("text")
            //.attr("transform", "rotate(-90)")
            .attr("x", 6)
            .attr("dx", 350)
            .attr("dy", "0em")
            .style("text-anchor", "end")
            .text("Years");


        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("");

        svg.selectAll(".bar")
            .data(data)
          .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.xvalue); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.yvalue); })
            .attr("height", function(d) { return height - y(d.yvalue); });

      });



   };
};





