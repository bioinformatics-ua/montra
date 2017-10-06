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
import re

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

    key = "question_%s" % question.number

    vals = request.POST.get(key, '').split('#')

    value = vals[0]
    unitselected = None
    cleanunit = None
    try:
        unitselected = vals[1]
        cleanunit = re.sub('<[^<]+?>', '', unitselected)
    except IndexError:
        pass
    for x in units:
        if x in perioddict:
            carry=None
            if cleanunit==x:
                carry = unicode(perioddict[x])
                if 'highlight' in unitselected:
                    carry = '<span class="highlight">'+carry+'</span>'
            timeperiods.append( (x, unicode(perioddict[x]), carry) )
    return {
        "required" : "required" in cd,
        "timeperiods" : timeperiods,
        "value" : value,
        'hasValue': value!="",
    }

@answer_proc('timeperiod')
def process_timeperiod(question, answer):
    parts = answer['ANSWER'].split('#')

    if not answer['ANSWER'] or len(parts) < 2:
        raise AnswerException(_(u"Invalid time period"))
    period = parts[0].strip()
    if period:
        try:
            period = str(int(period))
        except ValueError:
            raise AnswerException(_(u"Time period must be a whole number"))
    unit = parts[1]
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

@show_summary('timeperiod')
def show_summ_timeperiod(value):
    tmp=""
    parts = value.split('#')

    if len(parts) == 2:
        tmp+= " %s"%parts[0]
        carry = ""
        try:
            unit = parts[1]
            cleanunit = re.sub('<[^<]+?>', '', unit)
            carry = unicode(perioddict[cleanunit])
            if 'highlight' in unit:
                carry = '<span class="highlight">'+carry+'</span>'
        except:
            pass

        tmp += carry

    return tmp
