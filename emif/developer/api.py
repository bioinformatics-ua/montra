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
from django.conf import settings

from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from django.core.cache import cache

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

from .models import *

from questionnaire.models import Questionnaire
from fingerprint.models import Fingerprint
from accounts.models import Profile, EmifProfile

############################################################
##### Global Plugin - Web services
############################################################

class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['slug','name']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        exclude = ['id', 'password', 'username',
        'user_permissions', 'is_superuser', 'is_staff', 'is_active']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'description']

class EmifProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    interests = QuestionnaireSerializer(many=True)
    profiles = ProfileSerializer(many=True)

    class Meta:
        model = EmifProfile
        exclude = ['id', 'privacy']

class FingerprintSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer()
    owner = serializers.SerializerMethodField(method_name='get_owner')
    shared = serializers.SerializerMethodField(method_name='get_shared')
    name = serializers.SerializerMethodField(method_name='get_name')

    def get_owner(self, obj):
        return obj.owner

    def get_shared(self, obj):
        return obj.shared.all()

    def get_name(self, obj):
        return obj.findName()

    class Meta:
        model = Fingerprint
        exclude = ['id', 'removed', 'description']

## databaseSchemas()
class DatabaseSchemasView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():
            schemas = QuestionnaireSerializer(Questionnaire.objects.filter(disable='False'))

            response = Response({'schemas': schemas.data}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response

## getProfileInformation()
class getProfileInformationView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():
            user = EmifProfileSerializer(request.user.emif_profile)

            response = Response({'profile': user.data}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response

## getFingerprints()
class getFingerprintsView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, quest_slug=None):

        if request.user.is_authenticated():
            q=None
            if quest_slug:
                try:
                    q = Questionnaire.objects.get(slug=quest_slug)
                except Questionnaire.DoesNotExist:
                    return Response({}, status=status.HTTP_403_FORBIDDEN)

            fingerprints = FingerprintSerializer(Fingerprint.valid(questionnaire=q, owner=request.user))

            return Response({'fingerprints': fingerprints.data}, status=status.HTTP_200_OK)



        return Response({}, status=status.HTTP_403_FORBIDDEN)

############################################################






############################################################
##### Checks if a plugin can take a name - Web service
############################################################
class CheckNameView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kw):

        if request.user.is_authenticated():
            success=False

            name = request.POST.get('name', None)
            slug = request.POST.get('slug', None)

            if name != None:
                try:
                    plugin = Plugin.objects.get(name__iexact=name)

                    if plugin.slug == slug:
                        success = True

                except Plugin.DoesNotExist:
                    success = True

            response = Response({'success': success}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response
