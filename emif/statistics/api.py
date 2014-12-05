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

from fingerprint.services import findName

from emif.utils import removehs

import datetime

from questionnaire import Processors, QuestionProcessors, Fingerprint_Summary
from questionnaire.api import QuestionnaireManagement

from django.db.models import Count

from accounts.models import NavigationHistory


from django.conf import settings

import json

import urllib2

import random





class MostViewedFingerprintView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():
            list_viewed = []

            try:
                eprofile = EmifProfile.objects.get(user=request.user)
            except EmifProfile.DoesNotExist:
                print "-- ERROR: Couldn't get emif profile for user"

            most_hit = Hit.objects.filter(user=request.user).values('user','hitcount__object_pk').annotate(total_hits=Count('hitcount')).order_by('-total_hits')

            i=0

            for hit in most_hit:
                try:
                    this_fingerprint = Fingerprint.valid().get(id=hit['hitcount__object_pk'])

                    if eprofile.restricted:
                        try:
                            allowed = RestrictedUserDbs.objects.get(user=request.user, fingerprint=this_fingerprint)
                        except RestrictedUserDbs.DoesNotExist:
                            restricted = RestrictedGroup.hashes(request.user)

                            if this_fingerprint.fingerprint_hash not in RestrictedGroup.hashes(request.user):
                                continue

                    list_viewed.append(
                        {
                            'hash': this_fingerprint.fingerprint_hash,
                            'name': this_fingerprint.findName(),
                            'count': hit['total_hits']
                        })
                    i+=1
                    if i == 10:
                        break

                except Fingerprint.DoesNotExist:
                    print "-- Error on hitcount for fingerprint with id "+hit['hitcount__object_pk']

            response = Response({'mostviewed': list_viewed}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response





############################################################
##### Statistics Database
############################################################

class StatisticsView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():

            questionset = request.GET.get('questionset', 2)
            questionnarie = request.GET.get('questionnarie', '49')
            qm = QuestionnaireManagement(questionnarie)
            questions = qm.questions(questionset)

            db_types = []
            #db_types.append({'name': 'What are?', 'id': '1', 'answers': [{'Yes': '10', 'No': '20', '_T': '30'}]})
            #db_types.append({'name': 'What are?', 'id': '2', 'answers': [{'Yes': '10', 'No': '20', '_T': '30'}]})

            for q in questions:
                d = {'name': q['name'] , 'id': q['id'], 'type': q['type'], 'answers': [{'Yes': '10', 'No': '20', '_T': '30'}]}
                choices = Choice.objects.filter(question=q['obj'])
                for c in choices:
                    d['answers'].append({c.value:c.text})
                db_types.append(d)


            response = Response({'questions': db_types}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response


