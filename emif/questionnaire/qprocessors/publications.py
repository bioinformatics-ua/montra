
from questionnaire import *
from questionnaire import Processors, QuestionProcessors, Fingerprint_Summary
from django.utils.translation import ugettext as _

from questionnaire import *
from django.utils.translation import ugettext as _
from django.utils.simplejson import dumps

from django.template.loader import render_to_string

import json 

@question_proc('publication')
def question_pub(request, question):
    cd = question.getcheckdict()
    
    key = "question_%s" % question.number
    value = question.getcheckdict().get('default','')
    #print "PUB"
    #print key
    #print request.POST
    if key in request.POST:
        value = request.POST[key]
        #print "REQUEST" + value
    return {
        'required' : question.getcheckdict().get('required', False),
        'value' : value,
        "hasValue": value!="",
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

@show_summary('publication')
def show_summ(value):

    pubs = json.loads("["+value+"]")

    if type(pubs) is not list:
        pubs = [pubs]

    #print "###########"
    #print pubs[{\"pmid\":\"22874241\",
    # \"title\":\"Dicoogle Mobile: a medical imaging platform for Android.\"
    # ,\"journal\":\"Studies in health technology and informatics\"
    # ,\"year\":\"2012\",
    # \"pages\":\"180\",\"volume\":\"502-6\",
    # \"authors\":\"Viana-Ferreira C,Ferreira D,Valente F,Monteiro E,Costa C,Oliveira JL\",\"link\":\"\"}]",
        
    return render_to_string('questionnaire/publications_summary.html', {'pubs': pubs})

    ret = "<ul>"
    for p in pubs:
        title = p["title"]
        authors = p["authors"]
        year = p["year"]
        journal = p["journal"]
        pages = p["pages"]
        volume = p["volume"]        
        ret += "<li>" + authors + " - " + title + ". " + journal + ". " + year +" :" +pages +":"+ volume +"</li>"

    ret += "</ul>"
    #print "##########"
    #print ret
    return ret

add_type('publication', 'Publication')





