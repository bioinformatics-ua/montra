# -*- coding: utf-8 -*-
# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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


from django.http import HttpResponse

from django.contrib.auth.models import User, Group

from rest_framework import permissions
from rest_framework import renderers
from rest_framework.authentication import TokenAuthentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated

import os
import mimetypes

from questionnaire.models import Questionnaire, Question, Choice

from fingerprint.models import Fingerprint, FingerprintHead, AnswerChange, Answer



from emif.utils import removehs

import datetime

from questionnaire import Processors, QuestionProcessors, Fingerprint_Summary


from django.db.models import Count

from accounts.models import NavigationHistory


from django.conf import settings

import json

import urllib2

import random


from statistics.services import *


class FingerprintSchemas(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, fingerprint_schema_id=None, operation=None, \
         ttype=None,ttype2=None,*args, **kw):

        if request.user.is_authenticated():

            if operation == "all":

                stats = FingerprintSchemaStats(Questionnaire.objects.get(id=fingerprint_schema_id))
                statsList = {}
                statsList['totalDatabases'] = stats.totalDatabases()
                statsList['totalDatabaseOwners'] = stats.totalDatabaseOwners()
                statsList['totalDatabaseShared'] = stats.totalDatabaseShared()
                statsList['maxDatabaseShared'] = stats.maxDatabaseShared()
                statsList['avgDatabaseShared'] = stats.avgDatabaseShared()
                statsList['totalFilledQuestions'] = stats.totalFilledQuestions()
                statsList['maxFilledFingerprints'] = stats.maxFilledFingerprints()
                statsList['minFilledFingerprints'] = stats.minFilledFingerprints()
                statsList['avgFilledFingerprints'] = stats.avgFilledFingerprints()
                statsList['totalDatabaseUsers'] = stats.totalDatabaseUsers()
                statsList['totalInterested'] = stats.totalInterested()

                statsList['maxHitsFingerprints'] = stats.maxHitsFingerprints()
                statsList['minHitsFingerprints'] = stats.minHitsFingerprints()
                statsList['avgHitsFingerprints'] = stats.avgHitsFingerprints()
                statsList['totalHitsFingerprints'] = stats.totalHitsFingerprints()

                statsList['avgUniqueViewsFingerprints'] = stats.avgUniqueViewsFingerprints()
                statsList['maxUniqueViewsFingerprints'] = stats.maxUniqueViewsFingerprints()
                statsList['totalUniqueViewsFingerprints'] = stats.totalUniqueViewsFingerprints()

            else:
                # Not implemented
                # TODO: complete here if you want to respect it:
                response = Response({}, status=status.HTTP_404_NOT_FOUND)

            response = Response({'stats': statsList}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response





