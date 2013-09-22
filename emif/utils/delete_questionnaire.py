# -*- coding: utf-8 -*-

# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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


from questionnaire.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

# Uncomment this and add your list of ids to remove (of Questionnaire model)
to_delete = [1]

for rem in to_delete:
	qu = get_object_or_404(Questionnaire, id=rem)



	qsets = qu.questionsets()

	for qs in qsets:
		print "iterate questions"
		expected = qs.questions()
		
		for q in expected:
			print "iterate choices"
			print q.choices
			try:
				for c in q.choices:
					c.delete()
			except:
				pass
			q.delete()
		qs.delete()

	qu.delete()
