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

desiredQN = "10.01.11"

def getQuestionObj(id):
	arr = Question.objects.filter(questionset=id, number=desiredQN)
	for x in arr:
		return x
	return Question()

def create_question(qset):
	#Create Question;
	q = getQuestionObj(qset.id)
	q.questionset = qset
	q.number = desiredQN
	q.text_en = "h2. Specify any other scales"
	q.type = "open-textfield"
	q.help_text = "Specify each scale in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Subgroup, Items score available."
	q.slug = "neuropsychiatric_scales_other"
	q.checks = "dependent=\"10.01,yes\""
	return q

def updateSlug(qs):
	arr = Slugs.objects.filter(question=qs)
	if len(arr) == 0:
		x = Slugs()
		x.question = qs
		x.slug1 = qs.slug
		x.description = qs.text
		print x
		x.save()
		return
	for x in arr:
		x.slug1 = qs.slug
		x.description = qs.text
		print x
		x.save()
	return


qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychiatric_Scales")
print qsets
print len(qsets)
for qs in qsets:
 	print "iterate questions"
 	print qs
 	question = create_question(qs)
	question.save()
	print "Saved Question"
	updateSlug(question)

print "QUITTING"
