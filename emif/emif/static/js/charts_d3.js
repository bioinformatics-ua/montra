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
            //        alert("success");
//            console.log("Response: " + data);
            result = data;
        }
    });
    return result;
}


function draw_piechart(jsonData,div_id) {

    var data = JSON.parse(jsonData);

//    d3.json("http://localhost:8000/api/stats", function (error, data) {
//    d3.json(myjson, function (error, data) {

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
            .attr("class", "slice");

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

//    });
}

function draw_tagcloud(div_id) {
    var jWord = ["abc","def","ghi", "jkl"];
    var jCount = ["20", "50", "30", "80"];
    var words = [
  {text: "abc", size: 20},
  {text: "def", size: 50},
  {text: "ghi", size: 30},
  {text: "dasdas", size: 50},
  {text: "gdasdfhi", size: 80},
  {text: "ghgfdgfdi", size: 30},
  {text: "gdfgdhi", size: 30},{text: "ghi", size: 30},
  {text: "rrttre", size: 50},
  {text: "rte", size: 90},
  {text: "ghgfdytrytrgfdi", size: 30},
  {text: "ewerwerw", size: 30},
  {text: "jkl", size: 80}
];

    var fill = d3.scale.category20();
    var max = d3.max(words, function(d) { return d.size; })
    var tooltip = d3.select("body")


    d3.layout.cloud().size([900, 300])
      .words(words.map(function(d) {
          return {text: d.text, size: d.size};
        }))
      .padding(5)
      .rotate(function(d) { return ~~(Math.random()* (d.size - max/2)) ; })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw)
      .start();

    function draw(words) {
    d3.select('#' + div_id).append("svg")
        .attr("width", 900)
        .attr("height", 300)
      .append("g")
        .attr("transform", "translate(400,150)")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; })
        .on("click", function(d) { alert(d.text) })
        .call(d3.helper.tooltip()
//            .attr({class: function(d, i) { return d + ' ' +  i + ' A'; }})
//            .style({color: 'blue'})
            .text(function(d){ return d.size; })
        )
//            .on('mouseover', function(d, i){ d3.select(this).style({fill: 'skyblue'}); })
//            .on('mouseout', function(d, i){ d3.select(this).style({fill: 'aliceblue'}); });

    }
}
