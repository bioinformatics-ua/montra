
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
function replaceall(str,replace,with_this)
{
    var str_hasil ="";
    var temp;

    for(var i=0;i<str.length;i++) // not need to be equal. it causes the last change: undefined..
    {
        if (str[i] == replace)
        {
            temp = with_this;
        }
        else
        {
                temp = str[i];
        }

        str_hasil += temp;
    }

    return str_hasil;
};

function getValueOfRadioButtoms(idOfTheStaff){


}


/***************** BEGIN - CHECK IF ANSWER IS FILLED IN *****************/
/* Function to validate for fields of type 1 (see comments below)*/
function validate1(val, id_answered, dirty_id_answered) {
                /* Tip from: http://viralpatel.net/blogs/jquery-get-text-element-without-child-element/ */
 
            var just_question = $('#question_'+id_answered)
        .clone().removeAttr('id')    //clone the element <- add to remove the id from the cloned element because ie7 crashes on duplicate ids
        .children() //select all the children
        .remove()   //remove all the children
        .end()  //again go back to selected element
        .text().trim();    //get the text of element
    var result = true;
    console.log(val);
    if(val != "" && val != undefined) {
            //console.log('1 - #answered_'+id_answered);
            $('[id="answered_'+id_answered+'"]').show();
            $('[id="answered_'+id_answered+'"]').addClass("hasValue");
            result = true;
        
            if (!(typeof bool_container === 'undefined')) {
                console.log('question_nr_'+id_answered);
                var number_correct = $('#question_nr_'+id_answered).text().trim();
                number_correct = number_correct.substring(0, number_correct.length-1);
                //console.log( number_correct);
                //console.log( $('#question_nr_'+id_answered).text().trim()+" "+just_question);
                //console.dir(':input[name="question_'+dirty_id_answered.replace('.','\\.')+'"]');
                
                if($(':input[name="question_'+replaceall(dirty_id_answered, '.','\\.')+'"]').is(':radio')){
                    bool_container.pushWithDelegate('question_nr_'+number_correct,
                    $('#question_nr_'+id_answered).text().trim()+" "+just_question,
                                   $(':input[name="question_'+replaceall(dirty_id_answered, '.','\\.')+'"]').val(), 'clear_selection("question_nr_'+replaceall(dirty_id_answered,'.','\\.')+'", "");');   
                } else {
                  bool_container.pushWithDelegate('question_nr_'+number_correct,
                    $('#question_nr_'+id_answered).text().trim()+" "+just_question,
                                   $(':input[name="question_'+replaceall(dirty_id_answered,'.','\\.')+'"]').val(), 'clearSimple("question_'+replaceall(dirty_id_answered,'.','\\.')+'");');       
                }
                
            }
        
        } else {
            //console.log('2 - #answered_'+id_answered);
            $('[id="answered_'+id_answered+'"]').hide();
            $('[id="answered_'+id_answered+'"]').removeClass("hasValue");
            result = false;
            var number_correct = $('#question_nr_'+id_answered).text().trim();
            number_correct = number_correct.substring(0, number_correct.length-1);
            if (!(typeof bool_container === 'undefined')) {
                bool_container.splice('question_nr_'+number_correct,
                    $('#question_nr_'+id_answered).text().trim()+" "+just_question,
                                   $('#question_'+replaceall(dirty_id_answered,'.','\\.')).val());
            }
        }
            // If we have a boolean container, maker

            return result;

}

// Clear a simple text field by his name
function clearSimple(id){
    $(':input[name="'+replaceall(id,'.','\\.')+'"]').val('');
    // Simulate change
    $(':input[name="'+replaceall(id,'.','\\.')+'"]').change();
}

//Creates an advanced validator for question fields.
var classNamePatternAUX = /type_(\S+)/i;
var advValidator = new Fingerprint_Validator();



function validateById(id_answered, id_answered_aux)
{

    var valueCounter = 0;
    


    /*
        - verify the type to each question and create a respective processment for each one
        TYPES:
        1 - open | open-button | open-upload-image | open-textfield | datepicker | range | timeperiod | publication
            choice-yesno | choice-yesnocomment | choice-yesnodontknow
        2 - choice | choice-freeform
        3 - choice-multiple-freeform | choice-multiple | choice-multiple-freeform-options
        None - comment | sameas | custom

    */
    if($('[id="qc_'+id_answered+'"]').hasClass('type_open') || $('[id="qc_'+id_answered+'"]').hasClass('type_open-button')
        || $('[id="qc_'+id_answered+'"]').hasClass('type_open-upload-image')
        || $('[id="qc_'+id_answered+'"]').hasClass('type_open-textfield')
        || $('[id="qc_'+id_answered+'"]').hasClass('type_publication')) {

        var myValue = $('[id="answered_'+id_answered_aux+'"]').parent().parent()[0].id;


        if (myValue!=undefined)
        {
        myValue = myValue.replace('acc_qc_', '');
        myValue = myValue.replace('qc_', '');

        var val = $('#question_' + replaceall(myValue, '.','\\.')).val();

        var r = validate1(val, id_answered_aux, id_answered);
        if (r)
            valueCounter = 1;
        else
            valueCounter = -1;
        }

    }
    if($('[id="qc_'+id_answered+'"]').hasClass('type_datepicker') || $('[id="qc_'+id_answered+'"]').hasClass('type_range')
        || $('[id="qc_'+id_answered+'"]').hasClass('type_timeperiod')
        ) {
        var myValue = $('[id="answered_'+id_answered_aux+'"]').parent().parent()[0].id;

         if (myValue!=undefined)
        {
        myValue = myValue.replace('acc_qc_', '');

        var val = $('#question_' + replaceall(myValue, '.','\\.')).val();

        var r = validate1(val, id_answered_aux, id_answered);

        if (r)
            valueCounter = 1;
        else
            valueCounter = -1;
        
        }

    }



     if($('[id="qc_'+id_answered+'"]').hasClass('type_choice')
         || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-freeform')
         || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-yesnodontknow')
        || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-yesnocomment')
        || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-yesno')
         ) {

         if ($('[name="question_'+id_answered+'"]').is(':checked')) {

             $('[id="answered_'+id_answered_aux+'"]').show();
             $('[id="answered_'+id_answered_aux+'"]').addClass("hasValue");
             valueCounter = 1;

         } else {
             $('[id="answered_'+id_answered_aux+'"]').hide();
              $('[id="answered_'+id_answered_aux+'"]').removeClass("hasValue");

             valueCounter = -1;

         }
    }

    if($('[id="qc_'+id_answered+'"]').hasClass('type_choice-multiple-freeform')
         || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-multiple')
         || $('[id="qc_'+id_answered+'"]').hasClass('type_choice-multiple-freeform-options')) {

         if ($('[id="answer_'+id_answered+'"] input[type="checkbox"]').is(':checked')) {
             $('[id="answered_'+id_answered_aux+'"]').show();
              $('[id="answered_'+id_answered_aux+'"]').addClass("hasValue");
             valueCounter = 1;

         } else {
            valueCounter = -1;
            $('[id="answered_'+id_answered_aux+'"]').hide();
              $('[id="answered_'+id_answered_aux+'"]').removeClass("hasValue");

         }
    }
    return valueCounter;
}

$(document).ready(function () {
    

    $('.answered').each(function (ans){ 
        var myId = $('.answered')[ans]['id'];
        var id_answered = myId.split("_")[1];
        var id_answered_aux = myId.split("_")[1].replace(/\./g,'');
        var toSum = $('[id="answered_'+id_answered_aux+'"]').is(':visible');
        id_answered = $('[id="answered_'+id_answered_aux+'"]').parent().parent()[0].id;

        id_answered = id_answered.replace('acc_qc_', '');

        //id_answered = id_answered.replace('.','\\.');
        id_answered = replaceall(id_answered, '.','\\.')
          


        var valueConter = validateById(id_answered, id_answered_aux);

        
    });

    advValidator.onInit();
    $(document).on('change', '.answer input,.answer select,.answer textarea, button', function (e) {
        e.preventDefault();



        var el = e.target;
        var id_answered = el.id.split("_")[1];
        var id_answered_aux = el.id.split("_")[1].replace(/\./g,'');
        var toSum = $('[id="answered_'+id_answered_aux+'"]').hasClass('hasValue');
        var qId = parseInt(id_answered[0]);


        //Detects widget class and sends it to the advanced validator.
        var className = $('[id="qc_'+id_answered+'"]').attr("class");
        className = classNamePatternAUX.exec(className)[1];
        if(className != undefined){
            advValidator.validate(className, id_answered, el);
        }
            

        var valueCounter = 0;
        
        //id_answered = id_answered.replace('.','\\.');
        id_answered = replaceall(id_answered, '.','\\.')

        valueCounter = validateById(id_answered.trim(), id_answered_aux.trim());
        var toSum2 = $('[id="answered_'+id_answered_aux+'"]').hasClass('hasValue');
        if (toSum && toSum2)
        {
            valueCounter = 0;
        }
        console.log('after'+valueCounter);
        /* Update Counter */ 
        questionSetsCounters[qId]['filledQuestions'] = questionSetsCounters[qId]['filledQuestions'] + valueCounter;
         var ui = new CounterUI();
         ui.updateCountersClean(qId);

    });

});
/***************** END - CHECK IF ANSWER IS FILLED IN *****************/
