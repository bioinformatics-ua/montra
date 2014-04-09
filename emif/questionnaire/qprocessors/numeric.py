from questionnaire import *
from questionnaire import Processors, QuestionProcessors
from django.utils.translation import ugettext as _

from questionnaire import *
from django.utils.translation import ugettext as _
from django.utils.simplejson import dumps
import re

regex = re.compile("\\d{1,3}(\\.\\d{3})*$")

@question_proc('numeric')
def question_(request, question):
    cd = question.getcheckdict()
    
    key = "question_%s" % question.number
    value = question.getcheckdict().get('default','')

    if key in request.POST:
        value = request.POST[key]
        #print "REQUEST!!!!" + value
    return {
        'required' : question.getcheckdict().get('required', False),
        'value' : value,
        "hasValue": value!= "",
        'template' : 'questionnaire/numeric.html',
    }


@answer_proc('numeric')
def process_(question, ansdict):
    checkdict = question.getcheckdict()
    required = question.getcheckdict().get('required', 0)
    ans = ansdict['ANSWER'] or ''
    qtype = question.get_type()

    boo = regex.match(ans) == None
    
    if len(ans)!=0 and boo:
        raise AnswerException(_(u'Must be a mumeric field. ex: 1.000.000.000 = 1 Million'))

    if ansdict.has_key('comment') and len(ansdict['comment']) > 0:
        return dumps([ans, [ansdict['comment']]])
    if ans:
        return dumps([ans])
    return dumps([])

add_type('numeric', 'Numeric')
