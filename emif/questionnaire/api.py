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
#
from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from django.core.cache import cache
from django.db import transaction

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

from questionnaire.models import Questionnaire, QuestionnaireWizard


############################################################
##### New Questionnaire Types - Web service
############################################################

class QuestionnaireWizardView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kw):
        ''' When the request is via get, we return all the questionnaire wizards missing handling
        '''

        if request.user.is_authenticated():
            wiz = []
            types = QuestionnaireWizard.all(user=request.user)

            for wizard in types:
                if not wizard.questionnaire.disable:
                    wiz.append({'id': wizard.id, 'name': wizard.questionnaire.name})

            response = Response({'wizards': wiz}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response

    @transaction.commit_on_success
    def post(self, request, *args, **kw):
        ''' When the request is via post, we handle a response (yes or no to a wizard)
        '''

        if request.user.is_authenticated():
            success = False

            for key, value in request.POST.items():
                key = int(key)
                value = value == '1'
                try:
                    QuestionnaireWizard.objects.get(id=key).interest(value)

                except QuestionnaireWizard.DoesNotExist:
                    print "-- ERROR: Could not retrieve questionnaire wizard with id %r" % key

            response = Response({'success': success}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response
