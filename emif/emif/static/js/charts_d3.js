//$.post('api/insert', function (data) {
//    alert("coiso");
//    $('.result').html(data);
//    console.log("Response: " + data);
//});


function getQuestionValues(questionnaire_id, questionset_id, slug, type) {
    var result = "";
    $.ajax({
        type: "GET",
        url: "api/stats",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').prop('value'),
            q_id: questionnaire_id,
            qs_id: questionset_id,
            slug: slug,
            type: type
        },
        success: function (data) {
            //        alert("success");
            console.log("Response: " + data);
            result = data;
        }
    });
    return result;
}


function draw_piechart(jsonData) {
;
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


        var svg = d3.select("#chart").append("svg")
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
