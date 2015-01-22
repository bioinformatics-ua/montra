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
import hashlib

from django.shortcuts import render

from django.core import serializers
from django.conf import settings
from django.http import *
from django.http import Http404
from django.utils import simplejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from questionnaire.models import Questionnaire
from questionnaire.parsers import *
from questionnaire.views import *
from questionnaire.models import *
from searchengine.search_indexes import CoreEngine
from searchengine.models import Slugs
import searchengine.search_indexes
from searchengine.search_indexes import index_answeres_from_qvalues
from searchengine.search_indexes import convert_text_to_slug

from fingerprint.models import Database, Fingerprint

from emif.models import QueryLog, AdvancedQuery, AdvancedQueryAnswer
from emif.utils import convert_date, convert_qvalues_to_query, convert_query_from_boolean_widget, escapeSolrArg

from fingerprint.services import define_rows, merge_highlight_results

from rest_framework.authtoken.models import Token

from fingerprint.tasks import anotateshowonresults

from accounts.models import EmifProfile, RestrictedUserDbs, RestrictedGroup

from django.utils import timezone

from constance import config

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


def results_fulltext(request, page=1, full_text=True,template_name='results.html', isAdvanced=False, query_reference=None, advparams=None):
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

    return results_fulltext_aux(request, query, page, template_name, isAdvanced=isAdvanced, query_reference=query_reference, advparams=advparams)


def results_fulltext_aux(request, query, page=1, template_name='results.html', isAdvanced=False, force=False, query_reference=None, advparams=None):

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

    try:
        hlfl = ",".join(advparams)
    except:
        hlfl = None

    if isAdvanced:
        (list_databases, hits, hi) = get_databases_from_solr_with_highlight(request, query_filtered, sort=sortString, rows=rows, start=range, hlfl=hlfl)
    else:
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
            (query, advparams) = convert_query_from_boolean_widget(qexpression, qid)
            #print "Query: " + query


            request.session['query'] = query
            request.session['advparams'] = advparams

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

                this_query = AdvancedQuery(user=this_user,name=("Query on "+timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
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



            return results_fulltext_aux(request, query, isAdvanced=True, query_reference=this_query, advparams=advparams)



    query = ""
    advparams=None
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
        advparams=request.session.get('advparams', None)

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
            return results_fulltext(request, page, full_text=True, isAdvanced=request.session['isAdvanced'], query_reference=simple_query, advparams=advparams)
    except:
        raise
    #print "Printing the qexpression"
    #print request.POST['qexpression']
    return results_fulltext(request, page, full_text=False, isAdvanced=request.session['isAdvanced'], query_reference=simple_query, advparams=advparams)


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

            try:
                database_aux.percentage = r['percentage_d']
            except KeyError:
                pass

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

def restriction(user):
    dbs = RestrictedUserDbs.objects.filter(user=user)
    rest = None
    i = 0

    def add_condition(i, rest, hash):

        if rest == None:
            rest = " AND (id:"+hash
        else:
            rest += " OR id:"+hash

        i += 1

        return (i, rest)

    # The main principle is avoid iterations, since usually this number will be very restricted in comparison with the real value
    for db in dbs:
        (i, rest) = add_condition(i, rest, db.fingerprint.fingerprint_hash)

    dbs = RestrictedGroup.hashes(user)

    for hash in dbs:
        (i, rest) = add_condition(i, rest, hash)

    if i>0:
        rest += ")"

    return rest

def get_databases_from_solr_v2(request, query="*:*", sort="", rows=100, start=0, fl='',post_process=None):
    try:
        eprofile = EmifProfile.objects.get(user=request.user)
    except EmifProfile.DoesNotExist:
        print "-- ERROR: Couldn't get emif profile for user"
    c = CoreEngine()

    if eprofile.restricted == True:
        query += restriction(request.user)

    results = c.search_fingerprint(query, sort=sort, rows=rows, start=start, fl=fl)

    list_databases = get_databases_process_results(results)

    if post_process:
        list_databases = post_process(results, list_databases)

    return (list_databases, results.hits)

def get_query_from_more_like_this(request, doc_id, type, maxx=100):
    try:
        eprofile = EmifProfile.objects.get(user=request.user)
    except EmifProfile.DoesNotExist:
        print "-- ERROR: Couldn't get emif profile for user"
    if eprofile.restricted == True:
        query = restriction(request.user)

    c = CoreEngine()
    #results = c.search_fingerprint(query, sort=sort, rows=rows, start=start)
    results = c.more_like_this(doc_id, type, maxx=maxx)


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
    results = c.search_fingerprint("id:"+doc_id , start=0, rows=1, fl="database_name_t")
    for r in results:
        if "database_name_t" in r:
            database_name = r["database_name_t"]

    return (queryString, database_name)

def get_databases_from_solr_with_highlight(request, query="*:*", sort="", rows=100, start=0, hlfl="*"):
    try:
        eprofile = EmifProfile.objects.get(user=request.user)
    except EmifProfile.DoesNotExist:
        print "-- ERROR: Couldn't get emif profile for user"
    if eprofile.restricted == True:
        query += restriction(request.user)

    c = CoreEngine()

    results = c.search_highlight(query, sort=sort, rows=rows, start=start, hlfl=hlfl)

    list_databases = get_databases_process_results(results)

    return (list_databases,results.hits, results.highlighting)

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
        del request.session['advparams']
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

# Documentation
def docs_api(request, template_name='docs/api.html'):
    return render(request, template_name, {'request': request, 'breadcrumb': True})

def more_like_that(request, doc_id, mlt_query=None, page=1, template_name='more_like_this.html', force=False):

    if not config.more_like_this:
        raise Http404
    #first lets clean the query session log
    if 'query' in request.session:
        del request.session['query']

    if 'advparams' in request.session:
        del request.session['advparams']

    if 'isAdvanced' in request.session:
        del request.session['isAdvanced']

    if 'query_id' in request.session:
        del request.session['query_id']
    if 'query_type' in request.session:
        del request.session['query_type']

    database_name = ""

    fingerprint = Fingerprint.objects.get(fingerprint_hash=doc_id)

    if mlt_query == None:
        (_filter, database_name) = get_query_from_more_like_this(request, doc_id, fingerprint.questionnaire.slug)
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

def databases(request, page=1, template_name='results.html', force=False):

     #first lets clean the query session log
    if 'query' in request.session:
        del request.session['query']
    if 'advparams' in request.session:
        del request.session['advparams']
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

def create_auth_token(request, page=1, templateName='api-key.html', force=False):
    """
    Method to create token to authenticate when calls REST API
    """

    if not config.extra_information:
        raise Http404

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
