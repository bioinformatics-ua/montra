confs = {
    icon: '<i class="icon-book"></i>',
    name: "Literature",
    extralibs: ["//bioinformatics.ua.pt/becas/embed-widget.js", "{{STATIC_URL}}js/jquery.simplePagination.js"]
};

plugin = function(sdk){
    this_sdk = sdk;

    var per_page=10;
    var publications=[];
    var this_sdk;
    var context;

    function initializeBecas(pmid, container){
        var becasWidget2;

        // Initialize another widget
        becasWidget2 = new becas.Widget({
            container: container
        });
        // Request abstract annotation by PMID
        becasWidget2.annotatePublication({
            // required parameter
            pmid: pmid,
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
            success: function() {
                // Everything went fine, widget is rendered.
            },
            error: function(err) {
                // An error prevented annotation, an error message has rendered.
            }
        });
    }

    function collapser() {

        if ($(this).text().indexOf('Collapse') !== -1) {
        console.log(collapser);
            expanded = false;
            $(this).html('<i class="icon-plus"></i>&nbsp; Expand all');
            //change_name_collapse(false);

            $(".collapse", context).collapse("hide");

        } else {
            expanded = true;
            $(this).html('<i class="icon-minus"></i>&nbsp; Collapse all');
            //change_name_collapse(true);
            $(".collapse", context).collapse("show");
        }
    }

    function disableLinks(){
        $('.edit_paginator .page-link', context).click(function(event){
             event.preventDefault();
             return false;
        });
    }
    function redrawIndicator(start, end){
        $('.showing_publications_info', context).html("Showing "+(start+1)+" - "+end+" of "+publications.length+" Publications");
    }

    function showPublicationPage(pageNumber){
        console.log(context);
        var start = (pageNumber-1)*per_page;
        var end = ((pageNumber-1)*per_page)+per_page;

        // If last page and end is bigger than results
        if (end > publications.length){
            end = publications.length;
        }

        console.log("start:"+start+" end: "+end);

        $('.pubscontainer', context).html('<button id="collapseliterature" class="btn pull-right" href=""><i class="icon-plus"></i>&nbsp; Expand all</button><div class="clearfix accordion fullwidth" id="accordion2" style="margin-top: 10px;">');
        var pub, i;
        for(var i=start;i<end;i++){
            pub = publications[i];

            $('.pubscontainer', context).append(
                '<div class="accordion-group">\
                    <div class="accordion-heading">\
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+i+'">\
                           '+pub.title+'\
                        </a>\
                    </div>\
                    <div id="collapse'+i+'" class="accordion-body collapse">\
                        <div class="accordion-inner">\
                            <div id="becaswidget-'+pub.pmid+'"></div>\
                        </div>\
                    </div>\
                </div>'
            );
        }

        $('.pubscontainer', context).append('</div>');
        for(var i=start;i<end;i++){
            pub = publications[i];
            initializeBecas(pub.pmid, "becaswidget-"+pub.pmid);
        }

        $('#collapseliterature', context).click(collapser);

        disableLinks();
        redrawIndicator(start, end);
    }

    function handlePagination(pageNumber, event){
        showPublicationPage(pageNumber)
    }

    var empty_message = '\
    <h4 class="pull-center">No publications associated with this database.</h4>\
    <p class="pull-center">Publications added to this database, will appear here accompanied with annotations.</p>\
    ';
    sdk.html('Loading');
    sdk.refresh();
    context = sdk.container();

    var fp = FingerprintProxy.getInstance();
    var store = fp.getStore();

    store.getPublications().then(function(response){
        if(response.publications && response.publications.length > 0){
            publications = response.publications;

            sdk.html('<div class="pubscontainer"></div>\
                <div class="showing_publications_info"></div>\
                <div class="pull-right edit_paginator pagination">\
            </div>');
            sdk.refresh();
            $('.edit_paginator', context).pagination({
                items: publications.length,
                itemsOnPage: per_page,
                onPageClick: handlePagination
            });

            showPublicationPage(1);

        } else {
            sdk.html(empty_message);
            sdk.refresh();
        }
    }).catch(function(ex){
        console.log(ex);
        sdk.html('Error getting publications');
        sdk.refresh();
    });

};
