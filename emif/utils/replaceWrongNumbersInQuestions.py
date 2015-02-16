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

p = re.compile("(\\d{1,2})(\.\\d{2})*$", re.L)

changes = [{'id':5337, 'number':"1.10"},
 			{'id':5520, 'number':"1.17.01"},
 			{'id':5361, 'number':"3.10"},
 			{'id':5438, 'number':"8.10"}]
#qsets = QuestionSet.objects.all()
questionaires = Questionnaire.objects.filter(disable=False)
wrongs = []
for quest in questionaires:
	qsets = QuestionSet.objects.filter(questionnaire=quest)
	# print qsets
	# print len(qsets)
	for qs in qsets:
		#print qs
		questions = qs.questions()
		for q in questions:
			#print q.number
			if not p.match(q.number):
				wrongs.append("Wrong Question Numbe r: "+ str(q.number) + "Question ID: "+str(q.id))

print wrongs

if len(wrongs)> 0:
	for s in changes:
		questions = Question.objects.filter(id=s["id"])
		for q in questions:
			q.number = s["number"]
			q.save()
			print "Saved " +str(q)

# for qs in qsets:
#  	print "iterate questions"
#  	print qs
#  	question = create_question(qs)
# 	question.save()
# 	print "Saved Question"
# 	updateSlug(question)

print "QUITTING"
