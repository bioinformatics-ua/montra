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

    if value== "":
        return ""

    if not value.startswith('['):
        value = '['+value+']'

    try:
        pubs = json.loads(value)

        if type(pubs) is not list:
            pubs = [pubs]

        return render_to_string('questionnaire/publications_summary.html', {'pubs': pubs})
    except:
        return "Error Loading Publications"

add_type('publication', 'Publication')





