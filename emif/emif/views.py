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
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.urlresolvers import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from emif.utils import QuestionGroup

from questionnaire.models import *
from questionnaire.parsers import *
from questionnaire.views import *
from questionnaire.models import *
from searchengine.search_indexes import CoreEngine
from searchengine.models import Slugs
import searchengine.search_indexes
from searchengine.search_indexes import index_answeres_from_qvalues
from emif.utils import *
from emif.models import *

from django.core.mail import send_mail, BadHeaderError

import logging
import re
import md5
import random

import os
import os.path


def list_questions():
    print "list_questions"
    objs = Questionnaire.objects.all()
    results = {}
    for q in objs:
        results[q.id] = q.name
    print results
    return results


def index(request, template_name='index.html'):
    return render(request, template_name, {'request': request})


def about(request, template_name='about.html'):
    return render(request, template_name, {'request': request})


def quick_search(request, template_name='quick_search.html'):
    return render(request, template_name, {'request': request})


def results_db(request, template_name='results.html'):
    user = request.user
    su = Subject.objects.filter(user=user)
    databases = RunInfoHistory.objects.filter(subject=su)

    class Database:
        id = ''
        name = ''
        date = ''

    class Results:
        num_results = 0
        list_results = []

    list_databases = []
    for database in databases:
        database_aux = Database()
        database_aux.id = database.runid
        database_aux.date = database.completed
        answers = Answer.objects.filter(runid=database.runid)
        text = clean_value(str(answers[1].answer))
        info = text[:75] + (text[75:] and '..')
        database_aux.name = info
        list_databases.append(database_aux)

    list_results = Results()
    list_results.num_results = len(list_databases)
    list_results.list_results = list_databases

    return render(request, template_name, {'request': request,
                                           'list_results': list_results})


def results_comp(request, template_name='results_comp.html'):
    list_fingerprint_to_compare = []
    print request.POST
    if request.POST:
        for k, v in request.POST.items():
            print k
            print v
            if k.startswith("chk_") and v == "on":
                arr = k.split("_")

                list_fingerprint_to_compare.append(arr[1])

    print "list_fingerprint_to_compare" + str(list_fingerprint_to_compare)

    class Results:
        num_results = 0
        list_results = []

    class DatabaseFields:
        id = ''
        name = ''
        date = ''
        fields = None

    list_qsets = []
    for db_id in list_fingerprint_to_compare:
        qsets, name = createqsets(db_id)
        list_qsets.append((name, qsets))
    first_name = None
    if len(list_qsets) > 0:
        (first_name, discard) = list_qsets[0]

    print "list_qsets: " + str(list_qsets)
    return render(request, template_name, {'request': request,
                                           'results': list_qsets, 'database_to_compare': first_name})


def results_fulltext(request, page=1, template_name='results.html'):
    query = ""
    in_post = True
    try:
        query = request.POST['query']
        request.session['query'] = query
    except:
        in_post = False
        #raise

    if not in_post:
        query = request.session.get('query', "")

    return results_fulltext_aux(request, "text_t:" + query, page, template_name)


def results_fulltext_aux(request, query, page=1, template_name='results.html'):
    rows = 5
    if query == "":
        return render(request, "results.html", {'request': request,
                                                'list_results': [], 'page_obj': None})

    class Results:
        num_results = 0
        list_results = []
        paginator = None


    c = CoreEngine()
    #results = c.search_fingerprint("text_t:"+query,str(((int(page)-1)*rows)))
    results = c.search_fingerprint(query, str(0))
    #results = c.search_fingerprint("database_name_t:"+query)
    #print "Solr"
    #print results
    list_databases = []
    if len(results) == 0:
        return render(request, "results.html", {'request': request,
                                                'list_results': [], 'page_obj': None})
    for r in results:
        try:
            database_aux = Database()
            #print r['id']
            #print r['created_t']
            #print r['database_name_t']

            if (not r.has_key('database_name_t')):
                database_aux.name = '(Unnamed)'
            else:
                database_aux.name = r['database_name_t']

            if (not r.has_key('location_t')):
                database_aux.location = ''
            else:
                database_aux.location = r['location_t']

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
            if (not r.has_key('upload-image_t')):
                database_aux.logo = 'nopic.gif'
            else:
                database_aux.logo = r['upload-image_t']
            database_aux.id = r['id']
            database_aux.date = convert_date(r['created_t'])
            #database_aux.name = r['database_name_t']
            #database_aux.location = r['location_t']
            #database_aux.institution = r['institution_name_t']
            #database_aux.email_contact = r['contact_administrative_t']
            #database_aux.number_patients = r['number_active_patients_jan2012_t']
            list_databases.append(database_aux)
        except:
            raise

    pp = Paginator(list_databases, rows)
    list_results = Results()
    list_results.num_results = results.hits
    list_results.list_results = pp.page(page)
    list_results.paginator = pp
    query_old = request.session.get('query', "")
    return render(request, template_name, {'request': request,
                                           'list_results': list_results, 'page_obj': pp.page(page),
                                           'search_old': query_old})


def store_query(user_request, query_executed):
    print user_request.user.is_authenticated()
    print "Store Query2"
    # Verify if the query already exists in that user 
    user_aux = None
    if user_request.user.is_authenticated():

        user_aux = user_request.user

        results_tmp = QueryLog.objects.filter(query=query_executed, user=user_aux)

    else:
        results_tmp = QueryLog.objects.filter(query=query_executed, user__isnull=True)
    query = None
    print results_tmp
    print "lol"
    if (results_tmp.exists()):
        print "exists"
        # If the user exists, then update the Query 
        query = results_tmp[0]
    else:
        # Create a query 
        query = QueryLog()
        if user_request.user.is_authenticated():
            query.user = user_request.user
        else:
            query.user = None
        query.query = query_executed
        print "dmn"
    if query != None:
        if user_request.user.is_authenticated():
            query.user = user_request.user
        else:
            query.user = None
        query.query = query_executed
        query.save()
    print "executed"


def results_diff(request, page=1, template_name='results_diff.html'):
    query = ""
    in_post = True
    try:
        query = request.POST['query']
        request.session['query'] = query
    except:
        in_post = False
        #raise

    if not in_post:
        query = request.session.get('query', "")

    if query == "":
        return render(request, "results.html", {'request': request,
                                                'list_results': [], 'page_obj': None})
    store_query(request, query)
    try:
        # Store query by the user

        search_full = request.POST['search_full']

        if search_full == "search_full":
            return results_fulltext(request, page)
    except:

        return results_fulltext(request, page)


    class Results:
        num_results = 0
        list_results = []
        d1 = None
        d2 = None
        d3 = None


    class DatabaseFields:
        id = ''
        name = ''
        date = ''
        fields = None


    c = CoreEngine()
    results = c.search_fingerprint("text_t:" + query)
    #results = c.search_fingerprint("database_name_t:"+query)
    print "Solr"
    print results
    list_databases = []

    for r in results:
        try:
            database_aux = Database()
            print r['id']
            print r['created_t']
            print r['database_name_t']
            database_aux.id = r['id']
            database_aux.date = convert_date(r['created_t'])

            database_aux.name = r['database_name_t']
            list_databases.append(database_aux)
            if (len(list_databases) == 3):
                break
        except:
            pass

    c = CoreEngine()
    list_databases_final = []
    list_results = Results()

    for db in list_databases:

        results = c.search_fingerprint('id:' + db.id)

        class Tag:
            tag = ''
            value = ''

        list_values = []
        blacklist = ['created_t', 'type_t', '_version_']
        name = "Not defined"
        for result in results:
            for k in result:
                if k in blacklist:
                    continue
                t = Tag()
                results = Slugs.objects.filter(slug1=k)
                if len(results) > 0:
                    text = results[0].description
                else:
                    text = k
                info = text[:75] + (text[75:] and '..')

                t.tag = info

                value = clean_value(str(result[k]))
                value = value[:75] + (value[75:] and '..')
                t.value = value
                if k == "database_name_t":
                    name = t.value
                list_values.append(t)
        db.fields = list_values
        list_databases_final.append(db)

    list_results.d1 = list_databases_final[0]
    list_results.d2 = list_databases_final[1]
    list_results.d3 = list_databases_final[2]

    list_results.num_results = len(list_databases)

    return render(request, template_name, {'request': request,
                                           'results': list_results, 'search_old': query})


def geo(request, template_name='geo.html'):
    query = None
    try:
        query = request.session['query']
        query = 'text_t:' + query
    except:
        pass
    if query == None:
        query = "*:*"
    print "query@" + query
    list_databases = get_databases_from_solr(request, query)
    list_locations = []
    for database in list_databases:
        list_locations.append(database.location)
    return render(request, template_name, {'request': request,
                                           'list_cities': list_locations})


<<<<<<< HEAD
def statistics(request, questionnaire_id, question_set, template_name='statistics.html'):
=======


def statistics(request, template_name='statistics.html'):
    from emif.statistics import Statistic
>>>>>>> 427e412cd4ec589ed09cbb8ba4eb577de00a6e03

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


def advanced_search(request, questionnaire_id, question_set):
    #return render(request, template_name, {'request': request})
    print questionnaire_id

    #return show_full_questionnaire(request, questionnaire_id)
    return show_fingerprint_page_read_only(request, questionnaire_id, question_set)


def database_add(request, questionnaire_id, sortid):
    response = show_fingerprint_page_read_only(request, questionnaire_id, sortid,
                                               template_name='database_add.html')
    response['breadcrumb'] = True
    return response


class RequestMonkeyPatch(object):
    POST = {}
    method = POST

    def __init__(self):
        self.POST = {}

    def get_post(self):
        return self.POST


def database_edit(request, fingerprint_id, questionnaire_id, template_name="database_edit.html"):
    #return render(request, template_name, {'request': request})
    #print questionnaire_id
    #logging.debug("Debugger")
    #return show_full_questionnaire(request, questionnaire_id, 
    #    reverse_name='questionaries_with_sets')
    #return show_full_questionnaire(request, questionnaire_id)

    c = CoreEngine()
    results = c.search_fingerprint("id:" + fingerprint_id)
    items = None
    for r in results:
        items = r
        break
    fingerprint_id = r['id']
    qsobjs = QuestionSet.objects.filter(questionnaire=questionnaire_id)
    questionnaire = qsobjs[0].questionnaire
    sortid = None
    try:
        question_set = request.POST['active_qs']
        sortid = request.POST['active_qs_sortid']
    except:
        pass

    if request.POST:
        return check_database_add_conditions(request, questionnaire_id, sortid, template_name='database_edit.html')
        # to confirm that we have the correct answers

    expected = []
    for qset in qsobjs:
        questions = qset.questions()
        for q in questions:
            expected.append(q)

    extra = {} # question_object => { "ANSWER" : "123", ... }

    # this will ensure that each question will be processed, even if we did not receive
    # any fields for it. Also works to ensure the user doesn't add extra fields in
    #for x in expected:
    #    items.append( (u'question_%s_Trigger953' % x.number, None) )

    # generate the answer_dict for each question, and place in extra
    request2 = RequestMonkeyPatch()

    for item in items:
        #wprint item
        key = item

        value = items[key]
        results = Slugs.objects.filter(slug1=key)

        if results == None or len(results) == 0:
            continue
        question = results[0].question

        #if key.startswith('question_'):
        answer = str(question.number)
        #question = get_question(answer[1], questionnaire)
        #if not question:
        #    logging.warn("Unknown question when processing: %s" % answer[1])
        #    continue
        extra[question] = ans = extra.get(question, {})
        if "[" in value:
            value = value.lower().replace("]", "").replace("[", "")
        request2.get_post()['question_%s' % question.number] = value
        ans['ANSWER'] = value

        extra[question] = ans

    print extra
    errors = {}

    try:
        q_id = questionnaire_id
        qs_id = 1
        qs_list = QuestionSet.objects.filter(questionnaire=q_id)
        #print "Q_id: " + q_id
        #print "Qs_id: " + qs_id
        #print "QS List: " + str(qs_list)

        question_set = qs_list[int(qs_id)]
        #questions = Question.objects.filter(questionset=qs_id)

        questions = question_set.questions()
        #print "Questions: " + str(questions)
        #print "QuestionSet: " + str(question_set)

        questions_list = {}
        for qset_aux in qs_list:
            #questions_aux = Question.objects.filter(questionset=qset_aux)
            questions_list[qset_aux.id] = qset_aux.questions()
            #print "here"

        qlist = []
        jsinclude = []      # js files to include
        cssinclude = []     # css files to include
        jstriggers = []
        qvalues = {}

        qlist_general = []

        for k in qs_list:
            qlist = []
            qs_aux = None
            for question in questions_list[k.id]:

                qs_aux = question.questionset
                #print "Question: " + str(question)
                Type = question.get_type()
                _qnum, _qalpha = split_numal(question.number)

                qdict = {
                    'template': 'questionnaire/%s.html' % (Type),
                    'qnum': _qnum,
                    'qalpha': _qalpha,
                    'qtype': Type,
                    'qnum_class': (_qnum % 2 == 0) and " qeven" or " qodd",
                    'qalpha_class': _qalpha and (ord(_qalpha[-1]) % 2 \
                                                     and ' alodd' or ' aleven') or '',
                }

                # add javascript dependency checks
                cd = question.getcheckdict()
                depon = cd.get('requiredif', None) or cd.get('dependent', None)
                if depon:
                    # extra args to BooleanParser are not required for toString
                    parser = BooleanParser(dep_check)
                    qdict['checkstring'] = ' checks="%s"' % parser.toString(depon)
                    jstriggers.append('qc_%s' % question.number)
                if 'default' in cd and not question.number in cookiedict:
                    qvalues[question.number] = cd['default']
                if Type in QuestionProcessors:

                    qdict.update(QuestionProcessors[Type](request2, question))
                    if 'jsinclude' in qdict:
                        if qdict['jsinclude'] not in jsinclude:
                            jsinclude.extend(qdict['jsinclude'])
                    if 'cssinclude' in qdict:
                        if qdict['cssinclude'] not in cssinclude:
                            cssinclude.extend(qdict['jsinclude'])
                    if 'jstriggers' in qdict:
                        jstriggers.extend(qdict['jstriggers'])
                        #if 'qvalue' in qdict and not question.number in cookiedict:
                        #    qvalues[question.number] = qdict['qvalue']

                qlist.append((question, qdict))
            if qs_aux == None:
                qs_aux = k
            qlist_general.append((qs_aux, qlist))
        if (question_set.sortid == 99 or request.POST):
            # Index on Solr
            try:
                index_answeres_from_qvalues(qlist_general, question_set.questionnaire, request.user.username,
                                            fingerprint_id)
            except:
                raise

        r = r2r(template_name, request,
                questionset=question_set,
                questionsets=question_set.questionnaire.questionsets,
                runinfo=None,
                errors=errors,
                qlist=qlist,
                progress=None,
                triggers=jstriggers,
                qvalues=qvalues,
                jsinclude=jsinclude,
                cssinclude=cssinclude,
                fingerprint_id=fingerprint_id,
                async_progress=None,
                async_url=None,
                qs_list=qs_list,
                questions_list=qlist_general,
        )
        r['Cache-Control'] = 'no-cache'
        r['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"
    except:
        raise
    return r


# Documentation 
def docs_api(request, template_name='docs/api.html'):
    return render(request, template_name, {'request': request})


class Database:
    id = ''
    name = ''
    date = ''


def get_databases_from_db(request):
    user = request.user
    su = Subject.objects.filter(user=user)
    databases = RunInfoHistory.objects.filter(subject=su)

    list_databases = []
    for database in databases:
        database_aux = Database()
        database_aux.id = database.runid
        database_aux.date = database.completed
        answers = Answer.objects.filter(runid=database.runid)
        text = clean_value(str(answers[1].answer))
        info = text[:75] + (text[75:] and '..')
        database_aux.name = info
        list_databases.append(database_aux)
    return list_databases


def get_databases_from_solr(request, query="*:*"):
    c = CoreEngine()
    results = c.search_fingerprint(query)
    print "Solr"
    print results
    list_databases = []
    questionnaires_ids = {}
    qqs = Questionnaire.objects.all()
    for q in qqs:
        lower_name = q.name.replace(" ", "").lower()
        questionnaires_ids[lower_name] = q.pk

    for r in results:
        try:
            database_aux = Database()
            #print r['id']
            #print r['created_t']
            #print r['database_name_t']
            database_aux.id = r['id']

            if (not r.has_key('created_t')):
                database_aux.date = ''
            else:

                try:
                    database_aux.date = convert_date(r['created_t'])
                except:
                    database_aux.date = ''

            if (not r.has_key('database_name_t')):
                database_aux.name = '(Unnamed)'
            else:
                database_aux.name = r['database_name_t']

            if (not r.has_key('location_t')):
                database_aux.location = ''
            else:
                database_aux.location = r['location_t']

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

            if (not r.has_key('upload-image_t')):
                database_aux.logo = 'nopic.gif'
            else:
                database_aux.logo = r['upload-image_t']

            database_aux.ttype = questionnaires_ids[r['type_t']]
            list_databases.append(database_aux)
        except:
            pass
            #raise
    return list_databases


def delete_fingerprint(request, id):
    user = request.user
    #su = Subject.objects.filter(user=user)

    #email = su[0].email

    c = CoreEngine()
    results = c.search_fingerprint('user_t:' + user.username)
    for result in results:
        if (id == result['id']):
            c.delete(id)
            break

    return databases(request)


def databases(request, template_name='databases.html'):
    # Get the list of databases for a specific user

    user = request.user
    #list_databases = get_databases_from_db(request)
    list_databases = get_databases_from_solr(request, "user_t:" + user.username)

    return render(request, template_name, {'request': request,
                                           'list_databases': list_databases, 'breadcrumb': True, 'collapseall': False})


def all_databases(request, template_name='alldatabases.html'):
    #list_databases = get_databases_from_db(request)
    list_databases = get_databases_from_solr(request, "*:*")

    return render(request, template_name, {'request': request,
                                           'list_databases': list_databases, 'breadcrumb': True, 'collapseall': False})


def createqsets(runcode, qsets=None):
    c = CoreEngine()
    results = c.search_fingerprint('id:' + runcode)

    if qsets == None:
        qsets = {}
    name = ""
    list_values = []
    blacklist = ['created_t', 'type_t', '_version_']
    name = "Not defined."

    for result in results:

        print result['type_t']
        # Get the slug of fingerprint type
        q_aux = Questionnaire.objects.filter(slug=result['type_t'])
        print q_aux

        list_qsets = QuestionSet.objects.filter(questionnaire=q_aux[0]).order_by('sortid')

        for qset in list_qsets:
            if (qset.sortid != 0 and qset.sortid != 99):
                question_group = QuestionGroup()
                list_questions = Question.objects.filter(questionset=qset).order_by('number')
                for question in list_questions:
                    t = Tag()
                    t.tag = question.text
                    t.value = ""
                    question_group.list_ordered_tags.append(t)

                qsets[qset.text] = question_group
        print list_qsets
        print "results"

        for k in result:
            if k in blacklist:
                continue
            t = Tag()
            aux_results = Slugs.objects.filter(slug1=k)
            qs = None
            question_group = None
            if len(aux_results) > 0:
                text = aux_results[0].description
                qs = aux_results[0].question.questionset.text

                if qsets.has_key(qs):
                    # Add the Tag to the QuestionGroup
                    question_group = qsets[qs]
                else:
                    question_group = QuestionGroup()
                    qsets[qs] = question_group
                    # Add a new QuestionGroup
            else:
                text = k
                #print qs
            #info = text[:75] + (text[75:] and '..')

            info = text
            t.tag = info
            if question_group != None and question_group.list_ordered_tags != None:
                try:
                    t = question_group.list_ordered_tags[question_group.list_ordered_tags.index(t)]
                except:
                    pass

            value = clean_value(str(result[k].encode('utf-8')))
            #value = value[:75] + (value[75:] and '..')

            t.value = value.replace("#", " ")
            if k == "database_name_t":
                name = t.value
            list_values.append(t)
            if question_group != None:
                #try:
                #    question_group.list_ordered_tags.remove(t)
                #except:
                #    pass
                #question_group.list_ordered_tags.append(t)
                try:
                    question_group.list_ordered_tags[question_group.list_ordered_tags.index(t)] = t
                except:
                    pass
                    #qsets[qs] = question_group
        break

    print "List of qsets " + str(qsets)
    #for qg in qsets:
    #    print qg
    #    for tt in qsets[qg].list_ordered_tags:
    #        try:
    #            print tt
    #        except:
    #            pass
    #    #print qsets[qg].list_ordered_tags
    return (qsets, name)


def fingerprint(request, runcode, qs, template_name='database_info.html'):
    qsets, name = createqsets(runcode)
    return render(request, template_name,
                  {'request': request, 'qsets': qsets,
                   'breadcrumb': True, 'breadcrumb_name': name, 'style': qs, 'collapseall': True})


def get_questionsets_list(runinfo):
    # Get questionnaire
    current = runinfo.questionset
    sets = current.questionnaire.questionsets()
    return sets


def show_full_questionnaire_ro(request, qs_id, runinfo, errors={},
                               reverse_name='questionaries_with_sets'):
    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """

    #r = assure_authenticated_or_redirect(request)

    #if r:
    #    return r
    questionnaire_id = runinfo
    qu = get_object_or_404(Questionnaire, id=questionnaire_id)

    #qs = qu.questionsets()
    qs = qu.questionsets()[0]
    user = request.user
    su = Subject.objects.filter(user=user)

    if su:
        su = su[0]
    else:
        su = Subject(user=user,
                     first_name=user.first_name,
                     last_name=user.last_name,
                     email=user.email,
                     state='active')
        su.save()

    qs = qs_id
    try:
        qsobj = QuestionSet.objects.filter(pk=qs)[0]
    except:
        pass

    questionnaire = qsobj.questionnaire
    questionset = qsobj

    expected = questionset.questions()

    items = request.POST.items()
    extra = {} # question_object => { "ANSWER" : "123", ... }

    # this will ensure that each question will be processed, even if we did not receive
    # any fields for it. Also works to ensure the user doesn't add extra fields in
    for x in expected:
        items.append((u'question_%s_Trigger953' % x.number, None))

    # generate the answer_dict for each question, and place in extra
    for item in items:
        key, value = item[0], item[1]
        if key.startswith('question_'):
            answer = key.split("_", 2)
            question = get_question(answer[1], questionnaire)
            if not question:
                logging.warn("Unknown question when processing: %s" % answer[1])
                continue
            extra[question] = ans = extra.get(question, {})
            if (len(answer) == 2):
                ans['ANSWER'] = value
            elif (len(answer) == 3):
                ans[answer[2]] = value
            else:
                logging.warn("Poorly formed form element name: %r" % answer)
                continue
            extra[question] = ans

    errors = {}
    for question, ans in extra.items():
        if not question_satisfies_checks(question, runinfo):
            continue
        if u"Trigger953" not in ans:
            logging.warn("User attempted to insert extra question (or it's a bug)")
            continue
        try:
            cd = question.getcheckdict()
            # requiredif is the new way
            depon = cd.get('requiredif', None) or cd.get('dependent', None)
            if depon:
                depparser = BooleanParser(dep_check, runinfo, extra)
                if not depparser.parse(depon):
                    # if check is not the same as answer, then we don't care
                    # about this question plus we should delete it from the DB
                    delete_answer(question, runinfo.subject, runinfo.runid)
                    if cd.get('store', False):
                        runinfo.set_cookie(question.number, None)
                    continue
            add_answer(runinfo, question, ans)
            if cd.get('store', False):
                runinfo.set_cookie(question.number, ans['ANSWER'])
        except AnswerException, e:
            errors[question.number] = e
        except Exception:
            logging.exception("Unexpected Exception")
            transaction.rollback()
            raise

    if len(errors) > 0:
        res = show_questionnaire(request, runinfo, errors=errors)
        return res

    next = questionset.next()

    if next is None: # we are finished
        return finish_questionnaire(runinfo, questionnaire)

    return redirect_to_qs(runinfo)


def show_full_questionnaire(request, runinfo, errors={},
                            reverse_name='questionaries_with_sets'):
    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """

    #r = assure_authenticated_or_redirect(request)

    #if r:
    #    return r
    questionnaire_id = runinfo
    qu = get_object_or_404(Questionnaire, id=questionnaire_id)

    #qs = qu.questionsets()
    qs = qu.questionsets()[0]
    user = request.user
    su = Subject.objects.filter(user=user)

    if su:
        su = su[0]
    else:
        su = Subject(user=user,
                     first_name=user.first_name,
                     last_name=user.last_name,
                     email=user.email,
                     state='active')
        su.save()

    hash = md5.new()
    hash.update("".join(map(lambda i: chr(random.randint(0, 255)), range(16))))
    hash.update(settings.SECRET_KEY)
    key = hash.hexdigest()
    run = RunInfo(subject=su, random=key, runid=key, questionset=qs)
    run.save()
    questionsets = run.questionset.questionnaire.questionsets()

    return HttpResponseRedirect(reverse(reverse_name,
                                        kwargs={'runcode': key}))


def redirect_to_qs(runinfo):
    "Redirect to the correct and current questionset URL for this RunInfo"

    # cache current questionset
    qs = runinfo.questionset

    # skip questionsets that don't pass
    if not questionset_satisfies_checks(runinfo.questionset, runinfo):

        next = runinfo.questionset.next()

        while next and not questionset_satisfies_checks(next, runinfo):
            next = next.next()

        runinfo.questionset = next
        runinfo.save()

        hasquestionset = bool(next)
    else:
        hasquestionset = True

    # empty ?
    if not hasquestionset:
        logging.warn('no questionset in questionnaire which passes the check')
        return finish_questionnaire(runinfo, qs.questionnaire)

    url = reverse("questionset_sets",
                  args=[runinfo.random, runinfo.questionset.sortid])

    print "redirect to url: " + url
    return HttpResponseRedirect(url)


@transaction.commit_on_success
def questionaries_with_sets(request, runcode=None, qs=None, template_name='database_edit.html'):
    print "questionaries_with_sets"
    print "RunCode: " + str(runcode)
    print "Qs: " + str(qs)
    # if runcode provided as query string, redirect to the proper page
    if not runcode:
        runcode = request.GET.get('runcode')
        print "RunCode inside: " + runcode
        if not runcode:
            return HttpResponseRedirect("/")
        else:

            __qs = int(qs) + 1
            __qs += 1
            print HttpResponseRedirect(reverse("questionaries_with_sets", args=[runcode, str(__qs)]))
            return HttpResponseRedirect(reverse("questionaries_with_sets", args=[runcode, str(__qs)]))

    runinfo = get_runinfo(runcode)
    print "Runinfo:" + str(runinfo)

    if not runinfo:
        transaction.commit()
        return HttpResponseRedirect('/')


    #qs = runinfo.questionset
    if request.method != "POST":
        if qs is not None:
            qs = get_object_or_404(QuestionSet, sortid=qs, questionnaire=runinfo.questionset.questionnaire)
            print "qs.sortid=" + str(qs.sortid)
            print "runinfor.qs.sortid" + str(runinfo.questionset.sortid)
            if runinfo.random.startswith('test:'):
                pass # ok for testing
            elif qs.sortid > runinfo.questionset.sortid:
                # you may jump back, but not forwards
                return redirect_to_qs(runinfo)
            runinfo.questionset = qs
            runinfo.save()
            transaction.commit()
            # no questionset id in URL, so redirect to the correct URL
        if qs is None:
            return redirect_to_qs(runinfo)
        return show_fingerprint_page(request, runinfo)

    # Get several questionsets
    print "RunInfo: " + str(runinfo)
    print "runcode: " + str(runcode)
    print "QS: " + str(qs)

    # -------------------------------------
    # --- Process POST with QuestionSet ---
    # -------------------------------------

    # if the submitted page is different to what runinfo says, update runinfo
    # XXX - do we really want this?
    qs = request.POST.get('questionset_id', None)
    try:
        qsobj = QuestionSet.objects.filter(pk=qs)[0]
        if qsobj.questionnaire == runinfo.questionset.questionnaire:
            if runinfo.questionset != qsobj:
                runinfo.questionset = qsobj
                runinfo.save()
    except:
        pass

    questionnaire = runinfo.questionset.questionnaire
    questionset = runinfo.questionset

    # to confirm that we have the correct answers
    expected = questionset.questions()

    items = request.POST.items()
    extra = {} # question_object => { "ANSWER" : "123", ... }

    # this will ensure that each question will be processed, even if we did not receive
    # any fields for it. Also works to ensure the user doesn't add extra fields in
    for x in expected:
        items.append((u'question_%s_Trigger953' % x.number, None))

    # generate the answer_dict for each question, and place in extra
    for item in items:
        key, value = item[0], item[1]
        if key.startswith('question_'):
            answer = key.split("_", 2)
            question = get_question(answer[1], questionnaire)
            if not question:
                logging.warn("Unknown question when processing: %s" % answer[1])
                continue
            extra[question] = ans = extra.get(question, {})
            if (len(answer) == 2):
                ans['ANSWER'] = value
            elif (len(answer) == 3):
                ans[answer[2]] = value
            else:
                logging.warn("Poorly formed form element name: %r" % answer)
                continue
            extra[question] = ans

    errors = {}
    for question, ans in extra.items():
        if not question_satisfies_checks(question, runinfo):
            continue
        if u"Trigger953" not in ans:
            logging.warn("User attempted to insert extra question (or it's a bug)")
            continue
        try:
            cd = question.getcheckdict()
            # requiredif is the new way
            depon = cd.get('requiredif', None) or cd.get('dependent', None)
            if depon:
                depparser = BooleanParser(dep_check, runinfo, extra)
                if not depparser.parse(depon):
                    # if check is not the same as answer, then we don't care
                    # about this question plus we should delete it from the DB
                    delete_answer(question, runinfo.subject, runinfo.runid)
                    if cd.get('store', False):
                        runinfo.set_cookie(question.number, None)
                    continue
            add_answer(runinfo, question, ans)
            if cd.get('store', False):
                runinfo.set_cookie(question.number, ans['ANSWER'])
        except AnswerException, e:
            errors[question.number] = e
        except Exception:
            logging.exception("Unexpected Exception")
            transaction.rollback()
            raise

    if len(errors) > 0:
        res = show_questionnaire(request, runinfo, errors=errors)
        transaction.rollback()
        return res

    questionset_done.send(sender=None, runinfo=runinfo, questionset=questionset)

    next = questionset.next()
    while next and not questionset_satisfies_checks(next, runinfo):
        next = next.next()
    runinfo.questionset = next
    runinfo.save()

    if next is None: # we are finished
        return finish_questionnaire(runinfo, questionnaire)

    transaction.commit()
    return redirect_to_qs(runinfo)


def next_questionset_order_by_sortid(questionset_id, questionnaire_id):
    qsobjs = QuestionSet.objects.filter(questionnaire=questionnaire_id).order_by('sortid')
    next = False
    next_qs = None
    for qs in qsobjs:
        #print qs.pk
        #print questionset_id
        if next:
            next_qs = qs
            next = False
            break
        if qs.pk == int(questionset_id):
            next = True
    return next_qs


def handle_uploaded_file(f):
    print "abspath"

    with open(os.path.join(os.path.abspath(settings.PROJECT_DIR_ROOT + 'emif/static/upload_images/'), f.name),
              'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def check_database_add_conditions(request, questionnaire_id, sortid,
                                  template_name='database_add.html'):
    # -------------------------------------
    # --- Process POST with QuestionSet ---
    # -------------------------------------
    print "check_database_add_conditions"
    try:
        if request.FILES:
            print "file upload:"
            for name, f in request.FILES.items():
                print f
                handle_uploaded_file(f)
                #print request.FILES['file_uploaded']
                #handle_uploaded_file(request.FILES['file_uploaded'])
                #print request.POST
                #print request.POST['file_uploaded']
    except:
        raise
    qsobjs = QuestionSet.objects.filter(questionnaire=questionnaire_id)
    questionnaire = qsobjs[0].questionnaire
    question_set = None

    try:
        question_set = request.POST['active_qs']
        sortid = request.POST['active_qs_sortid']
    except:
        for qs in qsobjs:
            if qs.sortid == int(sortid):
                question_set = qs.pk
                break

    fingerprint_id = request.POST['fingerprint_id']
    #print "@QuestionSet" + str(question_set)
    #print "@QuestionSet- sortid" + str(sortid)
    # to confirm that we have the correct answers

    expected = []
    for qset in qsobjs:
        questions = qset.questions()
        for q in questions:
            expected.append(q)

    items = request.POST.items()
    extra = {} # question_object => { "ANSWER" : "123", ... }

    # this will ensure that each question will be processed, even if we did not receive
    # any fields for it. Also works to ensure the user doesn't add extra fields in
    for x in expected:
        items.append((u'question_%s_Trigger953' % x.number, None))

    # generate the answer_dict for each question, and place in extra
    for item in items:
        key, value = item[0], item[1]
        if key.startswith('question_'):
            answer = key.split("_", 2)
            question = get_question(answer[1], questionnaire)
            if not question:
                logging.warn("Unknown question when processing: %s" % answer[1])
                continue
            extra[question] = ans = extra.get(question, {})
            if (len(answer) == 2):
                ans['ANSWER'] = value
            elif (len(answer) == 3):
                ans[answer[2]] = value
            else:
                logging.warn("Poorly formed form element name: %r" % answer)
                continue
            extra[question] = ans

    errors = {}

    def verify_answer(question, answer_dict):

        type = question.get_type()

        if "ANSWER" not in answer_dict:
            answer_dict['ANSWER'] = None
        answer = None
        if type in Processors:
            answer = Processors[type](question, answer_dict) or ''
        else:
            raise AnswerException("No Processor defined for question type %s" % type)

        return True

    active_qs_with_errors = False
    #print "Active QuestionSet: " + question_set
    for question, ans in extra.items():
        #if not question_satisfies_checks(question, runinfo):
        #    continue
        #    
        #print ans 

        if u"Trigger953" not in ans:
            logging.warn("User attempted to insert extra question (or it's a bug)")
            continue
        try:
            cd = question.getcheckdict()
            #print cd 
            # requiredif is the new way
            depon = cd.get('requiredif', None) or cd.get('dependent', None)
            #print depon
            #if depon:
            #depparser = BooleanParser(dep_check, runinfo, extra)
            #if not depparser.parse(depon):
            # if check is not the same as answer, then we don't care
            # about this question plus we should delete it from the DB
            #delete_answer(question, runinfo.subject, runinfo.runid)
            #if cd.get('store', False):
            #    runinfo.set_cookie(question.number, None)
            #    continue
            #add_answer(runinfo, question, ans)
            verify_answer(question, ans)
            #if cd.get('store', False):
            #    runinfo.set_cookie(question.number, ans['ANSWER'])
        except AnswerException, e:
            errors[question.number] = e

            if (str(question.questionset.id) == question_set):
                #print "active enable"
                active_qs_with_errors = True
        except Exception:
            logging.exception("Unexpected Exception")
            raise

    if len(errors) > 0 and active_qs_with_errors:
        return show_fingerprint_page_errors(request, questionnaire_id, question_set,
                                            errors=errors, template_name='database_add.html', next=False, sortid=sortid,
                                            fingerprint_id=fingerprint_id)
        #print "show_fingerprint_page_errors"


    #question_set = int(question_set) + 1
    next_qs = next_questionset_order_by_sortid(question_set, questionnaire_id)
    if next_qs == None:
        # Redirect + handle that!!!
        pass
    else:
        sortid = next_qs.sortid
    question_set = str(next_qs.pk)
    #print question_set
    #print sortid
    return show_fingerprint_page_errors(request, questionnaire_id, question_set,
                                        errors={}, template_name='database_add.html', next=True, sortid=sortid,
                                        fingerprint_id=fingerprint_id)


def show_fingerprint_page_errors(request, q_id, qs_id, errors={}, template_name='database_add.html',
                                 next=False, sortid=0, fingerprint_id=None):
    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """
    try:

        qs_list = QuestionSet.objects.filter(questionnaire=q_id)
        #print "Q_id: " + q_id
        #print "Qs_id: " + qs_id
        #print "SortID: " + str(sortid)
        #print "QS List: " + str(qs_list)
        initial_sort = sortid

        if (int(sortid) == 99):
            sortid = len(qs_list) - 1
        question_set = qs_list[int(sortid)]
        #questions = Question.objects.filter(questionset=qs_id)

        questions = question_set.questions()
        #print "Questions: " + str(questions)
        #print "QuestionSet: " + str(question_set)

        questions_list = {}
        for qset_aux in qs_list:
            #questions_aux = Question.objects.filter(questionset=qset_aux)
            questions_list[qset_aux.id] = qset_aux.questions()
            #print "here"

        qlist = []
        jsinclude = []      # js files to include
        cssinclude = []     # css files to include
        jstriggers = []
        qvalues = {}

        qlist_general = []

        for k in qs_list:
            qlist = []
            qs_aux = None
            for question in questions_list[k.id]:
                qs_aux = question.questionset
                #print "Question: " + str(question)
                Type = question.get_type()
                _qnum, _qalpha = split_numal(question.number)

                qdict = {
                    'template': 'questionnaire/%s.html' % (Type),
                    'qnum': _qnum,
                    'qalpha': _qalpha,
                    'qtype': Type,
                    'qnum_class': (_qnum % 2 == 0) and " qeven" or " qodd",
                    'qalpha_class': _qalpha and (ord(_qalpha[-1]) % 2 \
                                                     and ' alodd' or ' aleven') or '',
                }

                # add javascript dependency checks
                cd = question.getcheckdict()
                depon = cd.get('requiredif', None) or cd.get('dependent', None)
                if depon:
                    # extra args to BooleanParser are not required for toString
                    parser = BooleanParser(dep_check)
                    qdict['checkstring'] = ' checks="%s"' % parser.toString(depon)
                    jstriggers.append('qc_%s' % question.number)
                if 'default' in cd and not question.number in cookiedict:
                    qvalues[question.number] = cd['default']
                if Type in QuestionProcessors:
                    qdict.update(QuestionProcessors[Type](request, question))
                    if 'jsinclude' in qdict:
                        if qdict['jsinclude'] not in jsinclude:
                            jsinclude.extend(qdict['jsinclude'])
                    if 'cssinclude' in qdict:
                        if qdict['cssinclude'] not in cssinclude:
                            cssinclude.extend(qdict['jsinclude'])
                    if 'jstriggers' in qdict:
                        jstriggers.extend(qdict['jstriggers'])
                        #if 'qvalue' in qdict and not question.number in cookiedict:
                        #    qvalues[question.number] = qdict['qvalue']

                qlist.append((question, qdict))
            if qs_aux == None:
                qs_aux = k
            qlist_general.append((qs_aux, qlist))
            #print "Next:"
        #if (initial_sort == 99):
        #    # Index on Solr
        #    index_answeres_from_qvalues(qlist_general, question_set.questionnaire, request.user.username)
        #print "Fingerprint"
        if (fingerprint_id != None):
            #print "Fingerprint" + fingerprint_id
            index_answeres_from_qvalues(qlist_general, question_set.questionnaire, request.user.username,
                                        fingerprint_id)

        r = r2r(template_name, request,
                questionset=question_set,
                questionsets=question_set.questionnaire.questionsets,
                runinfo=None,
                errors=errors,
                qlist=qlist,
                progress=None,
                triggers=jstriggers,
                qvalues=qvalues,
                jsinclude=jsinclude,
                cssinclude=cssinclude,
                async_progress=None,
                async_url=None,
                qs_list=qs_list,
                questions_list=qlist_general,
                fingerprint_id=fingerprint_id,
        )
        r['Cache-Control'] = 'no-cache'
        r['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"
    except:
        raise
    return r


def show_fingerprint_page_read_only(request, q_id, qs_id, errors={}, template_name='advanced_search.html'):
    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """
    try:

        qs_list = QuestionSet.objects.filter(questionnaire=q_id).order_by('sortid')

        #print "Q_id: " + q_id
        #print "Qs_id: " + qs_id
        #print "QS List: " + str(qs_list)
        if (int(qs_id) == 99):
            qs_id = len(qs_list) - 1
        question_set = qs_list[int(qs_id)]
        #questions = Question.objects.filter(questionset=qs_id)

        questions = question_set.questions()
        #print "Questions: " + str(questions)
        #print "QuestionSet: " + str(question_set)

        questions_list = {}
        for qset_aux in qs_list:
            #questions_aux = Question.objects.filter(questionset=qset_aux)
            questions_list[qset_aux.id] = qset_aux.questions()
            #print "here"

        qlist = []
        jsinclude = []      # js files to include
        cssinclude = []     # css files to include
        jstriggers = []
        qvalues = {}

        if request.POST:

            for k, v in request.POST.items():
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
            query = convert_qvalues_to_query(qvalues, q_id)
            #print "Query: " + query
            return results_fulltext_aux(request, query)

        qlist_general = []

        for k in qs_list:
            qlist = []
            qs_aux = None
            for question in questions_list[k.id]:
                qs_aux = question.questionset
                #print "Question: " + str(question)
                Type = question.get_type()
                _qnum, _qalpha = split_numal(question.number)

                qdict = {
                    'template': 'questionnaire/%s.html' % (Type),
                    'qnum': _qnum,
                    'qalpha': _qalpha,
                    'qtype': Type,
                    'qnum_class': (_qnum % 2 == 0) and " qeven" or " qodd",
                    'qalpha_class': _qalpha and (ord(_qalpha[-1]) % 2 \
                                                     and ' alodd' or ' aleven') or '',
                }

                # add javascript dependency checks
                cd = question.getcheckdict()
                depon = cd.get('requiredif', None) or cd.get('dependent', None)
                if depon:
                    # extra args to BooleanParser are not required for toString
                    parser = BooleanParser(dep_check)
                    qdict['checkstring'] = ' checks="%s"' % parser.toString(depon)
                    jstriggers.append('qc_%s' % question.number)
                if 'default' in cd and not question.number in cookiedict:
                    qvalues[question.number] = cd['default']
                if Type in QuestionProcessors:
                    qdict.update(QuestionProcessors[Type](request, question))
                    if 'jsinclude' in qdict:
                        if qdict['jsinclude'] not in jsinclude:
                            jsinclude.extend(qdict['jsinclude'])
                    if 'cssinclude' in qdict:
                        if qdict['cssinclude'] not in cssinclude:
                            cssinclude.extend(qdict['jsinclude'])
                    if 'jstriggers' in qdict:
                        jstriggers.extend(qdict['jstriggers'])
                        #if 'qvalue' in qdict and not question.number in cookiedict:
                        #    qvalues[question.number] = qdict['qvalue']
                        #

                qlist.append((question, qdict))
            if qs_aux == None:
                #print "$$$$$$ NONE"
                qs_aux = k
            qlist_general.append((qs_aux, qlist))

        errors = {}
        fingerprint_id = generate_hash()
        r = r2r(template_name, request,
                questionset=question_set,
                questionsets=question_set.questionnaire.questionsets,
                runinfo=None,
                errors=errors,
                qlist=qlist,
                progress=None,
                triggers=jstriggers,
                qvalues=qvalues,
                jsinclude=jsinclude,
                cssinclude=cssinclude,
                async_progress=None,
                async_url=None,
                qs_list=qs_list,
                questions_list=qlist_general,
                fingerprint_id=fingerprint_id,
        )
        r['Cache-Control'] = 'no-cache'
        r['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"
    except:

        raise
    return r


def feedback(request):
    subject = request.POST.get('topic', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    emails_to_feedback = 'bastiao@ua.pt'

    if subject and message and from_email:
        try:
            send_mail(subject, message, "bioinformatics@ua.pt", [emails_to_feedback, from_email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('http://bioinformatics.ua.pt/emif/feedback/thankyou/')
    else:
        return render_to_response('feedback.html', {'form': ContactForm(), 'email_to': emails_to_feedback,
                                                    'request': request}, RequestContext(request))

        # return render_to_response('feedback.html', {'form': ContactForm()},
        #     RequestContext(request))


def feedback_thankyou(request):
    return render_to_response('feedback_thankyou.html')


def show_fingerprint_page(request, runinfo, errors={}, template_name='database_edit.html'):
    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """
    questions = runinfo.questionset.questions()

    questions = runinfo.questionset.questions()

    qlist = []
    jsinclude = []      # js files to include
    cssinclude = []     # css files to include
    jstriggers = []
    qvalues = {}

    # initialize qvalues        
    cookiedict = runinfo.get_cookiedict()
    for k, v in cookiedict.items():
        qvalues[k] = v

    substitute_answer(qvalues, runinfo.questionset)

    for question in questions:

        # if we got here the questionset will at least contain one question
        # which passes, so this is all we need to check for
        if not question_satisfies_checks(question, runinfo):
            continue

        Type = question.get_type()
        _qnum, _qalpha = split_numal(question.number)

        qdict = {
            'template': 'questionnaire/%s.html' % (Type),
            'qnum': _qnum,
            'qalpha': _qalpha,
            'qtype': Type,
            'qnum_class': (_qnum % 2 == 0) and " qeven" or " qodd",
            'qalpha_class': _qalpha and (ord(_qalpha[-1]) % 2 \
                                             and ' alodd' or ' aleven') or '',
        }

        # substitute answer texts
        substitute_answer(qvalues, question)

        # add javascript dependency checks
        cd = question.getcheckdict()
        depon = cd.get('requiredif', None) or cd.get('dependent', None)
        if depon:
            # extra args to BooleanParser are not required for toString
            parser = BooleanParser(dep_check)
            qdict['checkstring'] = ' checks="%s"' % parser.toString(depon)
            jstriggers.append('qc_%s' % question.number)
        if 'default' in cd and not question.number in cookiedict:
            qvalues[question.number] = cd['default']
        if Type in QuestionProcessors:
            qdict.update(QuestionProcessors[Type](request, question))
            if 'jsinclude' in qdict:
                if qdict['jsinclude'] not in jsinclude:
                    jsinclude.extend(qdict['jsinclude'])
            if 'cssinclude' in qdict:
                if qdict['cssinclude'] not in cssinclude:
                    cssinclude.extend(qdict['jsinclude'])
            if 'jstriggers' in qdict:
                jstriggers.extend(qdict['jstriggers'])
            if 'qvalue' in qdict and not question.number in cookiedict:
                qvalues[question.number] = qdict['qvalue']

        qlist.append((question, qdict))

    try:
        has_progress = settings.QUESTIONNAIRE_PROGRESS in ('async', 'default')
        async_progress = settings.QUESTIONNAIRE_PROGRESS == 'async'
    except AttributeError:
        has_progress = True
        async_progress = False

    if has_progress:
        if async_progress:
            progress = cache.get('progress' + runinfo.random, 1)
        else:
            progress = get_progress(runinfo)
    else:
        progress = 0

    if request.POST:
        for k, v in request.POST.items():
            if k.startswith("question_"):
                s = k.split("_")
                if len(s) == 4:
                    qvalues[s[1] + '_' + v] = '1' # evaluates true in JS
                elif len(s) == 3 and s[2] == 'comment':
                    qvalues[s[1] + '_' + s[2]] = v
                else:
                    qvalues[s[1]] = v
    errors = {}
    r = r2r(template_name, request,
            questionset=runinfo.questionset,
            questionsets=runinfo.questionset.questionnaire.questionsets,
            runinfo=runinfo,
            errors=errors,
            qlist=qlist,
            progress=progress,
            triggers=jstriggers,
            qvalues=qvalues,
            jsinclude=jsinclude,
            cssinclude=cssinclude,
            async_progress=async_progress,
            async_url=reverse('progress', args=[runinfo.random])
    )
    r['Cache-Control'] = 'no-cache'
    r['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"
    return r




