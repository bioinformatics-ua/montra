confs = {
    icon: '<i class="icon-download-alt"></i>',
    name: "Extra Information",
    extralibs: ["{{STATIC_URL}}js/d3/d3.v3.min.js"]
};
plugin = function(sdk) {
    var context = sdk.container();

    function color(d) {
        return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
    }

    function click(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        update(d);
    }
    var vis, w = 960,
        u = 0,
        h = 800,
        barHeight = 20,
        barWidth = w * .8,
        duration = 400,
        root;

    var tree = d3.layout.tree()
        .size([h, 100]);

    var diagonal = d3.svg.diagonal()
        .projection(function(d) {
            return [d.y, d.x];
        });

    function json_to_d3json(obj) {
        d3_result = {};
        hash_childrens = {};
        d3_result['name'] = 'Extra Information';

        d3_aux = [];
        for (var t = 0; t < obj.length; t++) {

            var row = obj[t];
            var key = row.field
            var res = key.split("+");

            var aux_root = d3_aux;
            console.log(d3_aux);

            compact_slug = "";
            for (var j = 0; j < res.length; j++) {

                var l = res[j];
                if (compact_slug !== "") {
                    compact_slug = compact_slug + "+" + l;
                } else {
                    compact_slug = l;
                }
                var aux = {}
                aux['name'] = l;

                if (res.length - 1 != j) {

                    if (compact_slug in hash_childrens) {
                        aux_root = hash_childrens[compact_slug];
                    } else {
                        var aux_list = [];
                        aux['children'] = aux_list;
                        aux_root.push(aux);
                        aux_root = aux_list;
                        hash_childrens[compact_slug] = aux_list;
                    }

                } else {

                    if (compact_slug in hash_childrens) {
                        var aux2 = {}
                        aux2['name'] = row.value;
                        hash_childrens[compact_slug].push(aux2);

                    } else {

                        var aux2 = {};
                        aux2['name'] = row.value;
                        var aux_list = [aux2];
                        aux['children'] = aux_list;

                        hash_childrens[compact_slug] = aux_list
                        aux_root.push(aux);
                    }


                }

            }

        }

        d3_result['children'] = d3_aux;
        console.log(hash_childrens);
        console.log(d3_result);
        return d3_result;
    }

    var base = function(data) {
        var tmp = '<div class="span12">\
            <a class="btn_pivot_table btn pull-right" href="">Pivot table</a>\
            </div>\
            <div>\
                <div class="chart span4" style="display:none;"></div>\
                <div class="span10 pivot_table_extra_information">\
                <table class="table table-bordered table-hover">\
                <thead><th>Tag</th><th>Value</th></thead>\
                <tbody>';

        for (var i = 0; i < data.length; i++) {
            var row = data[i];
            tmp += "<tr><td>" + row.field + "</td><td>" + row.value + "</td></tr>";
        }

        tmp += '</tbody></table></div>\
                </div> <div class="span8"></div>';

        return tmp;
    }

    function update(source) {

        // Compute the flattened node list. TODO use d3.layout.hierarchy.
        var nodes = tree.nodes(root);

        // Compute the "layout".
        nodes.forEach(function(n, i) {
            n.x = i * barHeight;
        });

        // Update the nodes…
        var node = vis.selectAll("g.node")
            .data(nodes, function(d) {
                return d.id || (d.id = ++u);
            });

        var nodeEnter = node.enter().append("svg:g")
            .attr("class", "node")
            .attr("transform", function(d) {
                return "translate(" + source.y0 + "," + source.x0 + ")";
            })
            .style("opacity", 1e-6);

        // Enter any new nodes at the parent's previous position.
        nodeEnter.append("svg:rect")
            .attr("y", -barHeight / 2)
            .attr("height", barHeight)
            .attr("width", barWidth)
            .style("fill", color)
            .on("click", click);

        nodeEnter.append("svg:text")
            .attr("dy", 3.5)
            .attr("dx", 5.5)
            .text(function(d) {
                return d.name;
            });

        // Transition nodes to their new position.
        nodeEnter.transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + d.y + "," + d.x + ")";
            })
            .style("opacity", 1);

        node.transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + d.y + "," + d.x + ")";
            })
            .style("opacity", 1)
            .select("rect")
            .style("fill", color);

        // Transition exiting nodes to the parent's new position.
        node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .style("opacity", 1e-6)
            .remove();

        // Update the links…
        var link = vis.selectAll("path.link")
            .data(tree.links(nodes), function(d) {
                return d.target.id;
            });

        // Enter any new links at the parent's previous position.
        link.enter().insert("svg:path", "g")
            .attr("class", "link")
            .attr("d", function(d) {
                var o = {
                    x: source.x0,
                    y: source.y0
                };
                return diagonal({
                    source: o,
                    target: o
                });
            })
            .transition()
            .duration(duration)
            .attr("d", diagonal);

        // Transition links to their new position.
        link.transition()
            .duration(duration)
            .attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(duration)
            .attr("d", function(d) {
                var o = {
                    x: source.x,
                    y: source.y
                };
                return diagonal({
                    source: o,
                    target: o
                });
            })
            .remove();

        // Stash the old positions for transition.
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }
    sdk.html('Loading...');
    sdk.refresh();

    var fp = FingerprintProxy.getInstance();
    var store = fp.getStore();

    store.getExtra().then(function(response) {

        if (response.api.length > 0) {
            sdk.html(base(response.api));
            sdk.refresh();
            vis = d3.select(".chart", context).append("svg:svg")
                .attr("width", 960)
                .attr("height", 800)
                .append("svg:g")
                .attr("transform", "translate(20,30)");
            var chart = json_to_d3json(response.api);
            chart.x0 = 0;
            chart.y0 = 0;
            root = chart;
            update(chart);

            var pivot_table = $('.btn_pivot_table', context);
            pivot_table.bind('click', function(e) {
                $(".pivot_table_extra_information", context).toggle();
                $(".chart", context).toggle();

                if (pivot_table.text() == 'Pivot table') {
                    pivot_table.text('Tree view');
                } else {
                    pivot_table.text('Pivot table');
                }
                return false;
            });
        } else {
            sdk.html('<center>No information available. You can add information from external applications with <a href="api-info">API web services.</a></center>');
            sdk.refresh();
        }
    });
};
