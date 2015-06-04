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
from django.utils.translation import ugettext as _
from django.utils.simplejson import dumps

import re

@question_proc('choice-yesno','choice-yesnodontknow')
def question_yesno(request, question):
    key = "question_%s" % question.number
    key2 = "question_%s_comment" % question.number
    val = request.POST.get(key, '')
    cmt = request.POST.get(key2, '')
    qtype = question.get_type()
    cd = question.getcheckdict()
    jstriggers = []
    hasValue = False
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
        'template' : 'questionnaire/choice-yesno.html',
    }

@question_proc('open', 'open-validated','email', 'url', 'open-textfield', 'open-button', 'comment')
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
        #print 'MATCH'
        value = value+'-01-01'

    return {
        'required' : question.getcheckdict().get('required', False),
        'value' : value,
        'hasValue': (value!="" and value !="dd/mm/yyyy"),
        'template' : 'questionnaire/datepicker.html',
    }

@answer_proc('open', 'open-validated', 'email', 'url' 'open-textfield', 'choice-yesno', 'choice-yesnodontknow',  'open-button')
def process_simple(question, ansdict):
    checkdict = question.getcheckdict()
    required = question.getcheckdict().get('required', 0)
    ans = ansdict['ANSWER'] or ''
    qtype = question.get_type()
    if qtype.startswith('choice-yesno'):
        if ans not in ('yes','no','dontknow') and required:
            raise AnswerException(_(u'You must select an option'))
    else:
        if not ans.strip() and checkdict.get('required', False):
           raise AnswerException(_(u'Field cannot be blank'))
    if ansdict.has_key('comment') and len(ansdict['comment']) > 0:
        return dumps([ans, [ansdict['comment']]])
    if ans:
        return dumps([ans])
    return dumps([])
add_type('open', 'Open Answer, single line [input]')
add_type('open-validated', 'Open Validated Answer, single line validated with a regex[input]')
add_type('open-button', 'Open Answer, single line [input] with a button to validate')
add_type('open-textfield', 'Open Answer, multi-line [textarea]')
add_type('choice-yesno', 'Yes/No Choice [radio]')
add_type('choice-yesnodontknow', 'Yes/No/Don\'t know Choice [radio]')
add_type('datepicker', 'Date choice')
add_type('email', 'Email Address [input]')
add_type('url', 'Url Address [input]')



@answer_proc('comment')
def process_comment(question, answer):
    pass
add_type('comment', 'Comment Only')

@show_summary('choice-yesnodontknow')
def show_summ(value):
    valueclean = value.lower().strip()

    if 'dontknow' in valueclean:
        return valueclean.replace('dontknow', "Don't Know")
    elif 'yes' in valueclean:
        return valueclean.replace('yes', 'Yes')
    elif 'no' in valueclean:
        return valueclean.replace('no', 'No')

    return value
