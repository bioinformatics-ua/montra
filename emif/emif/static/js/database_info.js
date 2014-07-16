$('#li_workspace').addClass("active");

$("#btn_pivot_table").bind('click', function(e) {
    $("#pivot_table_extra_information").toggle();
    $("#chart").toggle();

    if ($('#btn_pivot_table').text() == 'Pivot table') {
        $('#btn_pivot_table').text('Tree view');
    } else {
        $('#btn_pivot_table').text('Pivot table');
    }
    return false;
});
$("#collapseall_metadata").bind('click', function(e) {
    //e.preventDefault(); 
    //e.stopPropagation();

    collapse_expand(this);

    return false;
});

function collapse_expand(context) {
    if ($(context).text().indexOf('Collapse') !== -1) {
        $(context).html('<i class="icon-plus"></i>&nbsp; Expand all');
        //change_name_collapse(false);

        $(".collapse:visible").collapse("hide");

    } else {
        $(context).html('<i class="icon-minus"></i>&nbsp; Collapse all');
        //change_name_collapse(true);
        $(".collapse:visible").collapse("show");
    }
}

$('.popover').popover({
    container: 'body'
});

$.fn.textWidth = function() {
    var node, original, width;
    original = $(this).html();
    node = $("<span style='position:absolute;width:auto;left:-9999px'>" + original + "</span>");
    //node.css('font-family', $(this).css('font-family')).css('font-size', $(this).//css('font-size'));
    $('body').append(node);
    width = node.width();
    node.remove();
    return width;
};
/* TODO: Toggle + Expand all
             $('.').on('click', function(e) {
             e.preventDefault();
             var $this = $(this);
             var $collapse = $this.closest('.collapse-group').find('.collapse');
             $collapse.collapse('toggle');
             });
             */


var w = 960,
    h = 800,
    i = 0,
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

var vis = d3.select("#chart").append("svg:svg")
    .attr("width", w)
    .attr("height", h)
    .append("svg:g")
    .attr("transform", "translate(20,30)");

function json_to_d3json(obj) {
    d3_result = {};
    hash_childrens = {};
    d3_result['name'] = 'Extra Information';

    d3_aux = [];
    for (var key in obj) {
        var res = key.split("+");

        var aux_root = d3_aux;

        compact_slug = "";
        console.log(key);
        for (var j = 0; j < res.length; j++) {

            var l = res[j];
            if (compact_slug != "") {
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
                    aux2['name'] = obj[key];
                    hash_childrens[compact_slug].push(aux2);

                } else {

                    var aux2 = {}
                    aux2['name'] = obj[key];
                    var aux_list = [aux2];
                    aux['children'] = aux_list;

                    hash_childrens[compact_slug] = aux_list
                    aux_root.push(aux);
                }


            }

        }


        /*var aux = {}
    aux['name'] = key;
    
    var aux2 = {}
    aux2['name'] = obj[key];
    aux['children'] = [aux2];
    d3_aux.push(aux);
    */


    }

    d3_result['children'] = d3_aux;
    console.log(hash_childrens);
    console.log(d3_result);

    return d3_result;
};

function json_to_table(obj) {
    var result = "<table class='table table-bordered table-hover'>";
    result += "<thead>";
    result += "<th>Tag</th>";
    result += "<th>Value</th>";
    result += "</thead>";
    result += "<tbody>";
    for (var key in obj) {

        result += "<tr><td>" + key + "</td>";
        result += "<td>" + obj[key] + "</td></tr>";

    }
    result += "</tbody>";
    result += "</table>";
    return result;

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
            return d.id || (d.id = ++i);
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

// Toggle children on click.
function click(d) {
    console.log(d);
    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
    update(d);
}

function color(d) {
    return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
}

function addTooltip(table_id) {
    if (isSafari()) {
        $('td', $(table_id)).each(function() {
            $(this).removeAttr("title");
        });
    } else {

        /* I decided to change this as this is was a very intensive process, 
            I instead tagged them, and add to the class the instance, this way i only have on instance per, table
            declaring a tooltip instance every td...*/
        $('td', $(table_id)).each(function() {
            var content = $(this).text().replace(/\s+/gi, ' ');
            if ($(this).textWidth() < $(this).width()) {
                $(this).removeClass('tooltipped');
            }
        });

        $('.tooltipped', $(table_id)).tooltip({
            container: "body",
            html: true
        });

    }
}

function isSafari() {
    if (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1) {
        return true;
    }
    return false;
}

function initializeQset(sortid) {
    var erec = new EmailRecognizer("#qs_"+sortid+" td");
    var results = erec.match();
    if (results > 0)
        erec.applyMasks();

    var lrec = new LinkRecognizer("#qs_"+sortid+" td.captioned_content");
    var results = lrec.match();
    if (results > 0)
        lrec.applyMasks();

    addTooltip('#t2_'+sortid);
    $('.captioned_content .summary_content', $('#t2_'+sortid)).expander({
        slicePoint: 68,
        expandText: 'more',
        userCollapseText: 'less'
    });
    // Add highlighting
    /*{% if request.session.query and not isAdvanced %}

            {% for word in request.session.query|whitespacesplit %}
                $('#set_container, .tooltip').highlight('{{word}}');
            {% endfor %}
        {% endif %}*/
    /*$('.comment_button', '#t2_{{qs.sortid}}').click(function(){
        $(this).parent().find('.comment_text').toggle('fast');
      });*/
    $('.comment_button', '#t2_'+sortid).popover({
        trigger: 'hover',
        html: true,
        template: '<div class="popover popover-medium"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
    });
}