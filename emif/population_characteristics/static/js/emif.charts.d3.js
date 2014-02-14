
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

  this.translateData = function(objects){
    
    console.log(objects);
    /*** Lets translate our data model to the d3 support data model */ 

    var i = 1;
    dataset = [[], 
                 
                 ];
    objects.values.forEach(function(row){
      dataset[0].push({'xvalue':row.Value1, 'yvalue':parseInt(row.Min)});
  
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

      var xAxis = d3.svg.axis()
          .scale(x)

          .orient("bottom")
          .ticks(d3.time.years, 10)
          .tickValues(["", "", ""])
          .tickPadding(8);


      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left");
          //.ticks(d3.time.years, 10)
          //.tickFormat(formatPercent);

      var svg = d3.select(div).append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      
      dataset.forEach(function (data) {
        console.log(data);
        

        x.domain(data.map(function(d) {  return d.xvalue; }));
        y.domain([0, d3.max(data, function(d) { return d.yvalue; })]);

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
            .text("Active patients");

        svg.selectAll(".bar")
            .data(data)
          .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { console.log(d); return x(d.xvalue); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { console.log(d); return y(d.yvalue); })
            .attr("height", function(d) { return height - y(d.yvalue); });

      });

   }; 
};





