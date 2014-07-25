var MAX_RESULTS = 10;

function showExportMessage(){
    $('#exporting-message').fadeIn('fast');


// Validation of quicksearch
$('#quicksearch').submit(function() {

        var quick_search = $('#edit-search-block-form--3', $(this)).val().trim();

        if(!quick_search || quick_search.length == 0)
            return false;

        return true;
});

    setTimeout(function() {
      $('#exporting-message').fadeOut('fast');  
    }, 4000);
}
var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    i=0;
    $.each(strs, function(i, str) {

      if(i>MAX_RESULTS)
        return false;

      if (substrRegex.test(str.query)) {
        // the typeahead jQuery plugin expects suggestions to a
        // JavaScript object, refer to typeahead docs for more info
        matches.push({ value: str.query });
      }
      i++;
    });

    cb(matches);
  };
};
$(function(){
    if ($(".search-query").length > 0){
        $('.search-query').canclear();
    }

    handleQuickSearch();
});

function handleQuickSearch(){
    $.get('api/searchsuggestions').done(function(data) {
        if(data.suggestions){
            $('.search-query').typeahead({
              hint: true,
              highlight: true,
              minLength: 1
            },
            {
              name: 'queries',
              source: substringMatcher(data.suggestions),
            });
        }
      })
}