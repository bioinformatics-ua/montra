# -*- coding: utf-8 -*-
# Copyright (C) 2014 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo F. Gonçalves Ribeiro <ribeiro.r@ua.pt>
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

from django.db.models.signals import post_save

from questionnaire.tasks import reindexQuestionnaires
from questionnaire.models import Questionnaire, QuestionSet, Question, Choice

def questionnaire_updated(sender, **kwargs):
    reindexQuestionnaires.delay()

post_save.connect(questionnaire_updated, sender=Questionnaire)
post_save.connect(questionnaire_updated, sender=QuestionSet)
post_save.connect(questionnaire_updated, sender=Question)
post_save.connect(questionnaire_updated, sender=Choice)
