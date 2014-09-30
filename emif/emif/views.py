# -*- coding: utf-8 -*-

# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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
from pprint import pprint

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.urlresolvers import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from emif.utils import QuestionGroup, ordered_dict

from questionnaire.models import *
from questionnaire.parsers import *
from questionnaire.views import *
from questionnaire.models import *
from searchengine.search_indexes import CoreEngine
from searchengine.models import Slugs
import searchengine.search_indexes
from searchengine.search_indexes import index_answeres_from_qvalues
from searchengine.search_indexes import convert_text_to_slug
from emif.utils import *
from emif.models import *

from fingerprint.services import *
from fingerprint.models import *

from api.models import *

from geopy import geocoders
from django.core.mail import BadHeaderError

from emif.utils import send_custom_mail

from rest_framework.authtoken.models import Token

from django.contrib.auth.decorators import login_required

from django.utils.html import strip_tags
from django.utils import simplejson

import json
import logging
import re
import md5
import random

import os
import os.path
import time

import base64

from django.core.cache import cache

from django.views.decorators.cache import cache_page

import hashlib

from emif.utils import escapeSolrArg

from notifications.models import Notification
    
from fingerprint.tasks import anotateshowonresults

from fingerprint.views import show_fingerprint_page_read_only, render_one_questionset

def index(request, template_name='index_new.html'):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.BASE_URL + 'wherenext')
    else:
        return render(request, template_name, {'request': request})

def about(request, template_name='about.html'):
    return render(request, template_name, {'request': request, 'breadcrumb': True})

def bootstrap_ie_compatibility(request, template_name='bootstrap_ie_compatibility.css'):
    return render(request, template_name, {'request': request, 'breadcrumb': False})

def results_comp(request, template_name='results_comp.html'):
    list_fingerprint_to_compare = []

    if request.POST:
        for k, v in request.POST.items():
            if k.startswith("chks_") and v == "on":
                arr = k.split("_")

                list_fingerprint_to_compare.append(arr[1])

    class Results:
        num_results = 0
        list_results = []

    class DatabaseFields:
        id = ''
        name = ''
        date = ''
        fields = None

    first_name = None
    list_qsets = {}
    for db_id in list_fingerprint_to_compare:
        qsets, name, db_owners, fingerprint_ttype = createqsets(db_id)

        list_qsets[db_id] = { 'name': name, 'qset': qsets}

        if(first_name == None):
            first_name = name

    '''for fingerprint_id, (name, qset) in list_qsets.items:
        print "--------------------------------"
        print content['name']
    '''

    return render(request, template_name, {'request': request, 'breadcrumb': True,
                                           'results': list_qsets, 'database_to_compare': first_name})


def results_fulltext(request, page=1, full_text=True,template_name='results.html', isAdvanced=False, query_reference=None):
    query = ""
    in_post = True
    try:
        query = request.POST['query']
        request.session['query'] = query
    except:
        in_post = False

    if not in_post:
        query = request.session.get("query","")

    if isAdvanced == False:
        query = "text_t:"+escapeSolrArg(query)
        #print query

    return results_fulltext_aux(request, query, page, template_name, isAdvanced=isAdvanced, query_reference=query_reference)


def results_fulltext_aux(request, query, page=1, template_name='results.html', isAdvanced=False, force=False, query_reference=None):

    rows = define_rows(request)
    if request.POST and "page" in request.POST and not force:
        page = request.POST["page"]

    if page == None:
        page = 1

    if query == "" or query == "text_t:" or query.strip()=="text_t:*" :
        return render(request, "results.html", {'request': request, 'breadcrumb': True,  'isSearch': True,
                                                'results': True, 'hide_add': True,
                                                'num_results': 0, 'page_obj': None})

    query = query + " AND " + typeFilter(request.user)

    (sortString, filterString, sort_params, range) = paginator_process_params(request.POST, page, rows)
    sort_params["base_filter"] = query;
    query_filtered=query
    if len(filterString) > 0:
        query_filtered += " AND " + filterString

    (list_databases, hits, hi) = get_databases_from_solr_with_highlight(request, query_filtered, sort=sortString, rows=rows, start=range)
    if not isAdvanced:
        hi = merge_highlight_results( '"'+escapeSolrArg(request.session["query"])+'"' , hi)
    else:
        hi = merge_highlight_results( None , hi)


    if range > hits and not force:
        return results_fulltext_aux(request, query, 1, isAdvanced=isAdvanced, force=True)

    request.session["highlight_results"] = hi

    if len(list_databases) == 0 :
        query_old = request.session.get('query', "")
        if isAdvanced == True:
            return render(request, "results.html", {'request': request, 'breadcrumb': True,  'isSearch': True,
                                                'results': True, 'hide_add': True,
                                                'num_results': 0, 'page_obj': None, 'isAdvanced': True})
        else:
            return render(request, "results.html", {'request': request, 'breadcrumb': True, 'isSearch': True,
                                                'results': True, 'hide_add': True,
                                                'num_results': 0, 'page_obj': None, 'search_old': query_old, 'isAdvanced': False})

    list_databases = paginator_process_list(list_databases, hits, range)

    # only execute if this if we are not posting back, we dont want to do this on changing page or applying filters
    if request.POST.get('page') == None and query_reference != None:
        # anotate the databases appearing on results
        anotateshowonresults.delay(query_filtered, request.user, isAdvanced, query_reference)

    myPaginator = Paginator(list_databases, rows)
    try:
        pager =  myPaginator.page(page)
    except PageNotAnInteger, e:
        pager =  myPaginator.page(page)

    query_old = request.session.get('query', "")


    if isAdvanced == True:
        return render(request, template_name, {'request': request,
                                           'num_results': hits, 'page_obj': pager, 'page_rows': rows, 'isSearch': True,
                                           'results': True, 'hide_add': True,
                                           'breadcrumb': True, 'isAdvanced': True, "sort_params": sort_params, "page":page})
    else :
        return render(request, template_name, {'request': request, 'isSearch': True,
                                           'results': True, 'hide_add': True,
                                           'num_results': hits, 'page_obj': pager, 'page_rows': rows,'breadcrumb': True, 'search_old': query_old, 'isAdvanced': False, "sort_params": sort_params, "page":page})

def typeFilter(user):
    emifprofile = user.get_profile()
    interests = emifprofile.interests.all()

    type_t_list = ""
    if interests:
        for i in interests:
            type_t = i.slug.replace(" ", "").lower()
            type_t_list+=(type_t + ",")

        type_t_list = type_t_list[:-1]

        return "type_t:" + type_t_list

def store_query(user_request, query_executed):
    #print user_request.user.is_authenticated()
    #print "Store Query2"

    query = QueryLog()
    if user_request.user.is_authenticated():
        query.user = user_request.user
    else:
        query.user = None

    query.query = query_executed

    query.save()

    return query


def results_diff(request, page=1, template_name='results.html'):

    # in case the request come's from a advanced search

    if request.POST.get("qid") != None:

        request.session['isAdvanced'] = True
        qlist = []
        jsinclude = []      # js files to include
        cssinclude = []     # css files to include
        jstriggers = []
        qvalues = {}
        qexpression = None  # boolean expression
        qserialization = None   # boolean expression serialization to show on results
        qid = None  #questionary id
        if request.POST:
            for k, v in request.POST.items():

                if (len(v)==0):
                    continue
                if k.startswith("question_"):
                    s = k.split("_")
                    if len(s) == 4:
                        #qvalues[s[1]+'_'+v] = '1' # evaluates true in JS
                        if (qvalues.has_key(s[1])):
                            qvalues[s[1]] += " " + v # evaluates true in JS
                        else:
                            qvalues[s[1]] = v # evaluates true in JS
                    elif len(s) == 3 and s[2] == 'comment':
                        qvalues[s[1] + '_' + s[2]] = v
                    else:
                        if (qvalues.has_key(s[1])):
                            qvalues[s[1]] += " " + v
                        else:
                            qvalues[s[1]] = v
                            #print qvalues
                elif k == "boolrelwidget-boolean-representation":
                    qexpression = v
                elif k == "boolrelwidget-boolean-serialization":
                    # we add the serialization to the session
                    request.session['serialization_query'] = v
                    qserialization = v
                elif k == "qid":
                    qid = v

            if qexpression == None or qserialization == None or qexpression.strip()=="" or qserialization.strip() == "":
                response = HttpResponse()
                response.status_code = 500
                return response

            query = convert_qvalues_to_query(qvalues, qid, qexpression)
            query = convert_query_from_boolean_widget(qexpression, qid)
            #print "Query: " + query


            request.session['query'] = query

            # We will be saving the query on to the serverside to be able to pull it all together at a later date
            try:
                # we get the current user
                this_user = User.objects.get(username = request.user)

                this_query = None

                this_query_hash = hashlib.sha1(qserialization).hexdigest()

                #print "This query is new, adding it and answers to it..."

                quest = None
                try:
                    quest = Questionnaire.objects.get(id = qid)
                except Questionnaire.DoesNotExist:
                    print "Questionnaire doesnt exist..."

                this_query = AdvancedQuery(user=this_user,name=("Query on "+time.strftime("%c")),
                    serialized_query_hash=this_query_hash,
                    serialized_query=qserialization, qid=quest)
                this_query.save()
                # and we all so insert the answers in a specific table exactly as they were on the post request to be able to put it back at a later time
                for k, v in request.POST.items():
                    if k.startswith("question_") and len(v) > 0:
                        aqa = AdvancedQueryAnswer(refquery=this_query,question=k, answer=v)
                        aqa.save()

                serialization_a = AdvancedQueryAnswer(refquery=this_query, question="boolrelwidget-boolean-representation", answer=qexpression)
                serialization_a.save()

                request.session['query_id'] = this_query.id
                request.session['query_type'] = this_query.qid.id

            except User.DoesNotExist:
                return HttpResponse("Invalid username")



            return results_fulltext_aux(request, query, isAdvanced=True, query_reference=this_query)



    query = ""
    simple_query=None
    in_post = True
    try:
        query = request.POST['query']

        # must save only on post, and without the escaping so it doesnt encadeate escapes on queries remade
        if query != "" and request.POST.get('page') == None:
            simple_query = store_query(request, query)

        query = '"'+escapeSolrArg(query)+'"'

        request.session['query'] = query

        request.session['isAdvanced'] = False
        request.session['query_id'] = -1
        request.session['query_type'] = -1
    except:
        in_post = False
        #raise
    if not in_post:
        query = request.session.get('query', "")

    if query == "":
        return render(request, "results.html", {'request': request,
                                                'num_results': 0, 'page_obj': None, 'breadcrumb': True})
    try:
        # Store query by the user
        if 'search_full' in request.POST:
            search_full = request.POST['search_full']
            request.session['search_full'] = 'search_full'
        else:
            print "try to get in session"
            search_full = request.session.get('search_full', "")
        if search_full == "search_full":
            return results_fulltext(request, page, full_text=True, isAdvanced=request.session['isAdvanced'], query_reference=simple_query)
    except:
        raise
    #print "Printing the qexpression"
    #print request.POST['qexpression']
    return results_fulltext(request, page, full_text=False, isAdvanced=request.session['isAdvanced'], query_reference=simple_query)

def statistics(request, questionnaire_id, question_set, template_name='statistics.html'):

    from emif.statistics import Statistic


    # print "QUESTIONNAIRE_ID: " + str(questionnaire_id)
    # print "QUESTION_SET: " + str(question_set)

    qs_list = QuestionSet.objects.filter(questionnaire=questionnaire_id).order_by('sortid')

    if int(question_set) == 99:
        question_set = len(qs_list) - 1
    question_set = qs_list[int(question_set)]

    questions = Question.objects.filter(questionset=question_set)

    return render(request, template_name, {'request': request, 'questionset': question_set,
                                           'breadcrumb': True, 'questions_list': questions,
                                           'questionnaire_id': questionnaire_id})


def generate_statistics_from_multiple_choice(question_slug):
    choices = Choice.objects.filter(question=q)
    total_values = calculate_total_values()
    c = CoreEngine()
    for choice in choices:
        query = "question_slug:" + "choice.value"
        results = c.search_fingerprint(query)
        number_results = len(results)


def calculate_databases_per_location():
    users = EmifProfile.objects.all()
    c = CoreEngine()
    contries = []
    for u in users:
        # Count number of DB's for each user
        query = "subject_id_t:" + u.user.id
        results = c.search_fingerprint(query)
        # Number of dbs
        number_of_dbs = len(results)
        if contries.has_key(u.contry.name):
            contries[u.contry.name] = contries[u.contry.name] + number_of_dbs
        else:
            contries[u.contry.name] = number_of_dbs


def get_databases_from_solr(request, query="*:*"):

    (list_databases, hits) = get_databases_from_solr_v2(request, query=query);

    return list_databases

def __get_scientific_contact(db, db_solr, type_name):
    #print "type_name" + type_name
    #print "type_name"
    if type_name == "Observational Data Sources":
        if (db_solr.has_key('institution_name_t')):
            db.admin_name = db_solr['institution_name_t']
        if (db_solr.has_key('Administrative_contact_address_t')):
            db.admin_address = db_solr['Administrative_contact_address_t']
        if (db_solr.has_key('Administrative_contact_email_t')):
            db.admin_email = db_solr['Administrative_contact_email_t']
        if (db_solr.has_key('Administrative_contact_phone_t')):
            db.admin_phone = db_solr['Administrative_contact_phone_t']


        if (db_solr.has_key('Scientific_contact_name_t')):
            db.scien_name = db_solr['Scientific_contact_name_t']
        if (db_solr.has_key('Scientific_contact_address_t')):
            db.scien_address = db_solr['Scientific_contact_address_t']

        if (db_solr.has_key('Scientific_contact_email_t')):
            db.scien_email = db_solr['Scientific_contact_email_t']
        if (db_solr.has_key('Scientific_contact_phone_t')):
            db.scien_phone = db_solr['Scientific_contact_phone_t']


        if (db_solr.has_key('Technical_contact_/_data_manager_contact_name_t')):
            db.tec_name = db_solr['Technical_contact_/_data_manager_contact_name_t']
        if (db_solr.has_key('Technical_contact_/_data_manager_contact_address_t')):
            db.tec_address = db_solr['Technical_contact_/_data_manager_contact_address_t']
        if (db_solr.has_key('Technical_contact_/_data_manager_contact_email_t')):
            db.tec_email = db_solr['Technical_contact_/_data_manager_contact_email_t']
        if (db_solr.has_key('Technical_contact_/_data_manager_contact_phone_t')):
            db.tec_phone = db_solr['Technical_contact_/_data_manager_contact_phone_t']

    elif "AD Cohort" in type_name :

        if (db_solr.has_key('Administrative_Contact__AC___Name_t')):
            db.admin_name = db_solr['Administrative_Contact__AC___Name_t']
        if (db_solr.has_key('AC__Address_t')):
            db.admin_address = db_solr['AC__Address_t']
        if (db_solr.has_key('AC__email_t')):
            db.admin_email = db_solr['AC__email_t']
        if (db_solr.has_key('AC__phone_t')):
            db.admin_phone = db_solr['AC__phone_t']

        if (db_solr.has_key('Scientific_Contact__SC___Name_t')):
            db.scien_name = db_solr['Scientific_Contact__SC___Name_t']
        if (db_solr.has_key('SC__Address_t')):
            db.scien_address = db_solr['SC__Address_t']
        if (db_solr.has_key('SC__email_t')):
            db.scien_email = db_solr['SC__email_t']
        if (db_solr.has_key('SC__phone_t')):
            db.scien_phone = db_solr['SC__phone_t']

        if (db_solr.has_key('Technical_Contact_Data_manager__TC___Name_t')):
            db.tec_name = db_solr['Technical_Contact_Data_manager__TC___Name_t']
        if (db_solr.has_key('TC__Address_t')):
            db.tec_address = db_solr['TC__Address_t']
        if (db_solr.has_key('TC__email_t')):
            db.tec_email = db_solr['TC__email_t']
        if (db_solr.has_key('TC__phone_t')):
            db.tec_phone = db_solr['TC__phone_t']

    return db


def get_databases_process_results(results):
    #print "Solr"
    list_databases = []
    questionnaires_ids = {}
    qqs = Questionnaire.objects.all()
    for q in qqs:
        questionnaires_ids[q.slug] = (q.pk, q.name)

    for r in results:
        try:
            database_aux = Database()

            database_aux.id = r['id']

            if (not r.has_key('created_t')):
                database_aux.date = ''
            else:

                try:
                    database_aux.date = convert_date(r['created_t'])
                except:
                    database_aux.date = ''


            if (not r.has_key('date_last_modification_t')):
                database_aux.date_modification = convert_date(r['created_t'])
            else:

                try:
                    database_aux.date_modification = convert_date(r['date_last_modification_t'])
                except:
                    database_aux.date_modification = convert_date(r['created_t'])

            if (not r.has_key('database_name_t')):
                database_aux.name = '(Unnamed)'
            else:
                database_aux.name = r['database_name_t']

            database_aux.localtion = ''

            if(r.has_key('city_t')):
                database_aux.location = r['city_t']
            if (r.has_key('location_t')):
                database_aux.location = r['location_t']
            if (r.has_key('PI:_Address_t')):
                database_aux.location = r['PI:_Address_t']
            if (r.has_key('AC__Address_t')):
                database_aux.location = r['AC__Address_t']
            if (r.has_key('TC__Address_t')):
                database_aux.location = r['TC__Address_t']

            if (not r.has_key('institution_name_t')):
                database_aux.institution = ''
            else:
                database_aux.institution = r['institution_name_t']

            if (not r.has_key('contact_administrative_t')):
                database_aux.email_contact = ''
            else:
                database_aux.email_contact = r['contact_administrative_t']

            if (not r.has_key('number_active_patients_jan2012_t')):
                database_aux.number_patients = ''
            else:
                database_aux.number_patients = r['number_active_patients_jan2012_t']

            if (not r.has_key('date_last_modification_t')):
                database_aux.last_activity = ''
            else:
                database_aux.last_activity = r['date_last_modification_t']

            if (not r.has_key('upload-image_t')):
                database_aux.logo = 'nopic.gif'
            else:
                database_aux.logo = r['upload-image_t']

            (ttype, type_name) = questionnaires_ids[r['type_t']]
            database_aux.ttype = ttype
            database_aux.type_name = type_name
            database_aux = __get_scientific_contact(database_aux, r, database_aux.type_name)
            #import pdb
            #pdb.set_trace()
            list_databases.append(database_aux)
        except Exception, e:
            print e
            pass

    return list_databases

def get_databases_from_solr_v2(request, query="*:*", sort="", rows=100, start=0, fl='',post_process=None):
    c = CoreEngine()
    results = c.search_fingerprint(query, sort=sort, rows=rows, start=start, fl=fl)

    list_databases = get_databases_process_results(results)

    if post_process:
        list_databases = post_process(results, list_databases)

    return (list_databases,results.hits)

def get_query_from_more_like_this(doc_id, maxx=100):
    c = CoreEngine()
    #results = c.search_fingerprint(query, sort=sort, rows=rows, start=start)
    results = c.more_like_this(doc_id, maxx=maxx)


    if len(results)>0:
        queryString = "id:("
        for r in results:
            if "id" in r:
                queryString = queryString + r["id"]+"^"+str(r["score"])+ " "

        queryString = queryString + ")"
    else:
        queryString = None

    ## PY SOLR IS STUPID, OTHERWISE THIS WOULD BE AVOIDED
    database_name = ""
    results = c.search_fingerprint("id:"+doc_id, start=0, rows=1, fl="database_name_t")
    for r in results:
        if "database_name_t" in r:
            database_name = r["database_name_t"]

    return (queryString, database_name)

def get_databases_from_solr_with_highlight(request, query="*:*", sort="", rows=100, start=0):
    c = CoreEngine()
    results = c.search_highlight(query, sort=sort, rows=rows, start=start, hlfl="*")

    list_databases = get_databases_process_results(results)

    return (list_databases,results.hits, results.highlighting)

def merge_highlight_results(query, resultHighlights):
    c = CoreEngine()
    h = {}
    h["results"] = resultHighlights

    if query:
        qresults = c.highlight_questions(query)
        h["questions"] = qresults.highlighting

    return h

def delete_fingerprint(request, id):

    deleteFingerprint(id, request.user)

    return redirect('databases')

def query_solr(request, page=1):
    if not request.POST:
        return

    # Get the list of databases for a specific user
    _filter = request.POST["filter"];
    #print _filter
    rows = 5
    if page == None:
        page = 1

    (sortString, filterString, sort_params, range) = paginator_process_params(request.POST, page, rows)

    #print filterString

    if len(filterString) > 0:
        _filter += " AND " + filterString

    #print _filter

    (list_databases,hits) = get_databases_from_solr_v2(request, _filter, sort=sortString, rows=rows, start=range)

    #print "Range: "+str(range)
    #print "hits: "+str(hits)
    #print "len: "+str(len(list_databases))

    list_databases = paginator_process_list(list_databases, hits, range)

    ret = {}
    ret["Hits"] = hits
    ret["Start"] = range
    ret["Rows"] = rows
    ret["Filter"] = filterString
    if range > hits:
        ret["Rec_Page"] = 1
    else:
        ret["Rec_Page"] = page

    return HttpResponse(json.dumps(ret), mimetype='application/json')

def databases(request, page=1, template_name='results.html', force=False):

     #first lets clean the query session log
    if 'query' in request.session:
        del request.session['query']

    if 'isAdvanced' in request.session:
        del request.session['isAdvanced']

    if 'query_id' in request.session:
        del request.session['query_id']
    if 'query_type' in request.session:
        del request.session['query_type']

    request.session['list_origin'] = 'personal'

    # Get the list of databases for a specific user
    user = request.user

    _filter = "user_t:" + '"' + user.username + '"'
    if user.is_superuser:
        _filter = "user_t:*"

    rows = define_rows(request)
    if request.POST and not force:
        page = request.POST["page"]

    if page == None:
        page = 1

    (sortString, filterString, sort_params, range) = paginator_process_params(request.POST, page, rows)

    sort_params["base_filter"] = _filter;

    #print filterString

    if len(filterString) > 0:
        _filter += " AND " + filterString

    #print _filter

    (list_databases,hits) = get_databases_from_solr_v2(request, _filter, sort=sortString, rows=rows, start=range)
    if range > hits and force < 2:
        return databases(request, page=1, force=True)

    #print "Range: "+str(range)
    #print "hits: "+str(hits)
    #print "len: "+str(len(list_databases))

    list_databases = paginator_process_list(list_databases, hits, range)

    #print "len: "+str(len(list_databases))
    ## Paginator ##
    myPaginator = Paginator(list_databases, rows)
    try:
        pager =  myPaginator.page(page)
    except PageNotAnInteger, e:
        pager =  myPaginator.page(page)
    ## End Paginator ##
    #print list_databases

    return render(request, template_name, {'request': request, 'export_my_answers': True,
                                           'list_databases': list_databases, 'breadcrumb': True, 'collapseall': False,
                                           'page_obj': pager, 'page_rows': rows,
                                           'api_token': True,
                                           'owner_fingerprint': False,
                                           'databases': True,
                                           'add_databases': True, "sort_params": sort_params, "page":page})

def paginator_process_params(request, page, rows, default_mode={"database_name": "asc"}):
    sortFieldsLookup = {}
    sortFieldsLookup["database_name"] = "database_name_sort"
    sortFieldsLookup["last_update"] = "last_activity_sort"
    sortFieldsLookup["type"] = "type_name_sort"

    sortFieldsLookup["institution"] = "institution_sort"
    sortFieldsLookup["location"] = "location_sort"
    sortFieldsLookup["nrpatients"] = "nrpatients_sort"

    sortFieldsLookup["score"] = "score"


    filterFieldsLookup = {}
    filterFieldsLookup["database_name_filter"] = "database_name_sort"
    filterFieldsLookup["last_update_filter"] = ""
    filterFieldsLookup["type_filter"] = "type_t"

    filterFieldsLookup["institution_filter"] = "institution_name_t"#"institution_sort"
    filterFieldsLookup["location_filter"] = "location_sort"
    filterFieldsLookup["nrpatients_filter"] = "number_active_patients_jan2012_t"

    prefixFilters = []
    openTextFilters = ["database_name_filter", "institution_filter", "location_filter"]

    sortString = ""
    filterString = ""
    sort_params= {}
    #print request
    if "s" in request:
        mode = json.loads(request["s"])
    else:
        mode = default_mode

    for x in mode:
        if sortFieldsLookup.has_key(x):
            if mode[x] == "asc" or mode[x] == "desc":
                sortString += sortFieldsLookup[x]+" "+mode[x]
                if x not in sort_params:
                    sort_params[x] = {}
                sort_params[x]["name"] = mode[x]
        elif len(mode[x])>0 and filterFieldsLookup.has_key(x):
            if x == "last_update_filter":
                filterString += "(created_t:\""+mode[x] + "\" OR date_last_modification_t:\""+mode[x] + "\") AND "
            elif x in prefixFilters:
                p = re.compile("([^a-z])")
                str2 = re.sub(p, "", mode[x].lower())
                filterString += "({!prefix f="+filterFieldsLookup[x]+"}"+str2+") AND "
            elif x in openTextFilters:
                filterString += "("+filterFieldsLookup[x]+":*"+mode[x] +"*) AND "
            else:
                filterString += filterFieldsLookup[x]+":'"+mode[x] +"' AND "
            if x[:-7] not in sort_params:
                sort_params[x[:-7]] = {}
            sort_params[x[:-7]]["filter"] = mode[x]
            #print sort_params

    if len(filterString) > 0:
        filterString = filterString[:-4]

    for x in ["database_name", "last_update", "type", "institution", "location", "nrpatients", "score"]:
        if (x in sort_params) and ( "name" in sort_params[x]):
            sort_params["selected_name"] = x
            sort_params["selected_value"] = sort_params[x]["name"]
            if sort_params[x]["name"] == "asc":
                sort_params[x]["click_url"]='?s={"'+x+'":"desc"}'
                sort_params[x]["next"]='desc'
                sort_params[x]["icon"]="icon-chevron-down"
            elif sort_params[x]["name"] == "desc":
                sort_params[x]["click_url"]='?s={"'+x+'":"asc"}'
                sort_params[x]["next"]='asc'
                sort_params[x]["icon"]="icon-chevron-up"
        else:
            if x not in sort_params:
                sort_params[x] = {}
            sort_params[x]["click_url"]='?s={"'+x+'":"asc"}'
            sort_params[x]["next"]='asc'
            sort_params[x]["icon"]="icon-minus"

    #print sortString

    start = (int(page) - 1) * rows

    #print mode
    if "extraObjects" in mode:
        extraObjects = mode["extraObjects"]
    else:
        extraObjects = {}
    sort_params["extraObjects"] = json.dumps(extraObjects)
    #print sort_params
    return (sortString, filterString, sort_params, start)

def paginator_process_list(list_databases, hits, start):
    nList = []

    for x in xrange(0,start):
        nList.append(None)
    nList.extend(list_databases)
    while len(nList)<hits:
        nList.append(None)

    return nList

def define_rows(request):
    if request.POST and "page_rows" in request.POST:
        rows = int(request.POST["page_rows"])

        profile = request.user.get_profile()

        profile.paginator = rows

        profile.save()

    else:
        # Otherwise get number of rows from preferences
        rows = 5

        try:
            profile = request.user.get_profile()

            rows = profile.paginator

        except:
            pass

    if rows == -1:
        rows = 99999

    return rows
# GET ALL DATABASES ACCORDING TO USER INTERESTS
def all_databases_user(request, page=1, template_name='results.html', force=False):

    rows = define_rows(request)

    if request.POST and not force:
        page = request.POST["page"]

    if page == None:
        page = 1
    # lets clear the geolocation session search filter (if any)
    try:
        del request.session['query']
        del request.session['isAdvanced']
        del request.session['serialized_query']
    except:
        pass

    request.session['list_origin'] = 'all'

    emifprofile = request.user.get_profile()
    interests = emifprofile.interests.all()

    type_t_list = ""
    if interests:
        for i in interests:
            type_t = i.slug.replace(" ", "").lower()
            type_t_list+=(type_t + ",")

        type_t_list = type_t_list[:-1]

        query = "type_t:" + type_t_list
        (sortString, filterString, sort_params, start) = paginator_process_params(request.POST, page, rows)
        sort_params["base_filter"] = query;
        if len(filterString) > 0:
            query += " AND " + filterString

        #print query

        (list_databases,hits) = get_databases_from_solr_v2(request, query, sort=sortString, rows=rows, start=start)

        list_databases = paginator_process_list(list_databases, hits, start)
        if start > hits and not force:
            return all_databases_user(request, 1, force=True)

    else:
        list_databases = []
        #list_databases = get_databases_from_solr(request, "*:*")

    ## Paginator ##

    myPaginator = Paginator(list_databases, rows)
    try:
        pager =  myPaginator.page(page)
    except PageNotAnInteger, e:
        pager =  myPaginator.page(1)
    ## End Paginator ##

    return render(request, template_name, {'request': request, 'export_all_answers': True, 'data_table': True,
                                           'list_databases': list_databases,
                                            'breadcrumb': True, 'collapseall': False,
                                            'geo': True,
                                            'page_obj': pager, "page_rows": rows,
                                            'alldatabases': True,
                                            'add_databases': True, "sort_params": sort_params, "page":page})

def qs_data_table(request, template_name='qs_data_table.html'):
    db_type = int(request.POST.get("db_type"))
    qset_post = request.POST.getlist("qsets[]")

    # generate a mumbo jumbo digest for this combination of parameters, to be used as key for caching purposes
    string_to_be_hashed = "dbtype"+str(db_type)

    for post in qset_post:
        string_to_be_hashed+="qs"+post

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

        (titles, answers) = creatematrixqsets(db_type, fingerprints, qset)

        cache.set(hashed, (titles, answers), 720) # 12 hours of cache

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


# TODO: move to another place, maybe API?
def get_api_info(fingerprint_id):
    """This is an auxiliar method to get the API Info
    """
    result = {}


    results = FingerprintAPI.objects.filter(fingerprintID=fingerprint_id)
    result = {}
    for r in results:
        result[r.field] = r.value
    return result

def handle_uploaded_file(f):
    #print "abspath"

    with open(os.path.join(os.path.abspath(settings.PROJECT_DIR_ROOT + 'emif/static/upload_images/'), f.name),
              'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def feedback(request, template_name='feedback.html'):

    if request.method == 'POST':  # If the form has been submitted...
        form = ContactForm(request.POST)
        if form.is_valid():  # All validation rules pass

            subject = request.POST.get('topic', '').encode('ascii', 'ignore')
            name = request.POST.get('name', '').encode('ascii', 'ignore')
            message = request.POST.get('message', '').encode('ascii', 'ignore')
            from_email = request.POST.get('email', '')

            emails_to_feedback = []
            for k, v in settings.ADMINS:
                emails_to_feedback.append(v)

            try:
                message_admin = "Name: " + str(name) + "\nEmail: " + from_email + "\n\nMessage:\n" + str(message)
                message = "Dear " + name + ",\n\nThank you for giving us your feedback.\n\nYour message will be analyzed by EMIF Catalogue team.\n\nMessage sent:\n" + str(message) + "\n\nSincerely,\nEMIF Catalogue"
                # Send email to admins
                send_custom_mail(subject, message_admin, settings.DEFAULT_FROM_EMAIL, emails_to_feedback)
                # Send email to user with the copy of feedback message
                send_custom_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [from_email])

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return feedback_thankyou(request)

    else:
        form = ContactForm()  # An unbound form
    return render(request, template_name, {'form': form, 'request': request, 'breadcrumb': True})

        # return render_to_response('feedback.html', {'form': ContactForm()},
        #     RequestContext(request))


def feedback_thankyou(request, template_name='feedback_thankyou.html'):
    return render(request, template_name, {'request': request, 'breadcrumb': True})

def create_auth_token(request, page=1, templateName='api-key.html', force=False):
    """
    Method to create token to authenticate when calls REST API
    """
    rows = define_rows(request)
    if request.POST and not force:
        page = request.POST["page"]

    if page == None:
        page = 1

    user = request.user
    if not Token.objects.filter(user=user).exists():
        token = Token.objects.create(user=request.user)
    else:
        token = Token.objects.get(user=user)

    _filter = "user_t:" + '"' + user.username + '"'

    (sortString, filterString, sort_params, range) = paginator_process_params(request.POST, page, rows)

    sort_params["base_filter"] = _filter;

    if len(filterString) > 0:
        _filter += " AND " + filterString

    (list_databases,hits) = get_databases_from_solr_v2(request, _filter, sort=sortString, rows=rows, start=range)
    if range > hits and force < 2:
        return create_auth_token(request, page=1, force=True)

    list_databases = paginator_process_list(list_databases, hits, range)

    myPaginator = Paginator(list_databases, rows)
    try:
        pager =  myPaginator.page(page)
    except PageNotAnInteger, e:
        pager =  myPaginator.page(1)
    ## End Paginator ##

    return render_to_response(templateName, {'list_databases': list_databases, 'token': token, 'user': user,
                              'request': request, 'breadcrumb': True, 'page_obj': pager, 'page_rows': rows, "sort_params": sort_params, "page":page}, RequestContext(request))

def invitedb(request, db_id, template_name="sharedb.html"):

    email = request.POST.get('email', '')
    message_write = request.POST.get('message', '')
    if (email == None or email==''):
        return HttpResponse('Invalid email address.')

    fingerprint = None
    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=db_id)
    except Fingerprint.DoesNotExist:
        print "Fingerprint with id "+db_id+" does not exist."
        return HttpResponse("Service Unavailable")

    subject = "EMIF Catalogue: A new database is trying to be shared with you."
    link_invite = settings.BASE_URL + "accounts/signup/"

    #message = """Dear %s,\n\n
    #        \n
    #        %s is sharing a new database with you on Emif Catalogue.
    #        First you must register on the EMIF Catalogue. Please follow the link below: \n\n
    #        %s
    #        \n\nSincerely,\nEMIF Catalogue
    #""" % (email,request.user.get_full_name(), link_invite)

    message = """%s\n
            To have full access to this fingerprint, please register in the EMIF Catalogue following the link below: \n\n
            %s
            \n\nSincerely,\nEMIF Catalogue
    """ % (message_write, link_invite)


    send_custom_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

    pend = None

    try:
        pend = InvitePending.objects.get(fingerprint=fingerprint, email=email)
        return HttpResponse("User already has been invited to join catalogue")
    except:
        pass

    pend = InvitePending(fingerprint=fingerprint, email=email)
    pend.save()

    return HttpResponse("An invitation has been sent to the user email so he can signup on catalogue")

def sharedb(request, db_id, template_name="sharedb.html"):
    if not request.method == 'POST':
        return HttpResponse("Service Unavailable")

    # Verify if it is a valid email
    email = request.POST.get('email', '')
    message = request.POST.get('message', '')
    if (email == None or email==''):
        return HttpResponse('Invalid email address.')

    # Verify if it is a valid user name
    username_to_share = None
    try:
        username_to_share = User.objects.get(email__exact=email)
    except Exception, e:
        pass

    if not username_to_share:
        return HttpResponse("Invalid email address.")


    # Verify if it is a valid database
    if (db_id == None or db_id==''):
        return HttpResponse('Service Unavailable')

    fingerprint = None
    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=db_id)
    except Fingerprint.DoesNotExist:
        return HttpResponse("Service Unavailable")

    subject = "EMIF Catalogue: A new database has been shared with you."
    name = username_to_share.get_full_name()
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    # import pdb
    # pdb.set_trace()
    __objs = SharePending.objects.filter(db_id=db_id, pending=True, user=username_to_share)
    if (len(__objs)>0):
        share_pending = __objs[0]
        success_msg = "You have already invited this user to start collaborating in your database. The invitation email was re-sent to his address."
    else:
        share_pending = SharePending()
        share_pending.user = username_to_share
        share_pending.db_id = db_id
        share_pending.activation_code = generate_hash()
        share_pending.pending = True
        share_pending.user_invite = request.user
        share_pending.save()
        success_msg = "An invitation has been sent to your co-worker start collaboration in your database. If you need further assistance, please do not hesitate to contact EMIF Catalogue team."

    link_activation = settings.BASE_URL + "share/activation/"+share_pending.activation_code

    new_notification = Notification(destiny=username_to_share ,origin=request.user, 
        notification=(findName(fingerprint)+" has been shared with you, please click here to activate it."), type=Notification.SYSTEM, href=link_activation)

    new_notification.save()

    emails_to_feedback = []
    #print settings.ADMINS
    for k, v in settings.ADMINS:
        emails_to_feedback.append(v)

    try:

        message = """%s

            Now you're able to edit and manage the database. \n\n
            To activate the database in your account, please open this link:
            %s
            \n\nSincerely,\nEMIF Catalogue
        """ % (message,link_activation)
        # Send email to admins
        #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, emails_to_feedback)
        # Send email to user with the copy of feedback message
        send_custom_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [from_email])

    except BadHeaderError:
        return HttpResponse('Service Unavailable')

    return HttpResponse(success_msg)

def sharedb_activation(request, activation_code, template_name="sharedb_invited.html"):

    return activate_user(activation_code, request.user, context = request)

# Documentation
def docs_api(request, template_name='docs/api.html'):
    return render(request, template_name, {'request': request, 'breadcrumb': True})

def more_like_that(request, doc_id, mlt_query=None, page=1, template_name='more_like_this.html', force=False):
    #first lets clean the query session log
    if 'query' in request.session:
        del request.session['query']

    if 'isAdvanced' in request.session:
        del request.session['isAdvanced']

    if 'query_id' in request.session:
        del request.session['query_id']
    if 'query_type' in request.session:
        del request.session['query_type']

    database_name = ""

    if mlt_query == None:
        (_filter, database_name) = get_query_from_more_like_this(doc_id)
    else:
        _filter = mlt_query

    if not _filter:
        return render(request, template_name, {'request': request,
                                       'num_results': 0, 'page_obj': None,
                                       'page_rows': 0,'breadcrumb': True,
                                       "breadcrumb_text": "More Like - "+database_name,
                                       'database_name': database_name, 'isAdvanced': False,
                                       'hide_add': True, 'more_like_this': True,
                                       "sort_params": None, "page":None})

    rows = define_rows(request)
    if request.POST and not force:
        page = request.POST["page"]

    if page == None:
        page = 1

    (sortString, filterString, sort_params, range) = paginator_process_params(request.POST, page, rows, default_mode={"score":"desc"})
    sort_params["base_filter"] = _filter;

    #print filterString

    if len(filterString) > 0:
        _filter += " AND " + filterString

    #print _filter

    def fn(res, lst):
        m = {}
        for r in res:
            if "id" in r and "score" in r:
                m[r["id"]] = r

        for d in lst:
            if d.id in m:
                d.score = str(round(float( m[d.id]["score"]), 3) )
        return lst

    (list_databases,hits) = get_databases_from_solr_v2(request, _filter, sort=sortString, rows=rows, start=range, fl="*, score", post_process=fn)
    if range > hits and force < 2:
        return databases(request, page=1, force=True)

    #print "Range: "+str(range)
    #print "hits: "+str(hits)
    #print "len: "+str(len(list_databases))

    list_databases = paginator_process_list(list_databases, hits, range)

    #print "len: "+str(len(list_databases))
    ## Paginator ##
    myPaginator = Paginator(list_databases, rows)
    try:
        pager =  myPaginator.page(page)
    except PageNotAnInteger, e:
        pager =  myPaginator.page(page)
    ## End Paginator ##    #print list_databases

    return render(request, template_name, {'request': request,
                                           'num_results': hits, 'page_obj': pager,
                                           'page_rows': rows,'breadcrumb': True,
                                           "breadcrumb_text": "More Like - "+database_name,
                                           'database_name': database_name, 'isAdvanced': False,
                                           'hide_add': True, 'more_like_this': True,
                                           "sort_params": sort_params, "page":page})

def clean_str_exp(s):
    return s.replace("\n", "|").replace(";", ",").replace("\t", "    ").replace("\r","").replace("^M","")

def save_answers_to_csv(list_databases, filename):
    """
    Method to export answers of a given database to a csv file
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="EMIF_Catalogue_%s_%s.csv"' % (filename, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    if list_databases:
        writer = csv.writer(response, delimiter = '\t')
        writer.writerow(['DB_ID', 'DB_name', 'Questionset', 'Question', 'QuestionNumber', 'Answer', 'Date Last Modification'])
        for t in list_databases:
            id = t.id

            returned = createqsets(id, clean=False, changeSearch=True, noprocessing=False)

            qsets, name, db_owners, fingerprint_ttype  = returned

            qsets = attachPermissions(id, qsets)

            for (k, qs), permissions in qsets:
                if permissions.visibility == 0 and permissions.allow_exporting == True:
                    writeGroup(id, k, qs, writer, name, t)

        writer.writerow([id, name, "System", "Date", "99.0", t.date])
        writer.writerow([id, name, "System", "Date Modification", "99.1", t.date_modification])
        writer.writerow([id, name, "System", "Type", "99.2", t.type_name])
        writer.writerow([id, name, "System", "Type Identifier", "99.3", t.ttype])
    return response

def attachPermissions(fingerprint_id, qsets):
    zipper = qsets
    zipee = []

    for q, v in zipper.ordered_items():
        qpermissions = getPermissions(fingerprint_id, QuestionSet.objects.get(id=v.qsid))
        zipee.append(qpermissions)

    merged = zip(zipper.ordered_items(), zipee)

    return merged

def writeGroup(id, k, qs, writer, name, t):
    if (qs!=None and qs.list_ordered_tags!= None):
        list_aux = sorted(qs.list_ordered_tags)

        for q in list_aux:
            _answer = clean_str_exp(str(q.value))
            if (_answer == "" and q.ttype=='comment'):
                _answer = "-"
            writer.writerow([id, name, k.replace('h1. ', ''), clean_str_exp(str(q.tag)), str(q.number), _answer, q.lastChange])

def export_datatable(request):

    db_type = int(request.POST.get("db_type"))
    qset_post = request.POST.getlist("qsets[]")

    # generate a mumbo jumbo digest for this combination of parameters, to be used as key for caching purposes
    string_to_be_hashed = "dbtype"+str(db_type)

    for post in qset_post:
        string_to_be_hashed+="qs"+post

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

        (titles, answers) = creatematrixqsets(db_type, fingerprints, qset)

        cache.set(hashed, (titles, answers), 720) # 12 hours of cache

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


def export_all_answers(request):
    """
    Method to export all databases answers to a csv file
    """

    list_databases = get_databases_from_solr(request, "*:*")
    return save_answers_to_csv(list_databases, "DBs")


def export_my_answers(request):
    """
    Method to export my databases answers to a csv file
    """

    user = request.user
    list_databases = get_databases_from_solr(request, "user_t:" + '"' + user.username + '"')

    return save_answers_to_csv(list_databases, "MyDBs")

def export_search_answers(request):
    """
    Method to export search databases answers to a csv file
    """

    user = request.user

    query = None
    isadvanced = request.session.get('isAdvanced')
    value = request.session.get('query')

    if(isadvanced):
        query = value
    else:
        query = "text_t:"+str(value)

    list_databases = get_databases_from_solr(request, query)

    return save_answers_to_csv(list_databases, "search_results")


def export_bd_answers(request, runcode):
    """
    Method to export answers of a specific database to a csv file
    :param request:
    :param runcode:
    """

    list_databases = get_databases_from_solr(request, "id:" + runcode)
    return save_answers_to_csv(list_databases, 'MyDB')

# def save_slug(slugName, desc, question):
#     slugsAux = Slugs()
#     slugsAux.slug1 = slugName
#     slugsAux.description = desc
#     slugsAux.question = question
#     slugsAux.save()


def save_slug(slugName, desc):
    slugsAux = Slugs()
    slugsAux.slug1 = slugName
    slugsAux.description = desc
    slugsAux.save()

# Redirect user after login. Rules:
# - settings value should be represented by "REDIRECT_" plus the profile.name in uppercase
# and with out spaces. Ex: REDIRECT_DATACUSTODIAN - for profile.name="Data Custodian"
@login_required
def wherenext(request):
    try:
        emifprofile = request.user.get_profile()
        if emifprofile.profiles.count():
            for profile in emifprofile.profiles.all():
                redirect = getattr(settings, "REDIRECT_" + profile.name.upper().strip().replace(" ", ""),
                    'emif.views.all_databases_user')
                return HttpResponseRedirect(reverse(redirect))

        interests = emifprofile.interests.all()
        if interests:
            return HttpResponseRedirect(reverse('emif.views.all_databases_user'))
    except:
        logging.warn("User has no emifprofile nor interests")
        return HttpResponseRedirect(reverse('emif.views.all_databases'))
