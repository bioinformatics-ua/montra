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

$("#collapseall_literature").bind('click', function(e) {
    //e.preventDefault(); 
    //e.stopPropagation();

    collapse_expand(this);

    return false;
});