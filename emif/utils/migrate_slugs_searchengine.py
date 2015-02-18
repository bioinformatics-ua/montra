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

from questionnaire.models import Question
from searchengine.models import Slugs
import sys

print '\nbegin copying slugs to searchengine.Slugs ...\n'

for question in Question.objects.all():
	print 'adding slug ' + question.slug
	if not question.slug_fk:
		slugs = Slugs.objects.filter(slug1=question.slug, description=question.text)
		if len(slugs) > 0:
			question.slug_fk = slugs[0]
			question.save()
		else:
			s1 = Slugs(slug1=question.slug, description=question.text)
			s1.save()
			question.slug_fk = s1
			question.save()

print '\nend!'
