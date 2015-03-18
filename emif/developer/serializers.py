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
from django.contrib.auth.models import User, Group

from rest_framework import serializers

from questionnaire.models import Questionnaire, Question
from fingerprint.models import Fingerprint, Answer
from accounts.models import Profile, EmifProfile
from docs_manager.models import Document

from django.db.models.loading import get_model

FingerprintAPI = get_model('api', 'FingerprintAPI')

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

class QuestionSerializer(serializers.ModelSerializer):
    disposition = serializers.SerializerMethodField(method_name='getDisp')
    questionset = serializers.SerializerMethodField(method_name='getQuestionset')

    def getDisp(self, obj):
        return dict(Question.DISPOSITION_TYPES)[obj.disposition]

    def getQuestionset(self, obj):
        return obj.questionset.text


    class Meta:
        model = Question
        exclude = ['id', 'checks', 'extra_en',
        'footer_en', 'slug_fk', 'stats',
        'metadata', 'mlt_ignore', 'tooltip']

class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ['question', 'data']

class FingerprintAPISerializer(serializers.ModelSerializer):
    pass
    class Meta:
        model = FingerprintAPI
        exclude = ['id', 'fingerprintID', 'user']

class DocumentSerializer(serializers.ModelSerializer):
    pass
    class Meta:
        model = Document
        exclude = ['id', 'fingerprint_id', 'removed']
