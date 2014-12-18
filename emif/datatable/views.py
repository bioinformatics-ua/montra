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
import csv

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.urlresolvers import *

from django.core.cache import cache
from django.views.decorators.cache import cache_page

from questionnaire.models import QuestionSet, Questionnaire
from questionnaire.services import createhollowqsets, creatematrixqsets

from fingerprint.models import Fingerprint
from django.utils.html import strip_tags

from accounts.models import RestrictedGroup, RestrictedUserDbs, EmifProfile

import hashlib

def get_matrix_data(db_type, qset_post, user, flat=False):

    # generate a mumbo jumbo digest for this combination of parameters, to be used as key for caching purposes
    string_to_be_hashed = "dbtype"+str(db_type)

    for post in qset_post:
        string_to_be_hashed+="qs"+post

    string_to_be_hashed += "_hashed_"+str(flat)

    hashed = hashlib.sha256(string_to_be_hashed).hexdigest()

    titles = None
    answers = None

    cached = cache.get(hashed)

    if cached != None:
        #print "cache hit"
        (titles, answers) = cached

    else :
        #print "need for cache"
        qset_int = []
        for qs in qset_post:
            qset_int.append(int(qs))


        qset = QuestionSet.objects.filter(id__in=qset_int)

        fingerprints = Fingerprint.objects.filter(questionnaire__id=db_type)

        try:
            eprofile = EmifProfile.objects.get(user=user)

            if eprofile.restricted == True:
                hashes = RestrictedGroup.hashes(user)


                others = RestrictedUserDbs.objects.filter(user=user)

                for db in others:
                    hashes.add(db.fingerprint.fingerprint_hash)

                fingerprints = fingerprints.filter(fingerprint_hash__in=hashes)

        except EmifProfile.DoesNotExist:
            print "-- ERROR: Couldn't get emif profile for user"

        (titles, answers) = creatematrixqsets(db_type, fingerprints, qset, flat=flat)

        cache.set(hashed, (titles, answers), 720) # 12 hours of cache

    return (hashed, titles, answers)

def qs_data_table(request, template_name='qs_data_table.html'):
    db_type = int(request.POST.get("db_type"))
    qset_post = request.POST.getlist("qsets[]")

    (hashed, titles, answers) = get_matrix_data(db_type, qset_post, request.user)

    return render(request, template_name, {'request': request,'hash': hashed, 'export_all_answers': True, 'breadcrumb': False, 'collapseall': False, 'geo': False, 'titles': titles, 'answers': answers})

def all_databases_data_table(request, template_name='alldatabases_data_table.html'):
    #dictionary of database types
    databases_types = {}

    # There's no need to show all, we just need the one's with fingerprints
    questionnaires = Questionnaire.objects.filter(fingerprint__pk__isnull=False).distinct()

    # Creating list of database types
    for questionnaire in questionnaires:
        qsets = createhollowqsets(questionnaire.id)

        databases_types[questionnaire] = qsets.ordered_items()

    return render(request, template_name, {'request': request, 'export_datatable': True,
                                           'breadcrumb': True, 'collapseall': False, 'geo': True,
                                           'list_databases': databases_types,
                                           'no_print': True,
                                           'databases_types': databases_types
                                           })

def export_datatable(request):

    db_type = int(request.POST.get("db_type"))
    qset_post = request.POST.getlist("qsets[]")

    (hashed, titles, answers) = get_matrix_data(db_type, qset_post, request.user, flat=True)

    """
    Method to export all databases answers to a csv file
    """
    def clean_str_exp(s):
        s2 = s.replace("\n", "|").replace(";", ",").replace("\t", "    ").replace("\r","").replace("^M","").replace("|", "")

        return re.sub("\s\s+" , " ", s2)



    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+str(hashed)+'.csv"'

    writer = csv.writer(response)

    titles_clean = []
    for title in titles:
        titles_clean.append(title.replace('h0. ','').replace('h1. ','').replace('h2. ','').replace('h3. ','').replace('h4. ','').replace('h5. ','').replace('h6. ','').replace('h7. ',''))

    writer.writerow(titles_clean)

    for title, ans in answers:
        line = [title]
        for a in ans:
            if a != '':
                line.append(clean_str_exp(strip_tags(a[0])))
            else:
                line.append('')
        writer.writerow(line)

    return response

    # list_databases = get_databases_from_solr(request, "*:*")
    # return save_answers_to_csv(list_databases, "DBs")
