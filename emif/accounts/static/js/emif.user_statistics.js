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