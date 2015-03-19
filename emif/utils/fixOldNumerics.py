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
from fingerprint.models import Answer, Fingerprint

def fix():
    q = Question.objects.get(id=5358)
    q.type='numeric'
    q.save()

    ans = Answer.objects.filter(question = q)
    for a in ans:
        a.data=a.data.replace('.', "'")
        a.save()
        a.fingerprint_id.indexFingerprint()

fix()
