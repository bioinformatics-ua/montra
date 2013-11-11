var getPlacement = function($el) {
    var offset = $el.offset(),
        top = offset.top,
        left = offset.left,
        height = $(document).outerHeight(),
        width = $(document).outerWidth(),
        vert = 0.5 * height - top,
        vertPlacement = vert > 0 ? 'bottom' : 'top',
        horiz = 0.5 * width - left,
        horizPlacement = horiz > 0 ? 'right' : 'left',
        placement = Math.abs(horiz) > Math.abs(vert) ?  horizPlacement : vertPlacement;
    return placement
};

function help_text_popover() {
    $('.qtext').each(function () {
        var $this = $(this);
        $this.popover({

            trigger: 'hover',
            placement: getPlacement($this),
            html: true,
            content: $this.find('.question-help-text').html()
//      content: 'body'
        });
    });
}


    /* Begin -- Check if user has unsaved changes */
 var formHasChanged = false;
 var submitted = true;
$(document).ready(function () {
    window.onbeforeunload = function (e) {
        if (formHasChanged && !submitted) {
            var message = "You have unsaved changes!", e = e || window.event;
            if (e) {
                e.returnValue = message;
            }
            return message;
        }
    }
 $(document).on('change', '#qform input, #qform select, #qform textarea', function (e) {
    formHasChanged = true;
    submitted = false;
});

 $("#qform").submit(function() {
     submitted = true;
     formHasChanged = false;
     });
});
/* End -- Check if user has unsaved changes */


/***************** BEGIN - CHECK IF ANSWER IS FILLED IN *****************/
/* Function to validate for fields of type 1 (see comments below)*/
function validate1(element, id_answered) {
    console.log("VAL: " + $(element).val());
    if($(element).val() != "") {
            console.log('1 - #answered_'+id_answered);
            $('[id="answered_'+id_answered+'"]').show();
        } else {
            console.log('2 - #answered_'+id_answered);
            $('[id="answered_'+id_answered+'"]').hide();
        }
}


$(document).ready(function () {
    $(document).on('change', '.answer input,.answer select,.answer textarea', function (e) {
        e.preventDefault();
        var el = e.target;
        var id_answered = el.id.split("_")[1];

        /*
            - verify the type to each question and create a respective processment for each one
            TYPES:
            1 - open | open-button | open-upload-image | open-textfield | datepicker | range | timeperiod
            2 - choice | choice-yesno | choice-yesnocomment | choice-yesnodontknow | choice-multiple | choice-multiple-freeform | choice-freeform
            3 -
            4 -     publication
            None - comment | sameas | custom

        */
        if($('[id="qc_'+id_answered+'"]').hasClass('type_open') || $('[id="qc_'+id_answered+'"]').hasClass('type_open-button')
            || $('[id="qc_'+id_answered+'"]').hasClass('type_open-upload-image') || $('[id="qc_'+id_answered+'"]').hasClass('type_open-textfield')) {
//            console.log('OPEN - #qc_'+ id_answered);
            validate1(this, id_answered);
        }

        if($('[id="qc_'+id_answered+'"]').hasClass('type_datepicker') || $('[id="qc_'+id_answered+'"]').hasClass('type_range')
            || $('[id="qc_'+id_answered+'"]').hasClass('type_timeperiod')) {
//            console.log('DATEPICKER - #qc_'+ id_answered);
            validate1(this, id_answered);
        }

         if($('[id="qc_'+id_answered+'"]').hasClass('type_choice-yesnodontknow') || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-yesno')
             || $('[id="qc_'+id_answered+'"]').hasClass('type_choice')
             || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-freeform')) {
//            console.log('CHOICE - #qc_'+ id_answered);


             if ($('[name="question_'+id_answered+'"]').is(':checked')) {
                 console.log('1 - #answered_'+id_answered);
                 $('[id="answered_'+id_answered+'"]').show();
             } else {
                   console.log('2 - #answered_'+id_answered);
                    $('[id="answered_'+id_answered+'"]').hide();
             }
        }

        if($('[id="qc_'+id_answered+'"]').hasClass('type_choice-multiple-freeform')
             || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-multiple')) {
//            console.log('CHOICE - #qc_'+ id_answered);

             console.log($('div[id="qc_'+id_answered+'"] input[type="checkbox"]').is(':checked'));
//                validate1($('[name="question_'+id_answered+'"]'), id_answered);

             if ($('div[id="qc_'+id_answered+'"] input[type="checkbox"]').is(':checked')) {
                 console.log('1 - #answered_'+id_answered);
                 $('[id="answered_'+id_answered+'"]').show();
             } else {
                  console.log('2 - #answered_'+id_answered);
                    $('[id="answered_'+id_answered+'"]').hide();
             }
        }

        /************************************************************************************/

    });
});
/***************** END - CHECK IF ANSWER IS FILLED IN *****************/
