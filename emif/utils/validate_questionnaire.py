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
from django.http import HttpResponse, HttpResponseRedirect

from questionnaire.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

from searchengine.models import *

rem = 1



qu = get_object_or_404(Questionnaire, id=rem)

qsets = qu.questionsets()

for qs in qsets:

    expected = qs.questions()
    for q in expected:
        slugs = Slugs.objects.filter(description__exact=q.text)
        if len(slugs)!=1:
            print "Error (multiple slugs to the description): " +  q.number
            for s in slugs:
                try:
                    print s.slug1 + "| " + s.description + "| " + str(s.question.pk)
                except:
                    print s.slug1 + "| " + str(s.question.pk)
            continue
        s = slugs[0]
        if (s.slug1 != q.slug):
            print "Error (slug1!=slug): " + q.number
            print s.slug1 + "| " + s.description + "| " + str(s.question.pk)
            continue
        if (s.question.pk!=q.pk):
            print "Error (q.pk!=pk): " + q.number
            continue


