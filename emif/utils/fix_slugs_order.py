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
from questionnaire.models import Questionnaire, QuestionSet, Question
from searchengine.models import Slugs
import sys

print '\nbegin fixing slugs on adcohort ...\n'

quest = Questionnaire.objects.filter(slug='adcohort')[0]
qset = QuestionSet.objects.filter(questionnaire=quest)[0]
temp_slug = None

dbname = Question.objects.get(slug='database_name', questionset = qset)
dbacronym = Question.objects.get(slug='Cohort_acronym', questionset = qset)

temp_slug = dbname.slug_fk
temp_type =dbname.type

dbname.slug_fk = dbacronym.slug_fk
dbacronym.slug_fk = temp_slug

dbname.type = dbacronym.type
dbacronym.type = temp_type

dbname.slug = 'Cohort_acronym'
dbacronym.slug = 'database_name'

dbname.save()

dbacronym.save()

print '\nend!'
