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
from questionnaire.models import Question, Choice

def fixQuestion():
    q = Question.objects.get(id=7045)
    if q.number == '24.01.02':
        q.type = 'choice-multiple'
        q.text_en = 'h2. Scanner (please specify each):'
        q.save()

        c = Choice.objects.filter(question=q)
        c.delete()

        options = ['Manufacturer', 'Model', 'Installation year', 'Software Version', 'Quality Control Method']
        i=1
        for option in options:
            new_choice = Choice(question=q, sortid=i, value=option, text_en=option)
            new_choice.save()
            i+=1

    else:
        print "-- ERROR: Question with id 7045 is not the question number 24.01.02"

fixQuestion()
