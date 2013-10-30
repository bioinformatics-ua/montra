
from questionnaire import *
from questionnaire import Processors, QuestionProcessors
from django.utils.translation import ugettext as _

from questionnaire import *
from django.utils.translation import ugettext as _
from django.utils.simplejson import dumps

@question_proc('publication')
def question_pub(request, question):
    cd = question.getcheckdict()
    print cd
    key = "question_%s" % question.number
    value = question.getcheckdict().get('default','')
    if key in request.POST:
        value = request.POST[key]
    return {
        'required' : question.getcheckdict().get('required', False),
        'value' : value,
        'template' : 'questionnaire/publications.html',
    }


@answer_proc('publication')
def process_pub(question, ansdict):
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

add_type('publication', 'Publication')





