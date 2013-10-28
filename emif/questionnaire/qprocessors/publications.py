
from questionnaire import *
from questionnaire import Processors, QuestionProcessors
from django.utils.translation import ugettext as _

@question_proc('publication')
def question_pub(request, question):
    cd = question.getcheckdict()
    print cd
    
    d = {}
    
    if 'template' not in d:
        d['template'] = 'questionnaire/publications.html'
    return d


@answer_proc('publication')
def process_pub(question, answer):
    pass

add_type('publication', 'Publication')





