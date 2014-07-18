var qvalues = new Array(); // used as dictionary
var qtriggers = new Array();

function dep_check(expr) {
    var exprs = expr.split(",", 2);
    var qnum = exprs[0];
    var value = exprs[1];
    var qvalue = qvalues[qnum];
    if (value.substring(0, 1) == "!") {
        var multiple_option = qvalues[qnum + '_' + value.substring(1)];
        if (multiple_option != undefined)
            return !multiple_option;
        value = value.substring(1);
        return qvalue != value;
    }
    if (value.substring(0, 1) == "<") {
        qvalue = parseInt(qvalue);
        if (value.substring(1, 2) == "=") {
            value = parseInt(value.substring(2));
            return qvalue <= value;
        }
        value = parseInt(value.substring(1));
        return qvalue < value;
    }
    if (value.substring(0, 1) == ">") {
        qvalue = parseInt(qvalue);
        if (value.substring(1, 2) == "=") {
            value = parseInt(value.substring(2));
            return qvalue >= value;
        }
        value = parseInt(value.substring(1));
        return qvalue > value;
    }
    var multiple_option = qvalues[qnum + '_' + value];
    if (multiple_option != undefined) {
        return multiple_option;
    }
    if (qvalues[qnum] == value) {
        return true;
    }
    return false;
}

function collapseAll(element, div_id) {
    if (element.text().indexOf('Collapse') !== -1) {
        console.log('Collapse all');
        element.text('Expand all');
        if (!element.hasClass('disabled')) {
            element.parents().find('#' + div_id + ' .collapse').each(function(index) {
                $(this).addClass('in');
                $(this).collapse('hide');
            });
        }
    } else {
        console.log('Expand all');
        element.text('Collapse all');
        if (!element.hasClass('disabled')) {
            element.parents().find('#' + div_id + ' .collapse').each(function(index) {
                $(this).removeClass('in');
                $(this).collapse('show');
            });
        }
    }
};

function getChecksAttr(obj) {
    /* while most browser consider getAttributes a function, IE 9< considers it a object
     * So its actually better to use jquery for this
    return obj.getAttribute('checks'); */
    var $obj = $(obj);
    return $obj.attr('checks');
}

function statusChanged(obj, res) {
    if (obj.tagName == 'DIV') {
        obj.style.display = !res ? 'none' : 'block';
        return;
    }
    //obj.style.backgroundColor = !res ? "#eee" : "#fff";
    obj.disabled = !res;
}

function clearcheck(id) {
    console.warn('clearcheck ID: ' + id);
    $(':input[name="' + id + '"]').removeAttr('checked');
    //$(':input[name="'+id+'"]').click();
}

function valchanged(qnum, value, self) {
    if (!(typeof bool_container === 'undefined')) {
        var $self = $(self);

        var just_number = qnum.split('_')[1];
        var clean = qnum.replace('question_', '').replace(/(\\)/g, '');
        var dirty = qnum.replace('question_', '').replace('_', ':');
        var index = dirty.indexOf(':');

        // We have to get the question
        var the_question = $('#question_' + clean.split('_')[0].replace(/(\.)/g, '')).text().trim();
        if (value == true) {

            //console.log(qnum);
            //console.log(clean.replace('_','. ')+' ('+the_question+')');
            //console.log(value);

            //var optional = $('#question_'+clean.split('_')[0].replace(/(\.)/g,'')).closest('input[type="text"]');
            //console.log(optional.attr('id'));

            //var optional = $('#question_'+just_number.replace(/(\.)/g,'\\.')+"_1_opt").val();
            bool_container.pushWithDelegate('question_nr_' + dirty.substring(0, index) + "_____" + clean + "_____",
                clean.replace('_', '. ') + ' (' + the_question + ')', dirty.substring(index + 1, dirty.length), 'clearcheck("' + $self.attr('id') + '");');
        } else if (value == false) {
            var optional = $('#question_' + just_number.replace(/(\.)/g, '') + "_opt").val();
            bool_container.splice('question_nr_' + dirty.substring(0, index) + "_____" + clean + "_____",
                clean.replace('_', '. ') + ' (' + the_question + ')', dirty.substring(index + 1, dirty.length));
        } else {
            if (value != 'yes' && value != 'no' && value != 'dontknow ')
                bool_container.pushWithDelegate('question_nr_' + clean, clean.replace('_', '') + '. ' + the_question.replace(/\s{2,}/g, ' ') + '',
                    value, 'clear_selection("question_nr_' + clean + '", " ");');

        }
    }

    qvalues[qnum] = value;
    // qnum may be 'X_Y' for option Y of multiple choice question X
    qnum = qnum.split('_')[0];
    for (var t in qtriggers) {
        t = qtriggers[t];
        checks = getChecksAttr(t);
        var res = eval(checks);
        statusChanged(t, res)
    }
}

function initialvalchanged(qnum, value, self) {
    qvalues[qnum] = value;
    // qnum may be 'X_Y' for option Y of multiple choice question X
    qnum = qnum.split('_')[0];
    for (var t in qtriggers) {
        t = qtriggers[t];
        checks = getChecksAttr(t);
        var res = eval(checks);
        statusChanged(t, res)
    }
}

function addtrigger(elemid) {
    var elem = document.getElementById(elemid);
    //console.log(elemid + " : " + elem + " : "+document.getElementById(elemid));
    if (!elem) {
        console.error("addtrigger: Element with id " + elemid + " not found.");
        return;
    }
    qtriggers[qtriggers.length] = elem;
}

function clear_selection(question_name, response) {
    var quest = question_name.replace('question_nr_', 'question_');
    var was_checked = $(":radio[name='" + quest + "']").is(':checked');

    $(":radio[name='" + quest + "']").prop('checked', false);
    if (!(typeof bool_container === 'undefined')) {
        bool_container.splice(question_name, response, '');
    }
    if (was_checked) {
        if (!(typeof questionSetsCounters === 'undefined')) {
            var qId = parseInt(quest.split("_")[1]);

            questionSetsCounters[qId]['filledQuestions'] = questionSetsCounters[qId]['filledQuestions'] - 1;

            var ui = new CounterUI();
            ui.updateCountersClean(qId);
        }
    }
}

/* 
 - disable the submit button once it's been clicked 
 - do it for a total of 5 seconds by which time the page should've been sent
 - oscillate the sending class which does some fancy css transition trickery
*/
function setsaveqs(id, fingerprint_id, q_id, mode) {
    if (!e) var e = window.event;

    $('#' + id).submit(function(e) {
        if (e)
            e.preventDefault();

        var self = $(this);

        if (!(typeof errornavigator === 'undefined')) {
            errornavigator.hideErrorPage();
            $("#loading-message").fadeOut('fast');
            $("#loading-error-message").fadeOut('fast');
            errornavigator.reset();

            var list_invalid = advValidator.validateFormContext(e, self);
            //console.log(list_invalid);


            if (list_invalid.length == 0) {

                if (formHasChanged) {
                    // If its not the first or last
                    var id = this.id.split('_');

                    if (self.length != 0 && id[1] != '0' && id[1] != '99') {

                        // Save this questionset using an ajax post
                        var posting = $.post(self.attr("action"), self.serialize());

                        $("#loading-message").fadeIn('fast');

                        posting.done(function(data) {
                            $("#loading-message").fadeOut('fast');
                            formHasChanged = false;

                            if (data.mandatoryqs && data.mandatoryqs != -1 && data.mandatoryqs != id[1]) {
                                formHasChanged = true;
                                questionsets_handle('qs_' + data.mandatoryqs, fingerprint_id, q_id, mode);

                            }
                        });

                        posting.fail(function(data) {
                            $("#loading-message").fadeOut('fast');

                            $("#loading-error-message").fadeIn('fast');

                        });
                        advValidator.reload();
                    }
                }

                document.body.scrollTop = document.documentElement.scrollTop = 0;

                formHasChanged = false;
                list_invalid = [];

            } else {
                console.log("Jump to errors and show error navigator.");

                for (var i = 0; i < list_invalid.length; i++) {
                    errornavigator.addError('qc_' + list_invalid[i]);
                }
                errornavigator.showErrorPager();

                // jump to first problem
                errornavigator.nextError();

            }

        }

    });
}
QsType = {
    ADD: 0,
    EDIT: 1,
    VIEW: 2,
    SEARCH: 3
}

function findQsPath(mode) {
    var path = ""
    if (mode == QsType.ADD)
        path = "addqs/";
    else if (mode == QsType.EDIT)
        path = "editqs/"
    else if (mode == QsType.VIEW)
        path = "detailedqs/"
    else if (mode == QsType.SEARCH) {
        path = "searchqs/"
    }

    return path;
}

function findPath(mode) {
    var path = ""
    if (mode == QsType.ADD)
        path = "add/";
    else if (mode == QsType.EDIT)
        path = "dbEdit/"
    else if (mode == QsType.VIEW)
        path = "dbDetailed/"
    else if (mode == QsType.SEARCH) {
        path = "advancedSearch/"
    }

    return path;
}

function loadqspart(fingerprint, pk, sortid, mode) {

    var path = findQsPath(mode);

    console.log(path + fingerprint + "/" + pk + "/" + sortid + "/");

    if (sortid != null) {
        console.log($("#qs_" + pk));
        $.get(path + fingerprint + "/" + pk + "/" + sortid + "/", function(data) {
            if (mode == QsType.SEARCH) {
                $("#qs_" + pk).html(data);
            } else {
                $("#qs_" + sortid).html(data);
            }
        });
    } else
        $.get(path + fingerprint + "/" + pk + "/", function(data) {
            $("#qs_" + pk).html(data);
        });

}
var errornavigator;

function initQsEnv(fingerprint_id, q_id, sortid, mode) {
    generateStub();
    $('.reqfield').tooltip({
        container: 'body'
    });
    errornavigator = $('#errornavigator').errornavigator();

    loadqspart(fingerprint_id, q_id, sortid, mode);

    if (mode == QsType.VIEW) {
        advValidator.searchMode(true);
    }

    initialCounterSetup();

    if (!(window.history && history.pushState)) {
        page = History.getState().hash.split('/')[2];

        if (page)
            questionsets_handle(document.getElementById('qs_' + page), fingerprint_id, q_id, mode);
    }

}

function questionsets_handle(id_questionset, fingerprint_id, q_id, mode) {
    if (!e) var e = window.event;

    var id = id_questionset.split('_');

    $('#active_qs').val(id_questionset);
    $('#active_qs_sortid').val(id[1]);

    advValidator.reload();

    // First we get the previous form
    var previous_id = $('.questionset:not(.hide)').first().attr('id').split('_')[1];
    var current_form = $('#qform' + previous_id);


    if (!(typeof errornavigator === 'undefined')) {
        errornavigator.hideErrorPage();
        $("#loading-message").fadeOut('fast');
        $("#loading-error-message").fadeOut('fast');
        errornavigator.reset();


        var list_invalid;
        if (mode == QsType.VIEW || mode == QsType.SEARCH)
            list_invalid = []
        else
            list_invalid = advValidator.validateFormContext(e, current_form);

        if (list_invalid.length == 0) {

            if (formHasChanged && (mode != QsType.VIEW) && mode != QsType.SEARCH) {
                // If its not the first or last
                if (current_form.length != 0 && id[1] != '0' && id[1] != '99') {

                    // Save this questionset using an ajax post
                    var posting = $.post(current_form.attr("action"), current_form.serialize());

                    $("#loading-message").fadeIn('fast');

                    posting.done(function(data) {
                        $("#loading-message").fadeOut('fast');
                        formHasChanged = false;

                        if (data.mandatoryqs && data.mandatoryqs != -1) {

                            formHasChanged = true;
                            questionsets_handle('qs_' + data.mandatoryqs, fingerprint_id, q_id, mode);

                        }
                    });
                    posting.fail(function(data) {
                        $("#loading-message").fadeOut('fast');
                    });
                }
            }
            $('.questionset').each(function(i, obj) {

                    if (obj.id == id_questionset) {

                        $('#' + obj.id).addClass("show");
                        $('#li_' + id_questionset).addClass("active");
                        $('#' + obj.id).removeClass("hide");

                        if ($('#' + obj.id).find('.loadingindicator').length != 0) {
                            if (mode == QsType.SEARCH)
                                loadqspart(fingerprint_id, obj.id.replace("qs_", ""), q_id, mode);
                            else
                                loadqspart(fingerprint_id, q_id, obj.id.replace("qs_", ""), mode);
                            console.log("Loading to dom");
                        } else {
                            console.log("Already on dom");
                        }
                        console.log(mode);
                        console.log(findPath(mode));
                        if (mode == QsType.SEARCH)
                            if(q_id != null){
                              History.pushState(null, null, findPath(mode) + fingerprint_id + "/" + obj.id.replace("qs_", "")+"/"+q_id);
                            } else {
                              History.pushState(null, null, findPath(mode) + fingerprint_id + "/" + obj.id.replace("qs_", ""));
                            }
                            
                        else
                            History.pushState(null, null, findPath(mode) + q_id + "/" + obj.id.replace("qs_", ""));

                        advValidator.reload();
                    } else {

                        $('#li_' + obj.id).removeClass("active");
                        $('#' + obj.id).addClass("hide");
                        $('#' + obj.id).removeClass("show");
                    }

                }

            );
            document.body.scrollTop = document.documentElement.scrollTop = 0;

            list_invalid = [];

        } else {
            console.log("Jump to errors and show error navigator.");

            for (var i = 0; i < list_invalid.length; i++) {
                errornavigator.addError('qc_' + list_invalid[i]);
            }
            errornavigator.showErrorPager();

            // jump to first problem
            errornavigator.nextError();

        }
    }
}