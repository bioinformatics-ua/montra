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

id_questionnaire = 1

qu = get_object_or_404(Questionnaire, id=id_questionnaire)


def get_number_of_h(number):
	return str(number.count('.'))

qsets = qu.questionsets()
for qs in qsets:
	print "iterate questions"
	questions = qs.questions()
	for q in questions:
		print q
		print q.text
		t = q.text
		q.text_en = "h" + get_number_of_h(q.number) + ". " + t


		print q.text
		q.save()
		slugs = Slugs.objects.filter(question=q.pk)
		for s in slugs:
			s.description = q.text
			s.save()

