//$.post('api/insert', function (data) {
//    alert("coiso");
//    $('.result').html(data);
//    console.log("Response: " + data);
//});


function getQuestionValues(questionnaire_id, questionset_id, slug) {
    var result = "";
    $.ajax({
        type: "GET",
        url: "api/stats",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').prop('value'),
            q_id: questionnaire_id,
            qs_id: questionset_id,
            slug: slug
        },
        success: function (data) {
            result = data;
        }
    });
    return result;
}


//Not used
function draw_piechart(jsonData, div_id) {

    var data = JSON.parse(jsonData);

    var w = 620;
    var h = 480;
    var radius = Math.min(w, h) / 2; //change 2 to 1.4. It's hilarious.

    //TODO: Generate colors randomly, but have them be apart.
    var color = d3.scale.ordinal().range(["#7b4173", "#9ecae1", "#ff7f0e", "#bcbd22", "#8c564b", "#d62728"])

    var arc = d3.svg.arc() //each datapoint will create one later.
        .outerRadius(radius - 20)
        .innerRadius(0);
    //well, if you set this to not 0 it becomes a donut chart!

    var pie = d3.layout.pie()

        .sort(function (d) {
            return d.score;
        })
        .value(function (d) {
            return d.score;
        });

    var svg = d3.select('#' + div_id).append("svg")
        .attr("width", w)
        .attr("height", h)
        .attr("class", "chart")
        .append("g") //someone to transform. Groups data.
        .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");
    //transform to the center.


    //create the slices
    var slices = svg.selectAll(".arc")
        .data(pie(data.charts))
        .enter().append("g")
        .attr("class", "slice")
        .call(d3.helper.tooltip()
            .style({position: 'absolute', 'z-index': 10000, border: '2px solid black',
                padding: '3px 5px;', margin: 'auto', 'background-color': 'rgba(0, 0, 0, 0.8)',
                color: 'white', 'font-size': '12px', 'font-family': 'arial', 'border-top-left-radius': '5px',
                'border-top-right-radius': '5px', 'border-bottom-right-radius': '5px',
                'border-bottom-left-radius': '5px', 'vertical-align': 'middle', 'text-align': 'center',
                'min-width': '50px', 'overflow': 'auto'})
            .text(function (d) {
                return d.data.name + "<br />" + d.data.score;
            })
        )

    //and fill them
    slices.append("path")
        .attr("d", arc)
        .style("fill", function (d, i) {
            return color(i);
        });

    //add text, even
    slices.append("text")
        .attr("transform", function (d) {
            return "translate(" + arc.centroid(d) + ")";
        })
        .attr("class", "data-title")
        .text(function (d) {
            return d.data.name;
        });

    var legend = d3.select('#' + div_id).append("svg")
        .attr("class", "legend")
        .attr("width", radius / 2)
        .attr("height", h / 2)
        .selectAll("g")
        .data(color.domain().slice().reverse())
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(0," + i * 20 + ")";
        });

    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .text(function (d) {
            return d;
        });

//    });
}


function draw_tagcloud(dataSet, div_id) {

    var words =
        {"charts":[
        {name: "abc", score: 20},
        {name: "def", score: 50},
        {name: "ghi", score: 30},
        {name: "dasdas", score: 50},
        {name: "gdasdfhi", score: 80},
        {name: "ghgfdgfdi", score: 30},
        {name: "gdfgdhi", score: 30},
        {name: "ghi", score: 30},
        {name: "rrttre", score: 50},
        {name: "rte", score: 90},
        {name: "ghgfdytrytrgfdi", score: 30},
        {name: "ewerwerw", score: 30},
        {name: "jkl", score: 80}
    ]};

    var words2 =
    {"charttype": "piechart",
        "attr2": "score",
        "charts": [
            {"score": 6, "name": "subjeccct cohort"},
            {"score": 2, "name": "disease cohort"},
            {"score": 3, "name": "subjeccct sfdsfsdf"},
            {"score": 5, "name": "sdfsdfsd"},
            {"score": 10, "name": "subject practicsdfsdfsdfs  benefit plan"}
        ],
        "attr1": "name"
    };

    var data;

    data = JSON.parse(dataSet);
    data = words2;
    var fill = d3.scale.category20();
    var max = d3.max(data.charts, function (d) {
       return d.score;
    })
    var min = d3.min(data.charts, function (d) {
       return d.score;
    })

    d3.layout.cloud()
        .size([700, 300])
//        .words(data.charts.map(function (d) {
//            return {name: d.name, score: d.score};
//        }))
        .words(data.charts)
        .padding(5)
        .rotate(function (d) {
            console.log(d.score);
            return ~~(Math.random() * (d.score));
//            return 0;
        })
        .font("Impact")
        .fontSize(function (d) {
            return d.score ;
        })
        .on("end", draw)

        .start();




    function draw(words) {
        d3.select('#' + div_id).append("svg")
            .attr("width", 700)
            .attr("height", 280)
            .append("g")
            .attr("transform", "translate(400,150)")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function (d) {
//                return ((d.score-min)/(max-min))*50 + "px";
                return d.score *5 + "px";
            })
            .style("font-family", "Impact")
            .style("fill", function (d, i) {
                return fill(i);
            })
            .attr("text-anchor", "middle")
//            .attr("x", 100)
//            .attr("y", 20)
            .attr("transform", function (d) {
                console.log(d.x, d.y, d.rotate);
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function (d) {
                return d.name;
            })
//        .on("click", function(d) { alert(d.text) })
            .call(d3.helper.tooltip()
                .style({position: 'absolute', 'z-index': 10000, border: '2px solid black',
                    padding: '3px 5px;', margin: 'auto', 'background-color': 'rgba(0, 0, 0, 0.8)',
                    color: 'white', 'font-size': '12px', 'font-family': 'arial', 'border-top-left-radius': '5px',
                    'border-top-right-radius': '5px', 'border-bottom-right-radius': '5px',
                    'border-bottom-left-radius': '5px', 'vertical-align': 'middle', 'text-align': 'center',
                    'min-width': '50px', 'overflow': 'auto'})
                .text(function (d) {
                    return d.name + "<br />" + d.score;
                })
            )
//            .on('mouseover', function(d, i){ d3.select(this).style({fill: 'skyblue'}); })
//            .on('mouseout', function(d, i){ d3.select(this).style({fill: 'aliceblue'}); });

    }
}



function drawPie(pieName, dataSet, selectString, colors, margin, outerRadius, innerRadius, sortArcs) {
    var data = JSON.parse(dataSet);

    // pieName => A unique drawing identifier that has no spaces, no "." and no "#" characters.
    // dataSet => Input Data for the chart, itself.
    // selectString => String that allows you to pass in
    //           a D3 select string.
    // colors => String to set color scale.  Values can be...
    //           => "colorScale10"
    //           => "colorScale20"
    //           => "colorScale20b"
    //           => "colorScale20c"
    // margin => Integer margin offset value.
    // outerRadius => Integer outer radius value.
    // innerRadius => Integer inner radius value.
    // sortArcs => Controls sorting of Arcs by value.
    //              0 = No Sort.  Maintain original order.
    //              1 = Sort by arc value size.

    // Color Scale Handling...
    var colorScale = d3.scale.category20c();
    switch (colors) {
        case "colorScale10":
            colorScale = d3.scale.category10();
            break;
        case "colorScale20":
            colorScale = d3.scale.category20();
            break;
        case "colorScale20b":
            colorScale = d3.scale.category20b();
            break;
        case "colorScale20c":
            colorScale = d3.scale.category20c();
            break;
        default:
            colorScale = d3.scale.category20c();
    }
    ;

    var canvasWidth = 700;
    var pieWidthTotal = outerRadius * 2;
    ;
    var pieCenterX = outerRadius + margin / 2;
    var pieCenterY = outerRadius + margin / 2;
    var legendBulletOffset = 30;
    var legendVerticalOffset = outerRadius - margin;
    var legendTextOffset = 20;
    var textVerticalSpace = 20;

    var canvasHeight = 0;
    var pieDrivenHeight = outerRadius * 2 + margin * 2;
    var legendTextDrivenHeight = (data.charts.length * textVerticalSpace) + margin * 2;
    // Autoadjust Canvas Height
    if (pieDrivenHeight >= legendTextDrivenHeight) {
        canvasHeight = pieDrivenHeight;
    }
    else {
        canvasHeight = legendTextDrivenHeight;
    }

    var x = d3.scale.linear().domain([0, d3.max(data, function (d) {
        return d.score;
    })]).rangeRound([0, pieWidthTotal]);
    var y = d3.scale.linear().domain([0, data.length]).range([0, (data.length * 20)]);


    var synchronizedMouseOver = function () {
        var arc = d3.select(this);
        var indexValue = arc.attr("index_value");

        var arcSelector = "." + "pie-" + pieName + "-arc-" + indexValue;
        var selectedArc = d3.selectAll(arcSelector);
//        selectedArc.style("fill", "#999");
        selectedArc.style("fill-opacity", ".7");

        var bulletSelector = "." + "pie-" + pieName + "-legendBullet-" + indexValue;
        var selectedLegendBullet = d3.selectAll(bulletSelector);
//        selectedLegendBullet.style("fill", "#999");
        selectedLegendBullet.style("fill-opacity", ".7");

        var textSelector = "." + "pie-" + pieName + "-legendText-" + indexValue;
        var selectedLegendText = d3.selectAll(textSelector);
//        selectedLegendText.style("fill", "#999");
        selectedLegendText.style("fill-opacity", ".7");

    };

    var synchronizedMouseOut = function () {
        var arc = d3.select(this);
        var indexValue = arc.attr("index_value");

        var arcSelector = "." + "pie-" + pieName + "-arc-" + indexValue;
        var selectedArc = d3.selectAll(arcSelector);
        var colorValue = selectedArc.attr("color_value");
//        selectedArc.style("fill", colorValue);
        selectedArc.style("fill-opacity", "1");

        var bulletSelector = "." + "pie-" + pieName + "-legendBullet-" + indexValue;
        var selectedLegendBullet = d3.selectAll(bulletSelector);
        var colorValue = selectedLegendBullet.attr("color_value");
//        selectedLegendBullet.style("fill", colorValue);
        selectedLegendBullet.style("fill-opacity", "1");

        var textSelector = "." + "pie-" + pieName + "-legendText-" + indexValue;
        var selectedLegendText = d3.selectAll(textSelector);
        selectedLegendText.style("fill", "Black");
        selectedLegendText.style("fill-opacity", "1");

    };

    var tweenPie = function (b) {
        b.innerRadius = 0;
        var i = d3.interpolate({startAngle: 0, endAngle: 0}, b);
        return function (t) {
            return arc(i(t));
        };
    }

    // Create a drawing canvas...
    var canvas = d3.select(selectString)
        .append("svg:svg") //create the SVG element inside the <body>
        .data([data]) //associate our data with the document
        .attr("width", canvasWidth) //set the width of the canvas
        .attr("height", canvasHeight) //set the height of the canvas
        .append("svg:g") //make a group to hold our pie chart
        .attr("transform", "translate(" + pieCenterX + "," + pieCenterY + ")") // Set center of pie

    // Define an arc generator. This will create <path> elements for using arc data.
    var arc = d3.svg.arc()
        .innerRadius(innerRadius) // Causes center of pie to be hollow
        .outerRadius(outerRadius);

    // Define a pie layout: the pie angle encodes the value of dataSet.
    // Since our data is in the form of a post-parsed CSV string, the
    // values are Strings which we coerce to Numbers.
    var pie = d3.layout.pie()
        .value(function (d) {
            return d.score;
        })
        .sort(function (a, b) {
            if (sortArcs == 1) {
                return b.score - a.score;
            } else {
                return null;
            }
        });

    // Select all <g> elements with class slice (there aren't any yet)
    var arcs = canvas.selectAll("g.slice")
        // Associate the generated pie data (an array of arcs, each having startAngle,
        // endAngle and value properties)
        .data(pie(data.charts))
        // This will create <g> elements for every "extra" data element that should be associated
        // with a selection. The result is creating a <g> for every object in the data array
        // Create a group to hold each slice (we will have a <path> and a <text>      // element associated with each slice)
        .enter().append("svg:a")
//            .attr("xlink:href", function(d) { return d.data.link; })
        .append("svg:g")
        .attr("class", "slice")    //allow us to style things in the slices (like text)
        // Set the color for each slice to be chosen from the color function defined above
        // This creates the actual SVG path using the associated data (pie) with the arc drawing function
        .style("stroke", "White")
        .attr("d", arc)
        .call(d3.helper.tooltip()
                .style({position: 'absolute', 'z-index': 10000, border: '2px solid black',
                    padding: '3px 5px;', margin: 'auto', 'background-color': 'rgba(0, 0, 0, 0.8)',
                    color: 'white', 'font-size': '12px', 'font-family': 'arial', 'border-top-left-radius': '5px',
                    'border-top-right-radius': '5px', 'border-bottom-right-radius': '5px',
                    'border-bottom-left-radius': '5px', 'vertical-align': 'middle', 'text-align': 'center',
                    'min-width': '50px', 'overflow': 'auto'})
                .text(function (d) {
                    return d.data.name + "<br />" + d.data.score;
                })
            );

    arcs.append("svg:path")
        // Set the color for each slice to be chosen from the color function defined above
        // This creates the actual SVG path using the associated data (pie) with the arc drawing function
        .attr("fill", function (d, i) {
            return colorScale(i);
        })
        .attr("color_value", function (d, i) {
            return colorScale(i);
        }) // Bar fill color...
        .attr("index_value", function (d, i) {
            return "index-" + i;
        })
        .attr("class", function (d, i) {
            return "pie-" + pieName + "-arc-index-" + i;
        })
        .style("stroke", "White")
        .attr("d", arc)
        .on('mouseover', synchronizedMouseOver)
        .on("mouseout", synchronizedMouseOut)
        .transition()
//            .ease("bounce")
        .duration(1000)
//            .delay(function(d, i) { return i * 50; })
        .attrTween("d", tweenPie)

    ;

    // Add a score value to the larger arcs, translated to the arc centroid and rotated.
    arcs.filter(function (d) {
        return d.endAngle - d.startAngle > .2;
    }).append("svg:text")
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")
//        .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")rotate(" + angle(d) + ")"; })
        .attr("transform", function (d) { //set the label's origin to the center of the arc
            //we have to make sure to set these before calling arc.centroid
            d.outerRadius = outerRadius; // Set Outer Coordinate
            d.innerRadius = innerRadius; // Set Inner Coordinate
            return "translate(" + arc.centroid(d) + ")rotate(0)";
        })
        .style("fill", "White")
        .style("font", "normal 12px Arial")
        .text(function (d) {
            return d.data.score;
        });


    // Computes the angle of an arc, converting from radians to degrees.
    function angle(d) {
        var a = (d.startAngle + d.endAngle) * 90 / Math.PI - 90;
        return a > 90 ? a - 180 : a;
    }

    // Plot the bullet circles...
    canvas.selectAll("circle")
        .data(data.charts).enter().append("svg:circle") // Append circle elements
        .attr("cx", outerRadius + legendBulletOffset)
        .attr("cy", function (d, i) {
            return i * textVerticalSpace - legendVerticalOffset;
        })
        .attr("stroke-width", ".5")
        .style("fill", function (d, i) {
            return colorScale(i);
        }) // Bullet fill color
        .attr("r", 5)
        .attr("color_value", function (d, i) {
            return colorScale(i);
        }) // Bar fill color...
        .attr("index_value", function (d, i) {
            return "index-" + i;
        })
        .attr("class", function (d, i) {
            return "pie-" + pieName + "-legendBullet-index-" + i;
        })
        .on('mouseover', synchronizedMouseOver)
        .on("mouseout", synchronizedMouseOut);

    // Create hyper linked text at right that acts as label key...
    canvas.selectAll("a.legend_link")
        .data(data.charts) // Instruct to bind data to text elements
        .enter().append("svg:a") // Append legend elements
//            .attr("xlink:href", function(d) { return d.link; })
        .append("text")
        .attr("text-anchor", "center")
        .attr("x", outerRadius + legendBulletOffset + legendTextOffset)
        //.attr("y", function(d, i) { return legendOffset + i*20 - 10; })
        //.attr("cy", function(d, i) {    return i*textVerticalSpace - legendVerticalOffset; } )
        .attr("y", function (d, i) {
            return i * textVerticalSpace - legendVerticalOffset;
        })
        .attr("dx", 0)
        .attr("dy", "5px") // Controls padding to place text in alignment with bullets
        .text(function (d) {
            return d.name;
        })
        .attr("color_value", function (d, i) {
            return colorScale(i);
        }) // Bar fill color...
        .attr("index_value", function (d, i) {
            return "index-" + i;
        })
        .attr("class", function (d, i) {
            return "pie-" + pieName + "-legendText-index-" + i;
        })
        .style("fill", "Black")
        .style("font", "normal 1.1em Arial")
        .on('mouseover', synchronizedMouseOver)
        .on("mouseout", synchronizedMouseOut)
    .call(d3.helper.tooltip()
                .style({position: 'absolute', 'z-index': 10000, border: '2px solid black',
                    padding: '3px 5px;', margin: 'auto', 'background-color': 'rgba(0, 0, 0, 0.8)',
                    color: 'white', 'font-size': '12px', 'font-family': 'arial', 'border-top-left-radius': '5px',
                    'border-top-right-radius': '5px', 'border-bottom-right-radius': '5px',
                    'border-bottom-left-radius': '5px', 'vertical-align': 'middle', 'text-align': 'center',
                    'min-width': '50px', 'overflow': 'auto'})
                .text(function (d) {
                    return d.name + "<br />" + d.score;
                })
            );

};


function drawHorizontalBarChart(chartID, dataSet, selectString, colors) {

        // chartID => A unique drawing identifier that has no spaces, no "." and no "#" characters.
        // dataSet => Input Data for the chart, itself.
        // selectString => String that allows you to pass in
        //           a D3 select string.
        // colors => String to set color scale.  Values can be...
        //           => "colorScale10"
        //           => "colorScale20"
        //           => "colorScale20b"
        //           => "colorScale20c"

     var data = JSON.parse(dataSet);

        var canvasWidth = 700;
        var barsWidthTotal = 300
        var barHeight = 20;
        var barsHeightTotal = barHeight * data.charts.length;
        //var canvasHeight = 200;
        var canvasHeight = data.charts.length * barHeight + 50; // +10 puts a little space at bottom.
        var legendOffset = barHeight/2;
        var legendBulletOffset = 30;
        var legendTextOffset = 20;

        var x = d3.scale.linear().domain([0, d3.max(data.charts, function(d) { return d.score; })]).rangeRound([0, barsWidthTotal]);
        var y = d3.scale.linear().domain([0, data.charts.length]).range([0, barsHeightTotal]);

        // Color Scale Handling...
        var colorScale = d3.scale.category20c();
        switch (colors)
        {
          case "colorScale10":
            colorScale = d3.scale.category10();
            break;
          case "colorScale20":
            colorScale = d3.scale.category20();
            break;
          case "colorScale20b":
            colorScale = d3.scale.category20b();
            break;
          case "colorScale20c":
            colorScale = d3.scale.category20c();
            break;
          default:
            colorScale = d3.scale.category20c();
        };

        var synchronizedMouseOver = function() {
          var bar = d3.select(this);
          var indexValue = bar.attr("index_value");

          var barSelector = "." + "bars-" + chartID + "-bar-" + indexValue;
          var selectedBar = d3.selectAll(barSelector);
//          selectedBar.style("fill", "Maroon");
          selectedBar.style("fill-opacity", ".7");

          var bulletSelector = "." + "bars-" + chartID + "-legendBullet-" + indexValue;
          var selectedLegendBullet = d3.selectAll(bulletSelector);
//          selectedLegendBullet.style("fill", "Maroon");
          selectedLegendBullet.style("fill-opacity", ".7");

          var textSelector = "." + "bars-" + chartID + "-legendText-" + indexValue;
          var selectedLegendText = d3.selectAll(textSelector);
//          selectedLegendText.style("fill", "Maroon");
          selectedLegendText.style("fill-opacity", ".7");
        };

        var synchronizedMouseOut = function() {
          var bar = d3.select(this);
          var indexValue = bar.attr("index_value");

          var barSelector = "." + "bars-" + chartID + "-bar-" + indexValue;
          var selectedBar = d3.selectAll(barSelector);
          var colorValue = selectedBar.attr("color_value");
          selectedBar.style("fill", colorValue);
          selectedBar.style("fill-opacity", "1");

          var bulletSelector = "." + "bars-" + chartID + "-legendBullet-" + indexValue;
          var selectedLegendBullet = d3.selectAll(bulletSelector);
          var colorValue = selectedLegendBullet.attr("color_value");
          selectedLegendBullet.style("fill", colorValue);
          selectedLegendBullet.style("fill-opacity", "1");

          var textSelector = "." + "bars-" + chartID + "-legendText-" + indexValue;
          var selectedLegendText = d3.selectAll(textSelector);
          selectedLegendText.style("fill", "Black");
          selectedLegendText.style("fill-opacity", "1");
        };

      // Create the svg drawing canvas...
      var canvas = d3.select(selectString)
        .append("svg:svg")
          //.style("background-color", "yellow")
          .attr("width", canvasWidth)
          .attr("height", canvasHeight);

      // Draw individual hyper text enabled bars...
      canvas.selectAll("rect")
        .data(data.charts)
        .enter().append("svg:a")
//          .attr("xlink:href", function(d) { return d.link; })
          .append("svg:rect")
            // NOTE: the "15 represents an offset to allow for space to place magnitude
            // at end of bars.  May have to address this better, possibly by placing the
            // magnitude within the bars.
            .attr("x", function(d) { return barsWidthTotal - x(d.score) + 10; }) // Left to right
//            .attr("x", 0) // Right to left
            .attr("y", function(d, i) { return y(i); })
            .attr("height", barHeight)
            .on('mouseover', synchronizedMouseOver)
            .on("mouseout", synchronizedMouseOut)
            .call(d3.helper.tooltip()
                .style({position: 'absolute', 'z-index': 10000, border: '2px solid black',
                    padding: '3px 5px;', margin: 'auto', 'background-color': 'rgba(0, 0, 0, 0.8)',
                    color: 'white', 'font-size': '12px', 'font-family': 'arial', 'border-top-left-radius': '5px',
                    'border-top-right-radius': '5px', 'border-bottom-right-radius': '5px',
                    'border-bottom-left-radius': '5px', 'vertical-align': 'middle', 'text-align': 'center',
                    'min-width': '50px', 'overflow': 'auto'})
                .text(function (d) {
                    return d.name + "<br />" + d.score;
                })
            )
            .style("fill", "White" )
            .style("stroke", "White" )
            .transition()

//	      .ease("bounce")
//              .duration(1500)
//              .delay(function(d, i) { return i * 100; })
            .attr("width", function(d) { return x(d.score); })
            .style("fill", function(d, i) { colorVal = colorScale(i); return colorVal; } )
            .attr("index_value", function(d, i) { return "index-" + i; })
            .attr("class", function(d, i) { return "bars-" + chartID + "-bar-index-" + i; })
            .attr("color_value", function(d, i) { return colorScale(i); }) // Bar fill color...
            .style("stroke", "white"); // Bar border color...


      // Create text values that go at end of each bar...
      canvas.selectAll("text")
        .data(data.charts) // Bind dataSet to text elements
        .enter().append("svg:text") // Append text elements
          .attr("x", x)
          .attr("y", function(d, i) { return y(i); })
          //.attr("y", function(d) { return y(d) + y.rangeBand() / 2; })
//          .attr("dx", function(d) { return x(d.score) - 5; })
          .attr("dx", function() {return barsWidthTotal - 5; })
          .attr("dy", barHeight-5) // vertical-align: middle
          .attr("text-anchor", "end") // text-align: right
          .text(function(d) { return d.score;})
          .call(d3.helper.tooltip()
                .style({position: 'absolute', 'z-index': 10000, border: '2px solid black',
                    padding: '3px 5px;', margin: 'auto', 'background-color': 'rgba(0, 0, 0, 0.8)',
                    color: 'white', 'font-size': '12px', 'font-family': 'arial', 'border-top-left-radius': '5px',
                    'border-top-right-radius': '5px', 'border-bottom-right-radius': '5px',
                    'border-bottom-left-radius': '5px', 'vertical-align': 'middle', 'text-align': 'center',
                    'min-width': '50px', 'overflow': 'auto'})
                .text(function (d) {
                    return d.name + "<br />" + d.score;
                })
            )
          .attr("fill", "White");

      // Plot the bullet circles...
      canvas.selectAll("circle")
        .data(data.charts).enter().append("svg:circle") // Append circle elements
          .attr("cx", barsWidthTotal + legendBulletOffset)
          .attr("cy", function(d, i) { return legendOffset + i*barHeight; } )
          .attr("stroke-width", ".5")
          .style("fill", function(d, i) { return colorScale(i); }) // Bar fill color
          .attr("index_value", function(d, i) { return "index-" + i; })
          .attr("class", function(d, i) { return "bars-" + chartID + "-legendBullet-index-" + i; })
          .attr("r", 5)
          .attr("color_value", function(d, i) { return colorScale(i); }) // Bar fill color...
          .on('mouseover', synchronizedMouseOver)
          .on("mouseout", synchronizedMouseOut);

      // Create hyper linked text at right that acts as label key...
      canvas.selectAll("a.legend_link")
        .data(data.charts) // Instruct to bind dataSet to text elements
        .enter().append("svg:a") // Append legend elements
//          .attr("xlink:href", function(d) { return d.name; })
            .append("text")
              .attr("text-anchor", "center")
              .attr("x", barsWidthTotal + legendBulletOffset + legendTextOffset)
              //.attr("y", function(d, i) { return legendOffset + i*20 - 10; })
              .attr("y", function(d, i) { return legendOffset + i*barHeight; } )
              .attr("dx", 0)
              .attr("dy", "5px") // Controls padding to place text above bars
              .text(function(d) { return d.name;})
              .style("fill", "Black")
              .attr("index_value", function(d, i) { return "index-" + i; })
              .attr("class", function(d, i) { return "bars-" + chartID + "-legendText-index-" + i; })
              .on('mouseover', synchronizedMouseOver)
              .on("mouseout", synchronizedMouseOut)
      .call(d3.helper.tooltip()
                .style({position: 'absolute', 'z-index': 10000, border: '2px solid black',
                    padding: '3px 5px;', margin: 'auto', 'background-color': 'rgba(0, 0, 0, 0.8)',
                    color: 'white', 'font-size': '12px', 'font-family': 'arial', 'border-top-left-radius': '5px',
                    'border-top-right-radius': '5px', 'border-bottom-right-radius': '5px',
                    'border-bottom-left-radius': '5px', 'vertical-align': 'middle', 'text-align': 'center',
                    'min-width': '50px', 'overflow': 'auto'})
                .text(function (d) {
                    return d.name + "<br />" + d.score;
                })
            );

      };
