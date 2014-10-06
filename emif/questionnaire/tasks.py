# -*- coding: utf-8 -*-

# Copyright (C) 2014 Ricardo Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo Ribeiro <ribeiro.r@ua.pt>
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


from __future__ import absolute_import

from celery import shared_task
import time

from searchengine.search_indexes import CoreEngine

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys
import re

from django.conf import settings
import pysolr


@periodic_task(run_every=crontab(minute=0, hour=3))
def reindexQuestionnaires():
    p = re.compile("(\\d{1,2})(\.\\d{2})*$", re.L)

    #qsets = QuestionSet.objects.all()
    slugs = []
    questionaires = Questionnaire.objects.filter(disable=False)

    solr = pysolr.Solr('http://' +settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
    start=0
    rows=100
    fl=''

    for quest in questionaires:
        id = quest.id
        obj = {"id":"questionaire_"+str(id)}
        qsets = QuestionSet.objects.filter(questionnaire=quest)
        for qs in qsets:
            #print qs
            questions = qs.questions()
            for q in questions:
                x = q.slug_fk
                key = str(x.slug1) + "_qs"
                obj[key] = q.text
        slugs.append(obj)


    for quest in questionaires:
        solr.delete(id='questionaire_'+str(id))

    solr.add(slugs)

    print "QUITTING"
