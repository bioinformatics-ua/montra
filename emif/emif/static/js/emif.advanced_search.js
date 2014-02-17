//##########################IMPORTANT
advValidator.searchMode(true);
//###################################

$(".chosen-select").chosen({max_selected_options: 5});

$(function(){
    bool_container = $('#bool_container').boolrelwidget({form_anchor: '#qform'});

    if (!(typeof bool_container === 'undefined')) {
        $('#qform').submit(
                     
                    function(e) {

                        // Update hidden inputs (in case they are not updated because we are using the other buttons not in control by the plugin)
                        bool_container.readyToSubmit(); 
                    }     
        );
    }
});


