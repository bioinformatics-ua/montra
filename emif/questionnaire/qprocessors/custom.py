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
#
# Custom type exists for backwards compatibility. All custom types should now
# exist in the drop down list of the management interface.
#

from questionnaire import *
from questionnaire import Processors, QuestionProcessors
from django.utils.translation import ugettext as _

@question_proc('custom')
def question_custom(request, question):
    cd = question.getcheckdict()
    _type = cd['type']
    d = {}
    if _type in QuestionProcessors:
        d = QuestionProcessors[_type](request, question)
    if 'template' not in d:
        d['template'] = 'questionnaire/%s.html' % _type
    return d


@answer_proc('custom')
def process_custom(question, answer):
    cd = question.getcheckdict()
    _type = cd['type']
    if _type in Processors:
        return Processors[_type](question, answer)
    raise AnswerException(_(u"Processor not defined for this question"))

add_type('custom', 'Custom')





