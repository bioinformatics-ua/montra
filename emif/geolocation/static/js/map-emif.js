confs = {
    icon: '<i class="fa fa-smile-o"></i>',
    name: "Vector map",
    width: 6,
    height: 2,
    extracss: [
        "{{STATIC_URL}}css/jquery-jvectormap-2.0.2.css",
        "{{STATIC_URL}}css/bootstrap-dropdown-checkbox.css"]
    ,
    extralibs: [
        "{{STATIC_URL}}js/jquery-jvectormap-2.0.2.min.js",
        "{{STATIC_URL}}js/jsMapsApi.js",
        "{{STATIC_URL}}js/bootstrap-dropdown-checkbox.js"
        ]
};

numReg = 0;
finalDeps = "";

plugin = function(sdk){

    // access the Polymer custom tags and vector map data from the services
    $.when(
        $.get("developer/file/2c5f467829adbe6a060b093445c5991e/1/polymer-micro.html"),
        $.get("developer/file/2c5f467829adbe6a060b093445c5991e/1/polymer-mini.html"),
        $.get("developer/file/2c5f467829adbe6a060b093445c5991e/1/polymer.html"),
        $.get("static/html/vector-map.html"))
        // $.get("static/html/filter-box.html"))
            .done(function(dep1, dep2, dep3, dep4) {


            deps = "";
            if(numReg==0)
            {
                // Polymer deps + custom tag definition
                deps = dep1[0]
                deps += dep2[0]
                deps += dep3[0]
                deps += dep4[0]
                finalDeps = deps;
            }
            else if(numReg==1)
            {
                // open the "box"
                deps += '<div class="container-fluid" style="height:100%">';

                // markers - pass a link to the URL responsible of returning the JSON file
                deps += '<div class="starter-template col-sm-12 col-md-12" style="height:300px">'+
            			'<vector-map style="height:300px; width:100px" id="my_map_3" map_type="world_mill_en" min_color="#2cb5d4" max_color="#153478"'+
                        'min_radius=5 max_radius=15 background_color="#666666" folder="static/" markers="api/vectormap"></vector-map>'+
            		    '</div>';

                // add as well the filter box
                /*
                deps += '<div class="starter-template col-sm-2 col-md-6">' +
    			        '<filter-box id="my-fbox" filters="./static/tests/json/test-filters.json"'+
                        'type="input" map="my_map_3"></filter-box>' +
                        '</div>';
                */


                // close the "box"
                deps += '</div>'
                finalDeps += deps
            }


            /*
            // countries - pass a link to the URL responsible of returning the JSON file
            deps += '<div class="starter-template col-sm-10 col-md-6" style="height:100%">'+
        			'<vector-map style="height:300px; width:100px" id="my_map_1" map_type="world_mill_en" min_color="#2cb5d4" max_color="#153478"'+
                    'min_radius=5 max_radius=15 background_color="#666666" folder="static/" countries="api/vectormap"></vector-map>'+
        		    '</div>';
            */



            numReg++;
            if(numReg==1)
            {
                console.log('Numreg is 1')
                sdk.html(finalDeps);
                sdk.refresh();
            }
            else {
                console.log('Numreg is 2')
                sdk.html(deps);
                sdk.refresh();
            }
    });
};
