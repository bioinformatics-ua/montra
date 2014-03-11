/******* Database info specific Javascript ****/
//<!--&lt;!&ndash; Use the widgets &ndash;&gt;-->
// Initialize widget
var becasWidget;
var becasWidget2;
// We must check becas exists, because the import the way it exists, may fail
if(!(typeof becas === 'undefined')){
    becasWidget = new becas.Widget({
        container: 'becas-widget-text'
    });
    // Request text annotation
    becasWidget.annotateText({
        // required parameter
        text: 'In Duchenne muscular dystrophy (DMD), the infiltration of skeletal muscle by immune cells aggravates disease, yet the precise mechanisms behind these inflammatory responses remain poorly understood. Chemotactic cytokines, or chemokines, are considered essential recruiters of inflammatory cells to the tissues.\nWe assayed chemokine and chemokine receptor expression in DMD muscle biopsies (n = 9, average age 7 years) using immunohistochemistry, immunofluorescence, and in situ hybridization.\nCXCL1, CXCL2, CXCL3, CXCL8, and CXCL11, absent from normal muscle fibers, were induced in DMD myofibers. CXCL11, CXCL12, and the ligand-receptor couple CCL2-CCR2 were upregulated on the blood vessel endothelium of DMD patients. CD68(+) macrophages expressed high levels of CXCL8, CCL2, and CCL5.\nOur data suggest a possible beneficial role for CXCR1/2/4 ligands in managing muscle fiber damage control and tissue regeneration. Upregulation of endothelial chemokine receptors and CXCL8, CCL2, and CCL5 expression by cytotoxic macrophages may regulate myofiber necrosis.',
        // optional parameters
        groups: {
            "SPEC": true,
            "ANAT": true,
            "DISO": true,
            "PATH": true,
            "CHED": true,
            "ENZY": true,
            "MRNA": true,
            "PRGE": true,
            "COMP": true,
            "FUNC": true,
            "PROC": true
        },
        success: function () {
            // Everything went fine, widget is rendered.
        },
        error: function (err) {
            // An error prevented annotation, an error message has rendered.
        }
    });

    // Initialize another widget
    becasWidget2 = new becas.Widget({
        container: 'becas-widget-pmid'
    });
    // Request abstract annotation by PMID
    becasWidget2.annotatePublication({
        // required parameter
        pmid: 23225384,
        // optional parameters
        groups: {
            "SPEC": true,
            "ANAT": true,
            "DISO": true,
            "PATH": true,
            "CHED": true,
            "ENZY": true,
            "MRNA": true,
            "PRGE": true,
            "COMP": true,
            "FUNC": true,
            "PROC": true
        },
        success: function () {
            // Everything went fine, widget is rendered.
        },
        error: function (err) {
            // An error prevented annotation, an error message has rendered.
        }
    });
}
$('#li_workspace').addClass("active");

$("#btn_pivot_table").bind('click', function (e) {
    $("#pivot_table_extra_information").toggle();
    $("#chart").toggle();

    if ($('#btn_pivot_table').text() == 'Pivot table') {
        $('#btn_pivot_table').text('Tree view');
    } else {
        $('#btn_pivot_table').text('Pivot table');
    }
    return false;
});
$("#collapseall_metadata").bind('click', function (e) {
    e.preventDefault();
    e.stopPropagation();

    var div_id = 'accordion1';
    collapseAll($("#collapseall_metadata"), div_id);

});
$("#collapseall_literature").bind('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    var div_id = 'accordion2';
    collapseAll($("#collapseall_literature"), div_id);

});

function collapseAll(element, div_id) {
    if (element.text().indexOf('Collapse') !== -1) {
        console.log('Collapse all');
        element.text('Expand all');
        if (!element.hasClass('disabled')) {
            element.parents().find('#' + div_id + ' .collapse').each(function (index) {
                $(this).addClass('in');
                $(this).collapse('hide');
            });
        }
    } else {
        console.log('Expand all');
        element.text('Collapse all');
        if (!element.hasClass('disabled')) {
            element.parents().find('#' + div_id + ' .collapse').each(function (index) {
                $(this).removeClass('in');
                $(this).collapse('show');
            });
        }
    }
}

$('.popover').popover({
    container: 'body'
});

$.fn.textWidth = function () {
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
    .projection(function (d) {
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
    nodes.forEach(function (n, i) {
        n.x = i * barHeight;
    });

    // Update the nodes…
    var node = vis.selectAll("g.node")
        .data(nodes, function (d) {
            return d.id || (d.id = ++i);
        });

    var nodeEnter = node.enter().append("svg:g")
        .attr("class", "node")
        .attr("transform", function (d) {
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
        .text(function (d) {
            return d.name;
        });

    // Transition nodes to their new position.
    nodeEnter.transition()
        .duration(duration)
        .attr("transform", function (d) {
            return "translate(" + d.y + "," + d.x + ")";
        })
        .style("opacity", 1);

    node.transition()
        .duration(duration)
        .attr("transform", function (d) {
            return "translate(" + d.y + "," + d.x + ")";
        })
        .style("opacity", 1)
        .select("rect")
        .style("fill", color);

    // Transition exiting nodes to the parent's new position.
    node.exit().transition()
        .duration(duration)
        .attr("transform", function (d) {
            return "translate(" + source.y + "," + source.x + ")";
        })
        .style("opacity", 1e-6)
        .remove();

    // Update the links…
    var link = vis.selectAll("path.link")
        .data(tree.links(nodes), function (d) {
            return d.target.id;
        });

    // Enter any new links at the parent's previous position.
    link.enter().insert("svg:path", "g")
        .attr("class", "link")
        .attr("d", function (d) {
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
        .attr("d", function (d) {
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
    nodes.forEach(function (d) {
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
function addTooltip(table_id){
    if(isSafari()){
    $('td', $(table_id)).each(function () {
        $(this).removeAttr("title");
    });               
    } else {
        /* I decided to change this as this is was a very intensive process, 
            I instead tagged them, and add to the class the instance, this way i only have on instance per, table
            declaring a tooltip instance every td...*/
        $('td', $(table_id)).each(function () {
            var content = $(this).text().replace(/\s+/gi, ' ');
            if ($(this).textWidth() > $(this).width()) {
                $(this).addClass('tooltipped');
            }
        });  

        $('.tooltipped', $(table_id)).tooltip({container: "body",html: true});

    }
}    
function isSafari() {
    if (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1) {
        return true;
    }
    return false;
}