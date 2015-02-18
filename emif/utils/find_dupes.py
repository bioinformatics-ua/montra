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
from questionnaire.models import Question, Questionnaire
from searchengine.models import Slugs
from questionnaire.utils import next_free_slug

def findDupes(q_slug):

    try:
        repeated_slugs = {}

        questionnaire = Questionnaire.objects.get(slug=q_slug)

        questions = Question.objects.filter(questionset__questionnaire=questionnaire).values_list('slug_fk__slug1', flat=True).distinct()

        for question in questions:
            qsts = Question.objects.filter(questionset__questionnaire=questionnaire, slug_fk__slug1=question)
            size = len(qsts)
            if size > 1:
                repeated_slugs[question] = qsts


        print "REPEATED SLUGS: "+str(len(repeated_slugs))
        for r in repeated_slugs:
            working_tag = r
            if r.endswith('_0'):
                working_tag = r[:-2]

            print working_tag
            for question in repeated_slugs[r][1:]:
                slug = next_free_slug(working_tag)
                if slug != None:
                    question.slug_fk = slug

                    print "Setting slug as "+str(slug.slug1)
                    question.slug = slug.slug1

                    question.save()

                else:
                    print "-- Error retrieving next free slug."

    except Questionnaire.DoesNotExist:
        print "Error retrieving questionnaire with slug "+str(q_slug)

print "[ Taking a look at adcohort ]"
findDupes('adcohort')
print "[ Taking a look at observational data sources ]"
findDupes('observationaldatasources')
