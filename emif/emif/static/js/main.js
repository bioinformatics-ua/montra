
// Validation of quicksearch
$('#quicksearch').submit(function() {

        var quick_search = $('#edit-search-block-form--3', $(this)).val().trim();

        if(!quick_search || quick_search.length == 0)
            return false;

        return true;
});