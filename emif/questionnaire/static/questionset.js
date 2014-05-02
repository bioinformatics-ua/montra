var qvalues = new Array(); // used as dictionary
var qtriggers = new Array();

function dep_check(expr) {
    var exprs = expr.split(",",2);
    var qnum = exprs[0];
    var value = exprs[1];
    var qvalue = qvalues[qnum];
    if(value.substring(0,1) == "!") {
      var multiple_option = qvalues[qnum+'_'+value.substring(1)];
      if(multiple_option != undefined)
        return !multiple_option;
      value = value.substring(1);
      return qvalue != value;
    }
    if(value.substring(0,1) == "<") {
      qvalue = parseInt(qvalue);
      if(value.substring(1,2) == "=") {
        value = parseInt(value.substring(2));
        return qvalue <= value;
      }
      value = parseInt(value.substring(1));
      return qvalue < value;
    }
    if(value.substring(0,1) == ">") {
      qvalue = parseInt(qvalue);
      if(value.substring(1,2) == "=") {
        value = parseInt(value.substring(2));
        return qvalue >= value;
      }
      value = parseInt(value.substring(1));
      return qvalue > value;
    }
    var multiple_option = qvalues[qnum+'_'+value];
    if(multiple_option != undefined) {
      return multiple_option;
    }
    if(qvalues[qnum] == value) {
      return true;
    }
    return false;
}

function getChecksAttr(obj) {
    /* while most browser consider getAttributes a function, IE 9< considers it a object
     * So its actually better to use jquery for this
    return obj.getAttribute('checks'); */
    var $obj = $(obj);
    return $obj.attr('checks');
}

function statusChanged(obj, res) {
    if(obj.tagName == 'DIV') {
        obj.style.display = !res ? 'none' : 'block';
        return;
    }
    //obj.style.backgroundColor = !res ? "#eee" : "#fff";
    obj.disabled = !res;
}
function clearcheck(id){
    console.warn('clearcheck ID: '+id);
    $(':input[name="'+id+'"]').removeAttr('checked');
    //$(':input[name="'+id+'"]').click();
}
function valchanged(qnum, value, self) {
    if (!(typeof bool_container === 'undefined')) {
        var $self = $(self);
        
        var just_number = qnum.split('_')[1];
        var clean = qnum.replace('question_','').replace(/(\\)/g, '');
        var dirty = qnum.replace('question_','').replace('_',':');
        var index = dirty.indexOf(':');

        // We have to get the question
        var the_question = $('#question_'+clean.split('_')[0].replace(/(\.)/g,'')).text().trim(); 
        if(value==true){

            //console.log(qnum);
            //console.log(clean.replace('_','. ')+' ('+the_question+')');
            //console.log(value);
            
            //var optional = $('#question_'+clean.split('_')[0].replace(/(\.)/g,'')).closest('input[type="text"]');
            //console.log(optional.attr('id'));
            
            //var optional = $('#question_'+just_number.replace(/(\.)/g,'\\.')+"_1_opt").val();
            bool_container.pushWithDelegate('question_nr_'+dirty.substring(0,index)+"_____"+clean+"_____",
                                clean.replace('_','. ')+' ('+the_question+')'
                               , dirty.substring(index+1,dirty.length), 'clearcheck("'+$self.attr('id')+'");');
        } else if(value==false){
            var optional = $('#question_'+just_number.replace(/(\.)/g,'')+"_opt").val();
            bool_container.splice('question_nr_'+dirty.substring(0,index)+"_____"+clean+"_____",
                                clean.replace('_','. ')+' ('+the_question+')'
                               , dirty.substring(index+1,dirty.length));
        } else {       
            if( value != 'yes' && value != 'no' && value != 'dontknow ')
            bool_container.pushWithDelegate('question_nr_'+clean, clean.replace('_','')+'. '+the_question.replace(/\s{2,}/g, ' ')+'', 
                value, 'clear_selection("question_nr_'+clean+'", " ");');   
                        
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
function initialvalchanged(qnum, value, self){
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
    if(!elem) {
      console.error("addtrigger: Element with id "+elemid+" not found.");
      return;
    }
    qtriggers[qtriggers.length] = elem;
}

function clear_selection(question_name, response){
    var quest = question_name.replace('question_nr_','question_');
    var was_checked = $(":radio[name='" + quest + "']").is(':checked');

    $(":radio[name='" + quest + "']").prop('checked', false);
    if (!(typeof bool_container === 'undefined')) {
            bool_container.splice(question_name, response, '');
    }        
    if(was_checked){
        if (!(typeof questionSetsCounters === 'undefined')) {
                var qId = parseInt(quest.split("_")[1]);

                questionSetsCounters[qId]['filledQuestions'] = questionSetsCounters[qId]['filledQuestions']-1;

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
function setsaveqs(id){
        $('#'+id).submit(function(e) {
            e.preventDefault();

            var self = $(this);

      if (!(typeof errornavigator === 'undefined')) {
      errornavigator.hideErrorPage();
      errornavigator.reset();

      var list_invalid = advValidator.validateFormContext(event, self);
      //console.log(list_invalid);


      if(list_invalid.length == 0){

        if(formHasChanged){
          // If its not the first or last
          var id = this.id.split('_');

          if(self.length != 0 && id[1] != '0' && id[1] != '99'){

            // Save this questionset using an ajax post
            var posting = $.post(self.attr("action"), self.serialize());

            $("#loading-message").fadeIn('fast');

            posting.done(function(data) {
              $("#loading-message").fadeOut('fast');
            });
          }
        }

        document.body.scrollTop = document.documentElement.scrollTop = 0; 

        formHasChanged = false;   
        list_invalid = []; 

      } else {
        console.log("Jump to errors and show error navigator.");

          for(var i = 0;i<list_invalid.length;i++){
            errornavigator.addError('qc_'+list_invalid[i]);
          }
          errornavigator.showErrorPager();

          // jump to first problem
          errornavigator.nextError();

        }

      }

        });
    }

