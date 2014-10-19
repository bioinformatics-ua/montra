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

from django.shortcuts import render, render_to_response

from django.core import serializers

from django.conf import settings

from django.http import *

from fingerprint.models import Fingerprint, Answer

from questionnaire.models import Question, Questionnaire

from literature.utils import dict_union

import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from public.utils import hasFingerprintPermissions

def literature_database_info_initial(request, fingerprint_id, template_name='literature_info.html'):
    return literature_database_info(request, fingerprint_id, 1, template_name)

# This view shows annotatted publications associated with a determined fingerprint_id,
# or a message saying there's no publications associated, in case there's none yet or
# the questionnaire type doesn't have publications widget
def literature_database_info(request, fingerprint_id, page, template_name='literature_info.html'):

    if not hasFingerprintPermissions(request, fingerprint_id):
        return HttpResponse("Access forbidden",status=403)

    publications = []
    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)

        publications = getListPublications(fingerprint)

    except Fingerprint.DoesNotExist:
        print "--- Literature Error: fingerprint doesnt exist"

    myPaginator = Paginator(publications, 10)
    try:
        pager =  myPaginator.page(page)
    except PageNotAnInteger, e:
        pager =  myPaginator.page(1)
    ## End Paginator ##

    return render(request, template_name, {'request': request, 'fingerprint_id': fingerprint_id, 'publications': pager})

# i could presume 'Publications_t' is always the source, but its better to find out what questions
# are of publications type, and get responses for that,
# since nothing stops uses from having questionary types that have multiple publications widgets

def getListPublications(database):


    # first we find the questionnaire type
    pubquestions = Question.objects.filter(type='publication', questionset__questionnaire=database.questionnaire)

    # we then get the field values themselves
    publications = []
    for pubq in pubquestions:
            string_publications = None

            string_publications = "[]"
            try:
                string_publications = Answer.objects.get(fingerprint_id=database, question=pubq).data

            except Answer.DoesNotExist:
                print "-- Literature Error: Couldnt find answer for publications question"
                pass

            # If we actually have publications defined
            if string_publications != None:
                # for some reason, json.loads returns a dict on no results
                if not string_publications.startswith('['):
                    string_publications = "["+ string_publications+"]"

                if type(publications) == type(json.loads(string_publications)):
                    #print string_publications
                    publications = publications+json.loads(string_publications)

    return publications


# Static, old version
def getListPublicationsStatic(database):
    publications = {}
    string_publications = None

    try:
        string_publications = database['Publications_t']

    except KeyError:
        pass

    # If we actually have publications defined
    if string_publications != None:
        publications = json.loads(string_publications)

    return publications

