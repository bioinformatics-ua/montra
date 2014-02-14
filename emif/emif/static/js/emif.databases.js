// emif.databases.js
// Works with templates/databases.html

// URL Hack to make paginator work with base
$(document).ready(function(){
    $('a[href="#"]').attr('href', function(i, val){
        return window.location + val;
    });
});

function post_to_url(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    //var form = document.createElement("form");
    var form = document.getElementById("send");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}


$(function() {

  // call the tablesorter plugin
  $("table").tablesorter({
    theme : 'blue',

    // sort on the first column and third column in ascending order
    sortList: [[0,0],[2,0]],

        // hidden filter input/selects will resize the columns, so try to minimize the change
    widthFixed : true,

    // initialize zebra striping and filter widgets
    widgets: ["zebra", "filter"]


  });

});

$('#li_workspace').addClass("active");

jQuery('#add_toolbar').click(function () {

$('#group_toolbar').addClass("open");
console.log($('#group_toolbar'))
});
