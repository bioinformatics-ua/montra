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

from questionnaire.models import Questionnaire, Question

from fingerprint.models import Fingerprint, FingerprintHead, AnswerChange, Answer

from fingerprint.services import findName

from emif.utils import removehs

import datetime

from questionnaire import Processors, QuestionProcessors, Fingerprint_Summary

from django.db.models import Count

from accounts.models import NavigationHistory


from django.conf import settings

import json

import urllib2

import random

from hitcount.models import Hit, HitCount

############################################################
##### Database Types - Web service
############################################################

class DatabaseTypesView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():    
            db_types = []

            types = Questionnaire.objects.filter(fingerprint__pk__isnull=False).distinct()

            for db in types:
                db_types.append({'id': db.id, 'name': db.name})    

            response = Response({'types': db_types}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response

############################################################
##### Most Viewed - Web service
############################################################


class MostViewedView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    def get(self, request, *args, **kw):
        stopwords = ['jerboalistvalues', 'population/comments', 'population/filters', 'population/compare'];
        if request.user.is_authenticated():    
            list_viewed = []
            i = 0

            user_history = user_history = NavigationHistory.objects.filter(user=request.user)
            most_viewed = user_history.values('path').annotate(number_viewed=Count('path')).order_by('-number_viewed')

            for viewed in most_viewed: 
                if i == 10:
                    break  

                if not [stopword for stopword in stopwords if stopword in viewed['path']]:
                    list_viewed.append({'page': viewed['path'], 'count': viewed['number_viewed']})
                    i+=1

            response = Response({'mostviewed': list_viewed}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response

############################################################
##### Most Viewed Fingerprint - Web service
############################################################


class MostViewedFingerprintView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():    
            list_viewed = []

            most_hit = Hit.objects.filter(user=request.user).values('user','hitcount__object_pk').annotate(total_hits=Count('hitcount')).order_by('-total_hits')
            
            i=0

            for hit in most_hit:
                try:
                    this_fingerprint = Fingerprint.valid().get(id=hit['hitcount__object_pk'])

                    list_viewed.append(
                        {
                            'hash': this_fingerprint.fingerprint_hash,
                            'name': findName(this_fingerprint),
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
##### Last Users - Web service
############################################################


class LastUsersView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    def get(self, request, *args, **kw):

        if request.user.is_authenticated() and request.user.is_staff == True:    
            last_users = []

            users = User.objects.all().order_by('-last_login')[:10]

            for user in users:
                last_users.append(user.username)

            response = Response({'lastusers': last_users}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response

############################################################
##### User Statistics - Web service
############################################################


class UserStatsView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():    
            stats = {}

            # statistics about the user
            # number of databases as owner
            # number of dbs as a shared user
            # most popular database of this user(with most unique views)
            # main database type

            stats['lastlogin'] = request.user.last_login.strftime("%Y-%m-%d %H:%M:%S") 

            my_db = Fingerprint.objects.filter(owner=request.user).order_by('-hits')
            my_db_share = Fingerprint.objects.filter(shared=request.user) 

            stats['numberownerdb'] = my_db.count()
            stats['numbershareddb'] = my_db_share.count()

            mostpopular = None
            try:
                mostpopular = my_db[0]
            except:
                # no database owned
                pass

            if mostpopular == None:
                stats['mostpopulardb'] = {'name': '---', 'hash': '---', 'hits': '---'}
            else:
                stats['mostpopulardb'] = {
                                    'name': findName(mostpopular), 
                                    'hash': mostpopular.fingerprint_hash,
                                    'hits': mostpopular.hits}

            all_dbs = my_db | my_db_share

            quest_types = all_dbs.order_by('questionnaire').values('questionnaire__name').annotate(Count('questionnaire')).order_by('-questionnaire__count')

            try:
                stats['populartype'] = quest_types[0]['questionnaire__name']
            except:
                stats['populartype'] = "---"

            response = Response({'stats': stats}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response


############################################################
##### Feed - Web service
############################################################


class FeedView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():    
            
            modifications = FingerprintHead.objects.filter(fingerprint_id__owner=request.user)

            modifications = modifications | FingerprintHead.objects.filter(fingerprint_id__shared=request.user).order_by("-date")

            feed = []

            modifications = modifications[:50]   

            aggregate = []
            previous = None
            for mod in modifications:
                
                if previous != None and mod.fingerprint_id != previous.fingerprint_id and len(aggregate) != 0:
                    feed.append(aggregate)
                    aggregate = []

                alterations = []

                anschg = AnswerChange.objects.filter(revision_head = mod)


                for chg in anschg:

                    question = chg.answer.question

                    try:
                        old_value = Fingerprint_Summary[question.type](chg.old_value)
                        new_value = Fingerprint_Summary[question.type](chg.new_value)
                    except:
                        old_value = chg.old_value
                        new_value = chg.new_value

                    alterations.append({
                            'number': question.number,
                            'text': removehs(question.text),
                            'oldvalue': old_value,
                            'newvalue': new_value,
                            'oldcomment': chg.old_comment,
                            'newcomment': chg.new_comment
                        })

                aggregate.append({
                    'hash': mod.fingerprint_id.fingerprint_hash,
                    'name': findName(mod.fingerprint_id),
                    'date': mod.date.strftime("%Y-%m-%d %H:%M"),
                    'icon': 'edit',
                    'alterations': alterations,
                    'revision': mod.revision
                })

                previous = mod

            feed.append(aggregate)

            response = Response({'hasfeed': True, 'feed': feed }, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response

############################################################
##### Tag Cloud - Web service
############################################################


class TagCloudView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    def get(self, request, *args, **kw):

        if request.user.is_authenticated():    

            tags = []

            solrlink = 'http://' +settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH+'/admin/luke?fl=text_t&numTerms=50&wt=json'

            stopwords = ['yes', 'and', 'not', 'the', 'for', 'all', 'more', 'with', 'than', 'please']

            topwords = json.load(urllib2.urlopen(solrlink))['fields']['text_t']['topTerms']

            i = 0

            while i < len(topwords):
                if len(topwords[i]) > 2 and topwords[i] not in stopwords:
                    tags.append({
                        'name': topwords[i],
                        'relevance': topwords[i+1],
                        'link': 'resultsdiff/1'
                    })

                if len(tags) >= 20:
                    break

                i+=2

            random.shuffle(tags, random.random)
            
         
            response = Response({'tags': tags}, status=status.HTTP_200_OK)

        else:
            response = Response({}, status=status.HTTP_403_FORBIDDEN)
        return response