$(function(){
    $('#schemas').dataTable({
        "oLanguage": {
            "sEmptyTable": "<center>No schemas found</center>"
        },
        "aoColumnDefs" : [
            {
                'bSortable' : false,
                'aTargets' : [1]
            }
        ],
        "order": [[ 0, "asc" ]]
    });
});
