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
from django.utils.translation import ugettext as _, ugettext_lazy

perioddict = {
    "second" : ugettext_lazy("second(s)"),
    "minute" : ugettext_lazy("minute(s)"),
    "hour" : ugettext_lazy("hour(s)"),
    "day" : ugettext_lazy("day(s)"),
    "week" : ugettext_lazy("week(s)"),
    "month" : ugettext_lazy("month(s)"),
    "year" : ugettext_lazy("year(s)"),
}

@question_proc('timeperiod')
def question_timeperiod(request, question):
    cd = question.getcheckdict()
    if "units" in cd:
        units = cd["units"].split(',')
    else:
        units = ["day","week","month","year"]
    timeperiods = []
    if not units:
        units = ["day","week","month","year"]

    key1 = "question_%s" % question.number
    key2 = "question_%s_unit" % question.number
    value = request.POST.get(key1, '')
    unitselected = request.POST.get(key2, units[0])

    for x in units:
        if x in perioddict:
            timeperiods.append( (x, unicode(perioddict[x]), unitselected==x) )
    return {
        "required" : "required" in cd,
        "timeperiods" : timeperiods,
        "value" : value,
        'hasValue': value!="",
    }

@answer_proc('timeperiod')
def process_timeperiod(question, answer):
    if not answer['ANSWER'] or not answer.has_key('unit'):
        raise AnswerException(_(u"Invalid time period"))
    period = answer['ANSWER'].strip()
    if period:
        try:
            period = str(int(period))
        except ValueError:
            raise AnswerException(_(u"Time period must be a whole number"))
    unit = answer['unit']
    checkdict = question.getcheckdict()
    if checkdict and 'units' in checkdict:
        units = checkdict['units'].split(',')
    else:
        units = ('day', 'hour', 'week', 'month', 'year')
    if not period and "required" in checkdict:
        raise AnswerException(_(u'Field cannot be blank'))
    if unit not in units:
        raise AnswerException(_(u"Invalid time period"))
    return "%s; %s" % (period, unit)

add_type('timeperiod', 'Time Period [input, select]')

