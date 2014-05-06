from questionnaire import *
from django.utils.translation import ugettext as _
from django.utils.simplejson import dumps

import re

@question_proc('choice-yesno','choice-yesnocomment','choice-yesnodontknow')
def question_yesno(request, question):
    key = "question_%s" % question.number
    key2 = "question_%s_comment" % question.number
    val = request.POST.get(key, '')
    cmt = request.POST.get(key2, '')
    qtype = question.get_type()
    cd = question.getcheckdict()
    jstriggers = []
    hasValue = False
    if qtype == 'choice-yesnocomment':
        hascomment = True
    else:
        hascomment = False
    if qtype == 'choice-yesnodontknow' or 'dontknow' in cd:
        hasdontknow = True
    else:
        hasdontknow = False

    if not val:
        if cd.get('default', None):
            val = cd['default']

    checks = ''
    if hascomment:
        if cd.get('required-yes'):
            jstriggers = ['question_%s_comment' % question.number]
            checks = ' checks="dep_check(\'question_%s,yes\')"' % question.number
        elif cd.get('required-no'):
            checks = ' checks="dep_check(\'question_%s,no\')"' % question.number
        elif cd.get('required-dontknow'):
            checks = ' checks="dep_check(\'question_%s,dontknow\')"' % question.number

    return {
        'required' : True,
        'checks' : checks,
        'value' : val,
        'hasValue': val!="",
        'qvalue' : '',
        'hascomment' : hascomment,
        'hasdontknow' : hasdontknow,
        'comment' : cmt,
        'jstriggers' : jstriggers,
        'template' : 'questionnaire/choice-yesnocomment.html',
    }

@question_proc('open', 'email', 'url', 'open-textfield', 'open-button', 'open-upload-image')
def question_open(request, question):
    key = "question_%s" % question.number
    value = question.getcheckdict().get('default','')
    if key in request.POST:
        value = request.POST[key]
    return {
        'required' : question.getcheckdict().get('required', False),
        'hasValue': value!="",
        'value' : value,
    }

@question_proc('datepicker')
def question_datepicker(request, question):
    key = "question_%s" % question.number
    value = question.getcheckdict().get('default','')
    if key in request.POST:
        value = request.POST[key]

    a = re.compile("([0-9]{4})$")
    if a.match(value) != None:
        print 'MATCH'
        value = value+'-01-01'

    print "VALOR:["+value+"]"

    return {
        'required' : question.getcheckdict().get('required', False),
        'value' : value,
        'hasValue': (value!="" and value !="dd/mm/yyyy"),
        'template' : 'questionnaire/datepicker.html',
    }

@answer_proc('open', 'email', 'url' 'open-textfield', 'choice-yesno', 'choice-yesnocomment', 'choice-yesnodontknow',  'open-button', 'open-upload-image')
def process_simple(question, ansdict):
    checkdict = question.getcheckdict()
    required = question.getcheckdict().get('required', 0)
    ans = ansdict['ANSWER'] or ''
    qtype = question.get_type()
    if qtype.startswith('choice-yesno'):
        if ans not in ('yes','no','dontknow') and required:
            raise AnswerException(_(u'You must select an option'))
        if qtype == 'choice-yesnocomment' \
        and len(ansdict.get('comment','').strip()) == 0:
            if checkdict.get('required', False):
                raise AnswerException(_(u'Field cannot be blank'))
            if checkdict.get('required-yes', False) and ans == 'yes':
                raise AnswerException(_(u'Field cannot be blank'))
            if checkdict.get('required-no', False) and ans == 'no':
                raise AnswerException(_(u'Field cannot be blank'))
    else:
        if not ans.strip() and checkdict.get('required', False):
           raise AnswerException(_(u'Field cannot be blank'))
    if ansdict.has_key('comment') and len(ansdict['comment']) > 0:
        return dumps([ans, [ansdict['comment']]])
    if ans:
        return dumps([ans])
    return dumps([])
add_type('open', 'Open Answer, single line [input]')
add_type('open-button', 'Open Answer, single line [input] with a button to validate')
add_type('open-upload-image', 'Upload Image')
add_type('open-textfield', 'Open Answer, multi-line [textarea]')
add_type('choice-yesno', 'Yes/No Choice [radio]')
add_type('choice-yesnocomment', 'Yes/No Choice with optional comment [radio, input]')
add_type('choice-yesnodontknow', 'Yes/No/Don\'t know Choice [radio]')
add_type('datepicker', 'Date choice')
add_type('email', 'Email Address [input]')
add_type('url', 'Url Address [input]')



@answer_proc('comment')
def process_comment(question, answer):
    pass
add_type('comment', 'Comment Only')



