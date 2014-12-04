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
from django.shortcuts import render, redirect


from django.core import serializers
from django.conf import settings
from django.http import *
from django.http import Http404
from django.utils import simplejson


from questionnaire import *
from questionnaire.views import *
from emif.models import AdvancedQuery

from emif.utils import generate_hash

from fingerprint.services import *
from fingerprint.tasks import indexFingerprintCelery
from fingerprint.models import QuestionSetCompletion

from geolocation.services import *

from emif.models import QueryLog, AdvancedQuery, AdvancedQueryAnswer

import json


def export_bd_answers(request, runcode):
    """
    Method to export answers of a specific database to a csv file
    :param request:
    :param runcode:
    """

    list_databases = get_databases_from_solr(request, "id:" + runcode)
    return save_answers_to_csv(list_databases, 'MyDB')

def database_add(request, questionnaire_id, sortid):

    response = show_fingerprint_page_read_only(request, questionnaire_id, sortid,
                                               template_name='database_add.html')

    return response

def delete_fingerprint(request, id):

    deleteFingerprint(id, request.user)

    return redirect('databases')

# detailed view with direct linking to questionset
def database_edit_dl(request, fingerprint_id, questionnaire_id, sort_id, template_name="database_edit.html"):
    return database_edit(request, fingerprint_id, questionnaire_id, sort_id=sort_id, template_name=template_name)


def database_edit(request, fingerprint_id, questionnaire_id, sort_id=1, template_name="database_edit.html", readonly=False):

    try:
        this_fingerprint = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)

        users_db = this_fingerprint.unique_users_string()
        created_date = this_fingerprint.created

        qs_list = QuestionSet.objects.filter(questionnaire=questionnaire_id)

        question_set = None
        try:
            question_set = qs_list.get(sortid=sort_id)
        except:
            raise Http404

        answers = Answer.objects.filter(fingerprint_id=this_fingerprint)

        # well this doesnt scale well, we should have the database name on the fingerprint
        # it probably will be mitigated by using the descriptor that should be updated on save...
        fingerprint_name = this_fingerprint.findName()

        # count questionset filled answers
        qreturned = []

        # mark questionsets that have questions request by other users
        requests = AnswerRequest.objects.filter(fingerprint = this_fingerprint, removed=False)

        qscs = QuestionSetCompletion.objects.filter(fingerprint=this_fingerprint).order_by('questionset')

        for qsc in qscs:
            print qsc.possible
            questionset_requests = requests.filter(question__questionset=qsc.questionset)
            qreturned.append([qsc.questionset, qsc.answered, qsc.possible, qsc.fill, questionset_requests])


        r = r2r(template_name, request,
                questionset=question_set,
                questionsets=qreturned,
                globalprogress = this_fingerprint.fill,
                runinfo=None,
                errors=None,
                progress=None,
                fingerprint_id=fingerprint_id,
                q_id = questionnaire_id,
                sort_id = sort_id,
                async_progress=None,
                async_url=None,
                qs_list=qs_list,
                breadcrumb=True,
                name=fingerprint_name.encode('utf-8'),
                id=fingerprint_id,
                users_db=users_db,
                created_date=created_date,
                hide_add=True,
                readonly=readonly
        )
        r['Cache-Control'] = 'no-cache'
        r['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"

        return r

    except Fingerprint.DoesNotExist:
        print "-- Error obtaining fingerprint "+str(fingerprint_id)

    # Something is really wrong if we get here...
    return HttpResponse('Error open edit for fingerprint '+str(fingerprint_id), status=500)

def database_detailed_view(request, fingerprint_id, questionnaire_id, template_name="database_edit.html"):

    return database_edit(request, fingerprint_id, questionnaire_id, template_name=template_name, readonly=True);

# detailed view with direct linking to questionset
def database_detailed_view_dl(request, fingerprint_id, questionnaire_id, sort_id, template_name="database_edit.html"):

    return database_edit(request, fingerprint_id, questionnaire_id, sort_id=sort_id, template_name=template_name, readonly=True);


def database_detailed_qs(request, fingerprint_id, questionnaire_id, sort_id):

    response = render_one_questionset(request, questionnaire_id, sort_id, fingerprint_id = fingerprint_id, is_new=False, readonly=True,
                                               template_name='fingerprint_add_qs.html')

    return response

def show_fingerprint_page_read_only(request, q_id, qs_id, SouMesmoReadOnly=False, aqid=None, errors={}, template_name='advanced_search.html'):

    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """
    # Getting first timestamp

    if template_name == "database_add.html" :
        hide_add = True
    else:
        hide_add = False

    serialized_query = None

    if template_name == 'advanced_search.html' and aqid != None:
        this_query = AdvancedQuery.objects.get(id=aqid)
        serialized_query = this_query.serialized_query

    try:

        qs_list = QuestionSet.objects.filter(questionnaire=q_id).order_by('sortid')

        if (int(qs_id) == 99):
            qs_id = len(qs_list) - 1

        question_set = qs_list[int(qs_id)]

        questions = question_set.questions()

        questions_list = {}
        for qset_aux in qs_list:
            questions_list[qset_aux.id] = qset_aux.questions()

        fingerprint_id = generate_hash()

        #### Find out about the number of answers serverside
        qreturned = []
        for x in question_set.questionnaire.questionsets():
            ttct = x.total_count()
            ans = 0
            percentage = 0
            qreturned.append([x, ans, ttct, percentage])
        #### End of finding out about the number of answers serverside

        r = r2r(template_name, request,
                        questionset=question_set,
                        globalprogress = 0,
                        questionsets=qreturned,
                        runinfo=None,
                        progress=None,
                        async_progress=None,
                        async_url=None,
                        qs_list=qs_list,
                        fingerprint_id=fingerprint_id,
                        breadcrumb=True,
                        hide_add=hide_add,
                        q_id=q_id,
                        aqid=aqid,
                        serialized_query=serialized_query)
        r['Cache-Control'] = 'no-cache'

        r['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"


    except:
        raise

    return r

def database_add_qs(request, fingerprint_id, questionnaire_id, sortid):

    response = render_one_questionset(request, questionnaire_id, sortid, fingerprint_id= fingerprint_id,
                                               template_name='fingerprint_add_qs.html')

    return response

def database_edit_qs(request, fingerprint_id, questionnaire_id, sort_id):

    response = render_one_questionset(request, questionnaire_id, sort_id, fingerprint_id = fingerprint_id, is_new=False,
                                               template_name='fingerprint_add_qs.html')

    return response

def render_one_questionset(request, q_id, qs_id, errors={}, aqid=None, fingerprint_id=None, is_new=True, readonly = False, template_name='fingerprint_add_qs.html'):
    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """
    request2 = None
    this_fingerprint = None

    # In case we should be getting an advancedquery
    if aqid != None:
        this_query = AdvancedQuery.objects.get(id=aqid)
        this_answers = AdvancedQueryAnswer.objects.filter(refquery=this_query)

        request2 = RequestMonkeyPatch()

        request2.method = request.method

        for answer in this_answers:
            request2.get_post()[answer.question] = answer.answer


    if fingerprint_id != None and not is_new:

        try:
            this_fingerprint = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)

            this_answers = Answer.objects.filter(fingerprint_id=this_fingerprint)

            extra = {}

            request2 = RequestMonkeyPatch()

            request2.method = request.method

            for answer in this_answers:
                this_q  = answer.question
                value   = answer.data

                if "[" in str(value):
                    value = str(value).replace("]", "").replace("[", "")

                request2.get_post()['question_%s' % this_q.number] = value

                if answer.comment != None:
                    request2.get_post()['comment_question_%s' % this_q.number] = answer.comment

                # This "extra" field was on the old solr version, i will admit, i have no clue wth this does...
                # it doesn't seem to make any difference as far as i could check, anyway i left it here commented
                # in case we need it after all
                #extra[this_q] = ans = extra.get(this_q, {})
                #ans['ANSWER'] = value
                #extra[this_q] = ans

        except Fingerprint.DoesNotExist:
            print "-Error fingerprint "+fingerprint_id + " does not exist but we think it does."

    try:

        qs_list = QuestionSet.objects.filter(questionnaire=q_id, sortid=qs_id).order_by('sortid')

        if (int(qs_id) == 99):
            qs_id = len(qs_list) - 1
        question_set = qs_list[0]
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

                    # qdict['checkstring'] = ' checks="%s"' % parser.toString(depon)

                    #It allows only 1 dependency
                    #The line above allows multiple dependencies but it has a bug when is parsing white spaces
                    qdict['checkstring'] = ' checks="dep_check(\'question_%s\')"' % depon

                    qdict['depon_class'] = ' depon_class'
                    jstriggers.append('qc_%s' % question.number)
                    if question.text[:2] == 'h1':
                        jstriggers.append('acc_qc_%s' % question.number)
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

            # extracting answers
        if aqid != None:
            (qlist_general, qlist, jstriggers, qvalues, jsinclude, cssinclude, extra_fields, hasErrors) = extract_answers(request2, q_id, question_set, qs_list)

        elif fingerprint_id != None and not is_new:
            (qlist_general, qlist, jstriggers, qvalues, jsinclude, cssinclude, extra_fields, hasErrors) = extract_answers(request2, q_id, question_set, qs_list)

        permissions = None
        if this_fingerprint != None:
            permissions = this_fingerprint.getPermissions(question_set)

        advanced_search=False
        if template_name == 'fingerprint_search_qs.html':
            advanced_search = True

        ansrequests = []
        if is_new == False and readonly == False:
            ansrequests = AnswerRequest.objects.filter(fingerprint = this_fingerprint, question__questionset__sortid=qs_id, removed = False)

        r = r2r(template_name, request,
                questionset=question_set,
                depmap = json.dumps(question_set.dependency_tree()),
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
                advanced_search = advanced_search,
                questions_list=qlist_general,
                fingerprint_id=fingerprint_id,
                breadcrumb=True,
                permissions=permissions,
                readonly=readonly,
                aqid = aqid,
                answer_requests = ansrequests
        )

        r['Cache-Control'] = 'no-cache'
        r['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"

    except:

        raise
    return r

def check_database_add_conditions(request, questionnaire_id, sortid, saveid,
                                  template_name='database_add.html', users_db=None, created_date=None):
    # -------------------------------------
    # --- Process POST with QuestionSet ---
    # -------------------------------------
    try:
        if request.FILES:
            print "file upload:"
            for name, f in request.FILES.items():
                handle_uploaded_file(f)
    except:
        raise

    qsobjs = QuestionSet.objects.filter(questionnaire=questionnaire_id)
    questionnaire = qsobjs[0].questionnaire
    question_set = None
    saveqs = None

    try:
        question_set = request.POST['active_qs']
        sortid = request.POST['active_qs_sortid']
    except:
        for qs in qsobjs:
            if qs.sortid == int(sortid):
                question_set = qs.pk
                break

    for qs in qsobjs:
        if qs.sortid == int(saveid):
            saveqs = [qs]
            break

    if (int(sortid) == 99):
            sortid = len(questionnaire.questionsets()) - 1

    question_set2 = qsobjs[int(sortid)]

    fingerprint_id = request.POST['fingerprint_id']

    request2 = RequestMonkeyPatch()

    if request.POST:
        (qlist_general, qlist, jstriggers, qvalues, jsinclude, cssinclude, extra_fields, hasErrors) = extract_answers(request, questionnaire_id, question_set2, saveqs)
    else:
        (qlist_general, qlist, jstriggers, qvalues, jsinclude, cssinclude, extra_fields, hasErrors) = extract_answers(request2, questionnaire_id, question_set2, saveqs)

    if fingerprint_id != None:
        if users_db==None:
            users_db = request.user.username

        if not hasErrors:
            add_city(qlist_general)

            success = saveFingerprintAnswers(qlist_general, fingerprint_id, question_set2.questionnaire, users_db, extra_fields=extra_fields, created_date=created_date)

            #print "SUCCESS SAVING:"+str(success)

            if not success:

                qs = -1
                try :
                    qs = question_set2.questionnaire.findMandatoryQs().sortid
                except:
                    pass
                return HttpResponse(simplejson.dumps({'mandatoryqs': qs}),
                                    mimetype='application/json')

            if request.POST:
                setNewPermissions(request, fingerprint_id, sortid)
            else:
                setNewPermissions(request2, fingerprint_id, sortid)

            # new version that just serializes the created fingerprint object (this eventually can be done using celery)
            indexFingerprintCelery.delay(fingerprint_id)

    return HttpResponse(simplejson.dumps({'success': 'true'}),
                                    mimetype='application/json')

