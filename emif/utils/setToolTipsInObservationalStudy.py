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

quest_id = 49
#qsets = QuestionSet.objects.all()
slugs = []
questionaires = Questionnaire.objects.filter(id=49)
for quest in questionaires:
	id = quest.id
	obj = {"id":"questionaire_"+str(id)}
	print quest.id
	print quest.name

	qsets = QuestionSet.objects.filter(questionnaire=quest)
	for qs in qsets:
		questions = qs.questions();
		#print "QS: "+qs.help_text
		for q in questions:
			#print "-----> Q:"+q.help_text
			if not q.tooltip and len(q.help_text)>0:
				q.tooltip = True
				print "----> Set Tooltip: "+ str(q)
				q.save()
			if q.tooltip:
				print q

print "QUITTING"
