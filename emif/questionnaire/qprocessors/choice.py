from questionnaire import *
from django.utils.translation import ugettext as _, ungettext
from django.utils.simplejson import dumps

import re


@question_proc('choice', 'choice-freeform')
def question_choice(request, question):
    choices = []
    jstriggers = []

    cd = question.getcheckdict()
    key = "question_%s" % question.number
    key2 = "question_%s_comment" % question.number
    val = None
    if key in request.POST:
        val = request.POST[key]

    else:
        if 'default' in cd:
            val = cd['default']

    if val != None and "#" in val:
        val = val.split("#")[0]
    for choice in question.choices():
        #print "choice.value: " + str(choice.value )
        #print "val" + str(val)
        choices.append( ( choice.value == val, choice, ) )

    if question.type == 'choice-freeform':
        jstriggers.append('%s_comment' % question.number)

    return {
        'choices'   : choices,
        'sel_entry' : val == '_entry_',
        'qvalue'    : val or '',
        'required'  : True,
        'comment'   : request.POST.get(key2, ""),
        'jstriggers': jstriggers,
    }

@answer_proc('choice', 'choice-freeform')
def process_choice(question, answer):
    required = question.getcheckdict().get('required', 0)

    opt = answer['ANSWER'] or ''
    if not opt and required:
        raise AnswerException(_(u'You must select an option'))
    if opt == '_entry_' and question.type == 'choice-freeform':
        opt = answer.get('comment','')
        if not opt:
            raise AnswerException(_(u'Field cannot be blank'))
        return dumps([[opt]])
    else:
        valid = [c.value for c in question.choices()]
        if opt not in valid and required:
            raise AnswerException(_(u'Invalid option!'))
    return dumps([opt])
add_type('choice', 'Choice [radio]')
add_type('choice-freeform', 'Choice with a freeform option [radio]')


@question_proc('choice-multiple', 'choice-multiple-freeform')
def question_multiple(request, question):
    key = "question_%s" % question.number
    #print key
    choices = []
    counter = 0
    cd = question.getcheckdict()
    val = None
    try:
        val = request.POST.get(key, None)
    except:
        pass
    defaults = cd.get('default','').split(',')
    for choice in question.choices():
        counter += 1
        key = "question_%s_multiple_%d" % (question.number, choice.sortid)
        
        if key in request.POST or (val!=None and (choice.value in val)) or \
          (request.method == 'GET' and choice.value in defaults):
            choices.append( (choice, key, ' checked',) )
        else:
            choices.append( (choice, key, '',) )
    extracount = int(cd.get('extracount', 0))
    if not extracount and question.type == 'choice-multiple-freeform':
        extracount = 1
    extras = []
    if question.number=="16": 
        print "Request POST "  + str(request.POST)
    for x in range(1, extracount+1):

        key = "question_%s_more%d" % (question.number, x)
        key_aux = "question_%s" % (question.number)

        if key_aux in request.POST :
            
            extras_value = request.POST[key_aux].split("||")
            if (len(extras_value)>1):
                extras.append( (key, extras_value[1]) )
            else:
                extras.append( (key, '') )
        elif key in request.POST:
            extras.append( (key, request.POST[key]) )
        else:
            extras.append( (key, '',) )

    return {
        "choices": choices,
        "extras": extras,
        "template"  : "questionnaire/choice-multiple-freeform.html",
        "required" : cd.get("required", False) and cd.get("required") != "0",

    }

@answer_proc('choice-multiple', 'choice-multiple-freeform')
def process_multiple(question, answer):
    multiple = []
    multiple_freeform = []

    requiredcount = 0
    required = question.getcheckdict().get('required', 0)
    if required:
        try:
            requiredcount = int(required)
        except ValueError:
            requiredcount = 1
    if requiredcount and requiredcount > question.choices().count():
        requiredcount = question.choices().count()


    import pdb
    #pdb.set_trace()
    for k, v in answer.items():
        #print "K: " + str(k)
        #print "V "
        if k.startswith('multiple'):
            multiple.append(v)
        if k.startswith('more') and len(v.strip()) > 0:
            multiple_freeform.append(v)

    if len(multiple) + len(multiple_freeform) < requiredcount:
        raise AnswerException(ungettext(u"You must select at least %d option",
                                        u"You must select at least %d options",
                                        requiredcount) % requiredcount)
    multiple.sort()
    if multiple_freeform:
        multiple.append(multiple_freeform)
    #print "Multiple" + str(multiple)
    return dumps(multiple)

def get_aux_text(full_value, choice_value):
    if (full_value==None):
        return ''
    _aux = full_value.split("#")
    #print _aux
    for v in _aux:
        if choice_value in v:
            values = re.findall(r'\{(.*?)\}', v)
            print choice_value
            print values
            if (len(values)>0):
                return values[0]
    return ''

@question_proc('choice-multiple', 'choice-multiple-freeform-options')
def question_multiple_options(request, question):
    key = "question_%s" % question.number
    print key
    choices = []
    counter = 0
    cd = question.getcheckdict()
    val = None
    try:
        val = request.POST.get(key, None)
    except:
        pass
    defaults = cd.get('default','').split(',')

    for choice in question.choices():
        counter += 1

        key = "question_%s_multiple_%d" % (question.number, choice.sortid)
        key_value = "question_%s_%d_opt" % (question.number, choice.sortid)
        if val!=None:
            print "Val: " +val
        if choice!=None:
            print "choice.value: " + choice.value
        _aux = ""
        try:
            _aux = request.POST[key_value]
        except:
            pass


        print "get_aux_text(val,choice.value )" + get_aux_text(val,choice.value )

        if key in request.POST or (val!=None and (choice.value in val)) or \
          (request.method == 'GET' and choice.value in defaults):
            choices.append( (choice, key, ' checked',get_aux_text(val,choice.value )) )
        else:
            choices.append( (choice, key, '',get_aux_text(val,choice.value )) )
    extracount = int(cd.get('extracount', 0))
    if not extracount and question.type == 'choice-multiple-freeform-options':
        extracount = 1
    extras = []
    
    for x in range(1, extracount+1):

        key = "question_%s_more%d" % (question.number, x)
        key_aux = "question_%s" % (question.number)

        if key_aux in request.POST :
            
            extras_value = request.POST[key_aux].split("||")
            if (len(extras_value)>1):
                extras.append( (key, extras_value[1]) )
            else:
                extras.append( (key, '') )
        elif key in request.POST:
            extras.append( (key, request.POST[key]) )
        else:
            extras.append( (key, '',) )

    return {
        "choices": choices,
        "extras": extras,
        "template"  : "questionnaire/choice-multiple-freeform-options.html",
        "required" : cd.get("required", False) and cd.get("required") != "0",

    }

@answer_proc('choice-multiple', 'choice-multiple-freeform-options')
def process_multiple_options(question, answer):
    multiple = []
    multiple_freeform = []

    requiredcount = 0
    required = question.getcheckdict().get('required', 0)
    if required:
        try:
            requiredcount = int(required)
        except ValueError:
            requiredcount = 1
    if requiredcount and requiredcount > question.choices().count():
        requiredcount = question.choices().count()

    for k, v in answer.items():
        print "K: " + str(k)
        print "V "
        if k.startswith('multiple'):
            multiple.append(v)
        if k.startswith('more') and len(v.strip()) > 0:
            multiple_freeform.append(v)

    if len(multiple) + len(multiple_freeform) < requiredcount:
        raise AnswerException(ungettext(u"You must select at least %d option",
                                        u"You must select at least %d options",
                                        requiredcount) % requiredcount)
    multiple.sort()
    if multiple_freeform:
        multiple.append(multiple_freeform)
    #print "Multiple" + str(multiple)
    return dumps(multiple)

add_type('choice-multiple', 'Multiple-Choice, Multiple-Answers [checkbox]')
add_type('choice-multiple-freeform', 'Multiple-Choice, Multiple-Answers, plus freeform [checkbox, input]')
add_type('choice-multiple-freeform-options', 'Multiple-Choice with Options, Multiple-Answers, plus freeform [checkbox, input]')


