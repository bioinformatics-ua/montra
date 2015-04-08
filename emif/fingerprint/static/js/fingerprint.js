/*
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
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
        placement = Math.abs(horiz) > Math.abs(vert) ? horizPlacement : vertPlacement;
    return placement;
};

    function help_text_popover() {
        $('.qtext').each(function() {
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
$(document).ready(function() {
    window.onbeforeunload = function(e) {
        if (formHasChanged && !submitted) {
            var message = "You have unsaved changes!",
                e = e || window.event;
            if (e) {
                e.returnValue = message;
            }
            return message;
        }
    }
    $(document).on('change', '[id^="qform"] input, [id^="qform"] select, [id^="qform"] textarea', function(e) {
        formHasChanged = true;
        submitted = false;
    });

    $('[id^="qform"]').submit(function() {
        submitted = true;
        formHasChanged = false;
    });
});

function replaceall(str, replace, with_this) {
    return str.replace(/\./g, '\\.')

};




/***************** BEGIN - CHECK IF ANSWER IS FILLED IN *****************/
/* Function to validate for fields of type 1 (see comments below)*/
function validate1(element, id_answered, dirty_id_answered, self_validated) {
    /* Tip from: http://viralpatel.net/blogs/jquery-get-text-element-without-child-element/ */

    var just_question = $('#question_' + id_answered)
        .clone().removeAttr('id') //clone the element <- add to remove the id from the cloned element because ie7 crashes on duplicate ids
    .children() //select all the children
    .remove() //remove all the children
    .end() //again go back to selected element
    .text().trim(); //get the text of element
    var result = true;
    if ( self_validated === 1 || ($(element).val() != "" && self_validated === undefined)) {
        //console.log('1 - #answered_'+id_answered);
        $('[id="answered_' + id_answered + '"]').show();
        $('[id="answered_' + id_answered + '"]').addClass("hasValue");
        result = true;

        if (!(typeof bool_container === 'undefined')) {
            var number_correct = $('#question_nr_' + id_answered).text().trim();

            number_correct = number_correct.substring(0, number_correct.length - 1);
            //console.log( number_correct);
            //console.log( $('#question_nr_'+id_answered).text().trim()+" "+just_question);
            //console.dir(':input[name="question_'+dirty_id_answered.replace('.','\\.')+'"]');
            var dirty = dirty_id_answered;

            if ($(':input[name="question_' + dirty + '"]').is(':radio')) {
                bool_container.pushWithDelegate('question_nr_' + number_correct,
                    $('#question_nr_' + id_answered).text().trim() + " " + just_question,
                    $(':input[name="question_' + dirty + '"]').val(), 'clear_selection("question_nr_' + dirty + '", "");');
            } else if($('select[name="question_' + dirty + '"]').prop('type') == 'select-one') {
                bool_container.pushWithDelegate('question_nr_' + number_correct,
                    $('#question_nr_' + id_answered).text().trim() + " " + just_question,
                    $('select[name="question_' + dirty + '"]').val(), 'clear_selection("question_nr_' + dirty + '", "");');
            } else {
                bool_container.pushWithDelegate('question_nr_' + number_correct,
                    $('#question_nr_' + id_answered).text().trim() + " " + just_question,
                    $(':input[name="question_' + dirty + '"]').val(), 'clearSimple("question_' + dirty + '");');
            }

        }

    } else {
        //console.log('2 - #answered_'+id_answered);
        $('[id="answered_' + id_answered + '"]').hide();
        $('[id="answered_' + id_answered + '"]').removeClass("hasValue");
        result = false;
        var number_correct = $('#question_nr_' + id_answered).text().trim();
        number_correct = number_correct.substring(0, number_correct.length - 1);
        if (!(typeof bool_container === 'undefined')) {
            var dirty = dirty_id_answered.replace(/\./g, '\\.');

            bool_container.splice('question_nr_' + number_correct,
                $('#question_nr_' + id_answered).text().trim() + " " + just_question,
                $('#question_' + dirty).val());
        }
    }
    // If we have a boolean container, maker

    return result;

}

// Clear a simple text field by his name
function clearSimple(id) {
    $(':input[name="' + id.replace(/\./g, '\\.') + '"]').val('');
    // Simulate change
    $(':input[name="' + id.replace(/\./g, '\\.') + '"]').change();
}

//Creates an advanced validator for question fields.
var classNamePatternAUX = /type_(\S+)/i;
var advValidator = new Fingerprint_Validator();



function validateById(id_answered, id_answered_aux) {
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
    var qc_id = $('[id="qc_' + id_answered + '"]');

    if (qc_id.hasClass('type_open') || qc_id.hasClass('type_open-validated')
        || qc_id.hasClass('type_open') || qc_id.hasClass('type_email') || qc_id.hasClass('type_url') ||
        qc_id.hasClass('type_numeric')
        || qc_id.hasClass('type_open-button') || qc_id.hasClass('type_open-upload-image') || qc_id.hasClass('type_open-textfield') || qc_id.hasClass('type_publication')) {
        var myValue = $('[id="answered_' + id_answered_aux + '"]').parent().parent()[0].id;

        var old_value;

        if (myValue != undefined) {
            myValue = myValue.replace('acc_qc_', '');
            myValue = myValue.replace('qc_', '');

            var val = $(':input[name="question_' + myValue.replace(/\./g, '\\.') + '"]');

            var self_validated;
            if(qc_id.hasClass('type_open-validated')){
                var inp = $(':input[name="question_' + id_answered + '"]');

                var comp = inp.inputmask("isComplete");
                if(comp){
                    $('[id="answered_' + id_answered_aux + '"]').show();
                    $('[id="answered_' + id_answered_aux + '"]').addClass("hasValue");

                    self_validated = 1;
                } else {
                    $('[id="answered_' + id_answered_aux + '"]').hide();
                    $('[id="answered_' + id_answered_aux + '"]').removeClass("hasValue");

                    self_validated = -1;
                }
            }
            var r = validate1(val, id_answered_aux, id_answered, self_validated);
            if (r)
                valueCounter = 1;
            else
                valueCounter = -1;

        }

    } else if (qc_id.hasClass('type_datepicker') || qc_id.hasClass('type_range') || qc_id.hasClass('type_timeperiod')) {

        var myValue = $('[id="answered_' + id_answered_aux + '"]').parent().parent()[0].id;



        if (myValue != undefined) {
            myValue = myValue.replace('acc_qc_', '');

            if(qc_id.hasClass('type_datepicker')){
                var value = $('[id="question_'+myValue+'"]').val();
                value = value.replace('mm','01');
                value = value.replace(/y/g,'0');
                value = value.replace('dd','01');
                $('[id="question_'+myValue+'"]').val(value);
            }
            var val = $(':input[name="question_' + myValue.replace(/\./g, '\\.') + '"]');

            var r = validate1(val, id_answered_aux, id_answered);

            if (r)
                valueCounter = 1;
            else
                valueCounter = -1;

        }

    } else if (qc_id.hasClass('type_choice') || qc_id.hasClass('type_choice-freeform') || qc_id.hasClass('type_choice-yesnodontknow') || qc_id.hasClass('type_choice-yesnocomment') || qc_id.hasClass('type_choice-yesno')) {

        var element = $('[name="question_' + id_answered + '"]');

        if( element.prop('type') == 'select-one' ) {
            var valchoosen = element.val();

            if(valchoosen == ''){
                $('[id="answered_' + id_answered_aux + '"]').hide();
                $('[id="answered_' + id_answered_aux + '"]').removeClass("hasValue");
                valueCounter = -1;
            } else {
                $('[id="answered_' + id_answered_aux + '"]').show();
                $('[id="answered_' + id_answered_aux + '"]').addClass("hasValue");
                valueCounter = 1;
            }
        } else {
            if ($('[name="question_' + id_answered + '"]').is(':checked')) {

                $('[id="answered_' + id_answered_aux + '"]').show();
                $('[id="answered_' + id_answered_aux + '"]').addClass("hasValue");
                valueCounter = 1;

            } else {
                $('[id="answered_' + id_answered_aux + '"]').hide();
                $('[id="answered_' + id_answered_aux + '"]').removeClass("hasValue");

                valueCounter = -1;

            }
        }
        // I need this call because i hookup the answer to the boolean plugin here.
        if (!(typeof bool_container === 'undefined')) {
            validate1($('[name="question_' + id_answered + '"]'), id_answered_aux, id_answered);
        }
    } else if (qc_id.hasClass('type_choice-multiple-freeform') || qc_id.hasClass('type_choice-multiple') || qc_id.hasClass('type_choice-multiple-freeform-options')) {

        if ($('[id="answer_' + id_answered + '"] input[type="checkbox"]').is(':checked')) {
            $('[id="answered_' + id_answered_aux + '"]').show();
            $('[id="answered_' + id_answered_aux + '"]').addClass("hasValue");
            valueCounter = 1;

        } else {
            valueCounter = -1;
            $('[id="answered_' + id_answered_aux + '"]').hide();
            $('[id="answered_' + id_answered_aux + '"]').removeClass("hasValue");

        }
    }

    return valueCounter;
}

$(document).ready(function() {
    $('.answered').each(function(ans) {

        var myId = this.id;
        var id_answered = myId.split("_")[1];
        var id_answered_aux = myId.split("_")[1].replace(/\./g, '');

        var toSum = $('[id="answered_' + id_answered_aux + '"]').is(':visible');
        id_answered = $('[id="answered_' + id_answered_aux + '"]').parent().parent()[0].id;

        id_answered = id_answered.replace('acc_qc_', '');

        id_answered = id_answered.replace('qc_', '');

        //console.log("ID_ANSWERED: " + id_answered);
        // Since were using name="" as selector, we dont need to do the escaping
        //id_answered = id_answered.replace('.','\\.');
        //id_answered = replaceall(id_answered, '.','\\.')



        var valueConter = validateById(id_answered, id_answered_aux);


    });

    function endsWith(str, suffix) {
        if(str)
            return str.indexOf(suffix, str.length - suffix.length) !== -1;

        return false;
    }
    advValidator.onInit();

    $(document).on('change', '.answer input, .answer select,.answer textarea', function(e) {
        e.preventDefault();

        if($(this).hasClass('commentary')){
            var qid = $(this).data('qid');
            var is_empty = ($(this).val().trim() === "");

            if(is_empty){
                $('#commentary_'+qid).html('<i class="icon-comment-alt">&nbsp;</i>');
            } else {
                $('#commentary_'+qid).html('<i class="icon-comment">&nbsp;</i>');
            }
            return;
        }

        if (endsWith($(this).attr('id'), "_opt") || endsWith($(this).attr('id'), "_ignoreme_"))
            return false;

        var el = e.target;

        if(!el.id)
            return;

        var id_answered = el.id.split("_")[1];
        var id_answered_aux = el.id.split("_")[1].replace(/\./g, '');
        var toSum = $('[id="answered_' + id_answered_aux + '"]').hasClass('hasValue');

        var qId = parseInt(id_answered);

        //Detects widget class and sends it to the advanced validator.
        try{
            var className = $('[id="qc_' + id_answered + '"]').attr("class");
            className = classNamePatternAUX.exec(className)[1];
            if (className != undefined) {
                advValidator.validate(className, id_answered, el);
            }
        } catch(err){
            console.warn("There was a error validating a field.");
        }

        var valueCounter = 0;

        // Since were using name="" as selector, we dont need to do the escaping
        //id_answered = id_answered.replace('.','\\.');
        //id_answered = id_answered.replace(/\./g,'\\.');


        valueCounter = validateById(id_answered.trim(), id_answered_aux.trim());

        var possible_change = 0;

        var handleChanges = function(){

            if(typeof depmap === 'object'){
                if(depmap[old]){
                    possible_change -= depmap[old];
                }
                if(depmap[newvalue]){
                    possible_change += depmap[newvalue];
                }
            }

            $('[name="'+$(el).attr('name')+'"]').data('old', newvalue);
        };
        if($(el).attr('type') =='radio'){

            var depmap = depmaps[id_answered];
            var old = $(el).data('old');

            var newvalue = $('[name="'+$(el).attr('name')+'"]:checked').val();

            handleChanges(depmap, old, newvalue);

        } else if($(el).prop('type') == 'select-one'){
            var depmap = depmaps[id_answered];
            var old = $(el).data('old');
            var newvalue = $('[name="'+$(el).attr('name')+'"]').val();

            handleChanges(depmap, old, newvalue);
        }
        else {
            $(el).data('old', $(el).val());
        }
        if (!(typeof questionSetsCounters === 'undefined')) {
            var toSum2 = $('[id="answered_' + id_answered_aux + '"]').hasClass('hasValue');
            if (toSum && toSum2) {
                valueCounter = 0;
            }
            /* Update Counter */
            try{
                var cc = new CounterCore(qId);


                //questionSetsCounters[qId]['filledQuestions'] = questionSetsCounters[qId]['filledQuestions'] + valueCounter;
                questionSetsCounters[qId]['filledQuestions'] = cc.countFilledQuestionSet(qId);
                questionSetsCounters[qId]['count'] = questionSetsCounters[qId]['count']+possible_change

                var ui = new CounterUI();
                ui.updateCountersClean(qId);
            } catch(err){
                console.warn("Tried to update a non tracked input");
            }
        }


    });
});

function tabindexer(){
var index=1;
$('input').each(function(){
$(this).attr('tabindex',index++);
});
}

function toggle_comments(question_number)
{
$("#comments_"+question_number).toggle();
}

/***************** END - CHECK IF ANSWER IS FILLED IN *****************/
