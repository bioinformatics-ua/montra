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
from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys
import re

from django.conf import settings


p = re.compile("(\\d{1,2})(\.\\d{2})*$", re.L)

#qsets = QuestionSet.objects.all()
slugs = []
questionaires = Questionnaire.objects.filter(disable=False)
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


print slugs

import pysolr

solr = pysolr.Solr('http://' +settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
start=0
rows=100
fl=''

solr.add(slugs)

#solr.delete(q="id:questionaire_*")



#if len(wrongs)> 0:
#	for s in changes:
#		questions = Question.objects.filter(id=s["id"])
#		for q in questions:
#			q.number = s["number"]
#			q.save()
#			print "Saved " +str(q)

# for qs in qsets:
#  	print "iterate questions"
#  	print qs
#  	question = create_question(qs)
# 	question.save()
# 	print "Saved Question"
# 	updateSlug(question)

print "QUITTING"
