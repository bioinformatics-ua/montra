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
from django.shortcuts import render_to_response, get_object_or_404
import sys

id_questionnaire = 1

id_question = 889

def increment_value(number):
	print number
	value = -1
	result = ""
	try:
		value = int(number)
		value+=1
		result = str(value)
		return result
	except:
		pass

	if (value==-1):
		value = number.split(".")

	v1 = str(int(value[0])+1)
	v2 = str(int(value[1]))

	return str(v1) + "." + str(v2)

print increment_value("3.2")
print increment_value("4")
print increment_value("5")
print increment_value("5.1")
print increment_value("5.2")

qu = get_object_or_404(Questionnaire, id=id_questionnaire)

qsets = qu.questionsets()

start = False
for qs in qsets:
	print "iterate questions"
	expected = Question.objects.filter(questionset=qs.id).order_by('number')

	for q in expected:
		if start:
			q.number = increment_value(q.number)
			print "old:"+q.number
			print "new:"+increment_value(q.number)
			q.save()
		if (q.id==id_question):
			start = True


