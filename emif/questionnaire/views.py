#!/usr/bin/python
# vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.db import transaction
from django.conf import settings
import datetime

from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from questionnaire import QuestionProcessors
from questionnaire import Fingerprint_Summary
from questionnaire import questionnaire_done
from questionnaire import questionset_done
from questionnaire import AnswerException
from questionnaire import Processors
from questionnaire.models import *
from questionnaire.parsers import *

from questionnaire.utils import *
from questionnaire.request_cache import request_cache
from questionnaire import profiler

from searchengine.search_indexes import convert_text_to_slug
from searchengine.models import Slugs

import logging
import random
import md5
import re

from openpyxl import load_workbook

from django.template.defaultfilters import slugify

def writeLog(log):
    with open("log_%s.txt" % datetime.datetime.now().strftime("%Y%m%d-%H%M%S"), "w") as f:
        f.write(log)
        f.close()

def get_slug(slug):
    slugs_objs = Slugs.objects.filter(slug1=slug)
    slug_aux = None
    if (len(slugs_objs)>0):
        slug_aux=slugs_objs[0]
    else:
        return slug
    slug_name_final = ""
    slug_arr = slug_aux.slug1.split("_")
    if len(slug_arr)>0:
        if (slug_arr[len(slug_arr)-1].isdigit()):
            slug_number = int(slug_arr[len(slug_arr)-1]) + 1
            slug_arr[len(slug_arr)-1] = str(slug_number)
            slug_name_final = "_".join(slug_arr)

        else:
            slug_name_final = slug_aux.slug1 + "_0"
    else:
        slug_name_final = slug_aux.slug1 + "_0"

    return slug_name_final

def r2r(tpl, request, **contextdict):
    "Shortcut to use RequestContext instead of Context in templates"
    contextdict['request'] = request
    return render_to_response(tpl, contextdict, context_instance = RequestContext(request))

#def get_runinfo(random):
#    "Return the RunInfo entry with the provided random key"
#    res = RunInfo.objects.filter(random=random.lower())
#    return res and res[0] or None

def get_question(number, questionnaire):
    "Return the specified Question (by number) from the specified Questionnaire"
    res = Question.objects.filter(number=number, questionset__questionnaire=questionnaire)
    return res and res[0] or None

def _table_headers(questions):
    """
    Return the header labels for a set of questions as a list of strings.

    This will create separate columns for each multiple-choice possiblity
    and freeform options, to avoid mixing data types and make charting easier.
    """
    ql = list(questions.distinct('number'))
    ql.sort(lambda x, y: numal_sort(x.number, y.number))
    columns = []
    for q in ql:
        if q.type == 'choice-yesnocomment':
            columns.extend([q.number, q.number + "-freeform"])
        elif q.type == 'choice-freeform':
            columns.extend([q.number, q.number + "-freeform"])
        elif q.type.startswith('choice-multiple'):
            cl = [c.value for c in q.choice_set.all()]
            cl.sort(numal_sort)
            columns.extend([q.number + '-' + value for value in cl])
            if q.type == 'choice-multiple-freeform':
                columns.append(q.number + '-freeform')
        else:
            columns.append(q.number)
    return columns



@permission_required("questionnaire.export")
def export_csv(request, qid): # questionnaire_id
    """
    For a first_name questionnaire id, generaete a CSV containing all the
    answers for all subjects.
    """
    #print "export_csv"
    import tempfile, csv, cStringIO, codecs
    from django.core.servers.basehttp import FileWrapper
    #print qid
    class UnicodeWriter:
        """
        COPIED from http://docs.python.org/library/csv.html example:

        A CSV writer which will write rows to CSV file "f",
        which is encoded in the first_name encoding.
        """

        def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
            # Redirect output to a queue
            self.queue = cStringIO.StringIO()
            self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
            self.stream = f
            self.encoder = codecs.getincrementalencoder(encoding)()

        def writerow(self, row):
            self.writer.writerow([s.encode("utf-8") for s in row])
            # Fetch UTF-8 output from the queue ...
            data = self.queue.getvalue()
            data = data.decode("utf-8")
            # ... and reencode it into the target encoding
            data = self.encoder.encode(data)
            # write to the target stream
            self.stream.write(data)
            # empty queue
            self.queue.truncate(0)

        def writerows(self, rows):
            for row in rows:
                self.writerow(row)

    fd = tempfile.TemporaryFile()

    questionnaire = get_object_or_404(Questionnaire, pk=int(qid))
    headings, answers = answer_export(questionnaire)

    writer = UnicodeWriter(fd)
    writer.writerow([u'subject', u'runid'] + headings)
    for subject, runid, answer_row in answers:
        row = ["%s/%s" % (subject.id, subject.state), runid] + [
            a if a else '--' for a in answer_row]
        writer.writerow(row)

    response = HttpResponse(FileWrapper(fd), mimetype="text/csv")
    response['Content-Length'] = fd.tell()
    response['Content-Disposition'] = 'attachment; filename="export-%s.csv"' % qid
    fd.seek(0)
    return response

def answer_export(questionnaire, answers=None):
    """
    questionnaire -- questionnaire model for export
    answers -- query set of answers to include in export, defaults to all

    Return a flat dump of column headings and all the answers for a 
    questionnaire (in query set answers) in the form (headings, answers) 
    where headings is:
        ['question1 number', ...]
    and answers is:
        [(subject1, 'runid1', ['answer1.1', ...]), ... ]

    The headings list might include items with labels like 
    'questionnumber-freeform'.  Those columns will contain all the freeform
    answers for that question (separated from the other answer data).

    Multiple choice questions will have one column for each choice with
    labels like 'questionnumber-choice'.

    The items in the answers list are unicode strings or empty strings
    if no answer was first_name.  The number of elements in each answer list will
    always match the number of headings.    
    """
    if answers is None:
        answers = Answer.objects.all()
    answers = answers.filter(
        question__questionset__questionnaire=questionnaire).order_by(
        'subject', 'runid', 'question__questionset__sortid', 'question__number')
    answers = answers.select_related()
    questions = Question.objects.filter(
        questionset__questionnaire=questionnaire)
    headings = _table_headers(questions)

    coldict = {}
    for num, col in enumerate(headings): # use coldict to find column indexes
        coldict[col] = num
    # collect choices for each question
    qchoicedict = {}
    for q in questions:
        qchoicedict[q.id] = [x[0] for x in q.choice_set.values_list('value')]

    runid = subject = None
    out = []
    row = []
    for answer in answers:
        if answer.runid != runid or answer.subject != subject:
            if row: 
                out.append((subject, runid, row))
            runid = answer.runid
            subject = answer.subject
            row = [""] * len(headings)
        ans = answer.split_answer()
        if type(ans) == int:
            ans = str(ans) 
        for choice in ans:
            col = None
            if type(choice) == list:
                # freeform choice
                choice = choice[0]
                col = coldict.get(answer.question.number + '-freeform', None)
            if col is None: # look for enumerated choice column (multiple-choice)
                col = coldict.get(answer.question.number + '-' + choice, None)
            if col is None: # single-choice items
                if ((not qchoicedict[answer.question.id]) or
                    choice in qchoicedict[answer.question.id]):
                    col = coldict.get(answer.question.number, None)
            if col is None: # last ditch, if not found throw it in a freeform column
                col = coldict.get(answer.question.number + '-freeform', None)
            if col is not None:
                row[col] = choice
    # and don't forget about the last one
    if row: 
        out.append((subject, runid, row))
    return headings, out
    
def dep_check(expr, runinfo, answerdict):
    """
    Given a comma separated question number and expression, determine if the
    provided answer to the question number satisfies the expression.

    If the expression starts with >, >=, <, or <=, compare the rest of
    the expression numerically and return False if it's not able to be
    converted to an integer.

    If the expression starts with !, return true if the rest of the expression
    does not match the answer.

    Otherwise return true if the expression matches the answer.

    If there is no comma and only a question number, it checks if the answer
    is "yes"

    When looking up the answer, it first checks if it's in the answerdict,
    then it checks runinfo's cookies, then it does a database lookup to find
    the answer.
    
    The use of the comma separator is purely historical.
    """

    if hasattr(runinfo, 'questionset'):
        questionnaire = runinfo.questionset.questionnaire
    elif hasattr(runinfo, 'questionnaire'):
        questionnaire = runinfo.questionnaire
    else:
        assert False

    if "," not in expr:
        expr = expr + ",yes"

    check_questionnum, check_answer = expr.split(",",1)
    try:
        check_question = Question.objects.get(number=check_questionnum,
          questionset__questionnaire = questionnaire)
    except Question.DoesNotExist:
        return False

    if check_question in answerdict:
        # test for membership in multiple choice questions
        # FIXME: only checking answerdict
        for k, v in answerdict[check_question].items():
            if not k.startswith('multiple_'):
                continue
            if check_answer.startswith("!"):
                if check_answer[1:].strip() == v.strip():
                    return False
            elif check_answer.strip() == v.strip():
                return True
        actual_answer = answerdict[check_question].get('ANSWER', '')
    elif hasattr(runinfo, 'get_cookie') and runinfo.get_cookie(check_questionnum, False):
        actual_answer = runinfo.get_cookie(check_questionnum)
    else:
        # retrieve from database
        ansobj = Answer.objects.filter(question=check_question,
            runid=runinfo.runid, subject=runinfo.subject)
        if ansobj:
            actual_answer = ansobj[0].split_answer()[0]
            logging.warn("Put `store` in checks field for question %s" \
            % check_questionnum)
        else:
            actual_answer = None

    if not actual_answer:
        if check_question.getcheckdict():
            actual_answer = check_question.getcheckdict().get('default')
    
    if actual_answer is None:
        actual_answer = u''
    if check_answer[0:1] in "<>":
        try:
            actual_answer = float(actual_answer)
            if check_answer[1:2] == "=":
                check_value = float(check_answer[2:])
            else:
                check_value = float(check_answer[1:])
        except:
            logging.error("ERROR: must use numeric values with < <= => > checks (%r)" % check_question)
            return False
        if check_answer.startswith("<="):
            return actual_answer <= check_value
        if check_answer.startswith(">="):
            return actual_answer >= check_value
        if check_answer.startswith("<"):
            return actual_answer < check_value
        if check_answer.startswith(">"):
            return actual_answer > check_value
    if check_answer.startswith("!"):
        return check_answer[1:].strip() != actual_answer.strip()
    return check_answer.strip() == actual_answer.strip()

def import_questionnaire(request, template_name='import_questionnaire.html'):
    """
    To-Do
    - validation of template structure and content fields
    """

    #_debug=True to not save
    _debug = False

    qNumber = QuestionNumber()
    slugs = []
    # wb = load_workbook(filename = r'/Volumes/EXT1/Dropbox/MAPi-Dropbox/EMIF/Code/emif/emif/questionnaire_ad_v2.xlsx')
    # wb = load_workbook(filename = r'/Volumes/EXT1/Dropbox/MAPi-Dropbox/EMIF/Observational_Data_Sources_Template_v5.xlsx')
    # wb = load_workbook(filename = r'C:/Questionnaire_template_v3.4.xlsx')
    wb = load_workbook(filename =r'/home/ribeiro/Questionnaire_template_v3.5.3.xlsx')
    ws = wb.get_active_sheet()
    log = ''

    # Cell B1: Name of questionnaire
    name = ws.cell('B1').value
    slugQ = convert_text_to_slug(ws.cell('B1').value)
    disable = False

    def format_number(number):
        # print number
        number_arr = number.split(".")

        result = number_arr[0] + "."
        for i in range(1,len(number_arr)):

            val = int(number_arr[i])
            if val<10:
                val = "0" + str(val)
            number_arr[i] = str(val)
            if (i!=len(number_arr)-1):
                result += str(val) + "."
            else:
                result += str(val)
        # print "result " + result
        return result

    questionnaire = Questionnaire(name=name, disable=disable, slug=slugQ, redirect_url='/')
    log += '\nQuestionnaire created %s ' % questionnaire

    try:
        if not _debug:
            questionnaire.save()
            log += '\nQuestionnaire saved %s ' % questionnaire
        _choices_array = {}
        _questions_rows = {}

        #############################
        # TIPS:
        # Type of Row: QuestionSet, Category, Question
        # Columns: Type, Text/Question, Level/Number, Data type, Value list, Help text/Description, Tooltip, Slug, Stats
        #############################

        for row in ws.rows[2:]:
            if len(row) > 0:
                type_Column = row[0]

                text_question_Column = row[1]

                if (text_question_Column.value!=None):
                    text_question_Column.value = text_question_Column.value.encode('ascii', 'ignore')
                level_number_column = row[2]
                _checks = ''

                # Type = QUESTIONSET
                # Columns required:  Type, Text/Question
                # Columns optional:  Help text/Description, Tooltip
                if str(type_Column.value) == "QuestionSet":
                    sortid = str(level_number_column.value)
                    try:
                        qNumber.getNumber('h0', sortid)
                    except:
                        writeLog(log)
                        raise
                    text_en = 'h1. %s' % text_question_Column.value
                    slug_qs = str(slugQ) + "_" + convert_text_to_slug(str(text_question_Column.value))
                    if row[5].value:
                        helpText = row[5].value
                    else:
                        helpText = ""
                    tooltip = False
                    if row[6].value:
                        if str(row[6].value).lower() == 'yes':
                            tooltip = True

                    questionset = QuestionSet(questionnaire=questionnaire, checks='required', sortid=sortid, text_en=text_en, heading=slug_qs, help_text=helpText, tooltip=tooltip)
                    log += '\n%s - QuestionSet created %s - %s ' % (type_Column.row, sortid, text_en)
                    try:
                        if not _debug:
                            questionset.save()
                            log += '\n%s - QuestionSet saved %s - %s ' % (type_Column.row, sortid, text_en)
                    except:

                        log += "\n%s - Error to save questionset %s - %s" % (type_Column.row, sortid, text_en)
                        writeLog(log)
                        raise

                # Type = CATEGORY
                # Columns required:  Type, Text/Question, Level/Number, Category
                # Columns optional:  Help text/Description, Slug, Tooltip, Dependencies
                elif str(type_Column.value) == "Category":

                    try:
                        text_en = str(level_number_column.value) + '. ' + str(text_question_Column.value)
                        if row[7].value:
                            slug = row[7].value
                        else:
                            slug = convert_text_to_slug(str(row[1].value)[:50])
                            #slug = get_slug(slug, questionnaire.pk)
                            slug = get_slug(slug)

                        if row[5].value:
                            helpText = row[5].value
                        else:
                            helpText = ""
                        # print "HELP_TEXT1: " + str(helpText)
                        _tooltip = False

                        if row[6].value:
                            if str(row[6].value).lower() == 'yes':
                                _tooltip = True

                        #If has dependencies
                        if row[8].value:
                            try:
                                dependencies_list = row[8]
                                list_dep_aux = dependencies_list.value.split('|')
                                question_num_parent = str(_questions_rows.get(int(list_dep_aux[0])))

                                # print str(row[0].row) + " str(list_dep_aux[0]: " + str(int(list_dep_aux[0]))
                                # print str(row[0].row) + " question_num_parent: " + question_num_parent
                                # print str(row[0].row) + " _questions_rows: " + str(_questions_rows)

                                index_aux = int(str(list_dep_aux[1]))-1
                                choice_parent_list = _choices_array.get(int(list_dep_aux[0]))
                                choice_parent = choice_parent_list[index_aux]
                                _checks = 'dependent=\"' + str(question_num_parent) + ',' + str(choice_parent) + '\"'

                            except:
                                raise

                        try:
                            questionNumber = qNumber.getNumber(level_number_column.value)
                            questionNumber = format_number(str(questionNumber))
                        except:
                            log += "\n%s - Error to create Category number %s" % (type_Column.row, text_en)
                            writeLog(log)
                            raise

                        #Create or load slug
                        #print slug
                        slugs = Slugs.objects.filter(slug1=slug, description=text_en)
                        if len(slugs) <= 0:
                            slug_db = Slugs(slug1=slug, description=text_en)
                            slug_db.save()
                        else:
                            slug_db = slugs[0]

                        question = Question(questionset=questionset, text_en=text_en, number=str(questionNumber),
                                            type='comment', help_text=helpText, slug=slug, slug_fk=slug_db, stats=False, category=True,
                                            tooltip=_tooltip, checks=_checks)

                        if not _debug:
                            question.save()
                            log += '\n%s - Category created %s ' % (type_Column.row, question)

                        _questions_rows[type_Column.row] = str(questionNumber)

                        #if not _debug:
                            # TODO: I think we don't need this now, since question now has a slug foreign key
                        #    save_slug(question.slug,  question.text_en, question)

                        # slugs.append((question.slug,  question.text_en, question))
                        log += '\n%s - Category saved %s ' % (type_Column.row, question)
                    except:
                        log += "\n%s - Error to save Category %s" % (type_Column.row, text_en)
                        writeLog(log)
                        raise

                # Type = QUESTION
                # Columns required:  Type, Text/Question, Level/Number, Data Type, Category, Stats
                # Columns optional:  Value List, Help text/Description, Tooltip, Dependencies
                else:
                    #try:
                    text_en = str(level_number_column.value) + '. ' + str(text_question_Column.value)
                    #except:
                        #import pdb
                        #pdb.set_trace()
                    try:
                        dataType_column = row[3]
                        if row[7].value:
                            slug = row[7].value
                        else:
                            slug = convert_text_to_slug(str(row[1].value)[:50])
                            #slug = get_slug(slug, questionnaire.pk)
                            slug = get_slug(slug)

                        if row[5].value:
                            helpText = row[5].value
                        else:
                            helpText = ''

                        _tooltip = False

                        if row[6].value:
                            if str(row[6].value).lower() == 'yes':
                                _tooltip = True

                        #If has dependencies
                        if row[8].value:
                            try:
                                dependencies_list = row[8]
                                list_dep_aux = dependencies_list.value.split('|')
                                question_num_parent = str(_questions_rows.get(int(list_dep_aux[0])))

                                # print "###############"
                                # print str(row[0].row) + " dependencies_list: " + str(dependencies_list)
                                # print str(row[0].row) + " str(list_dep_aux[0]: " + str(int(list_dep_aux[0]))
                                # print str(row[0].row) + " question_num_parent: " + question_num_parent
                                # print str(row[0].row) + " _questions_rows: " + str(_questions_rows)
                                # print str(row[0].row) + " _choices_array: " + str(_choices_array)

                                index_aux = int(str(list_dep_aux[1]))-1
                                choice_parent_list = _choices_array.get(int(list_dep_aux[0]))
                                choice_parent = choice_parent_list[index_aux]
                                _checks = 'dependent=\"' + str(question_num_parent) + ',' + str(choice_parent) + '\"'
                            except:
                                raise

                        try:
                            questionNumber = qNumber.getNumber(level_number_column.value)
                            questionNumber = format_number(str(questionNumber))
                        except:
                            log += "\n%s - Error to create question number %s" % (type_Column.row, text_en)
                            writeLog(log)
                            raise

                        #print slug
                        #Create or load slug
                        slugs = Slugs.objects.filter(slug1=slug, description=text_en)
                        if len(slugs) <= 0:
                            slug_db = Slugs(slug1=slug, description=text_en)
                            slug_db.save()
                        else:
                            slug_db = slugs[0]

                        visible_default = False
                        if row[10].value:
                            if str(row[10].value).lower() == 'visible':
                                visible_default = True

                        question = Question(questionset=questionset, text_en=text_en, number=str(questionNumber),
                                            type=dataType_column.value, help_text=helpText, slug=slug, slug_fk=slug_db, stats=True,
                                            category=False, tooltip=_tooltip, checks=_checks, visible_default=visible_default)

                        log += '\n%s - Question created %s ' % (type_Column.row, question)

                        if not _debug:
                            question.save()

                        _questions_rows[type_Column.row] = str(questionNumber)

                        #if not _debug:
                            # TODO: I think we don't need this now, since question now has a slug foreign key
                        #    save_slug(question.slug,  question.text_en, question)

                        # slugs.append((questionslugs.slug,  question.text_en, question))
                        log += '\n%s - Question saved %s ' % (type_Column.row, question)
                        if dataType_column.value in ['choice', 'choice-freeform', 'choice-multiple', 'choice-multiple-freeform']:
                            _choices_array_aux = []
                            # Parse of values list
                            values_list = row[4]
                            if (values_list!=None and values_list.value!=None):
                                list_aux = values_list.value.split('|')
                                i = 1
                                for ch in list_aux:
                                    try:
                                        choice = Choice(question=question, sortid=i, text_en=ch, value=ch)
                                        log += '\n%s - Choice created %s ' % (type_Column.row, choice)
                                        if not _debug:
                                            choice.save()
                                        _choices_array_aux.append(ch)

                                        log += '\n%s - Choice saved %s ' % (type_Column.row, choice)
                                        i += 1
                                    except:
                                        log += "\n%s - Error to save Choice %s" % (type_Column.row, choice)
                                        writeLog(log)
                                        raise
                                _choices_array[type_Column.row] = _choices_array_aux

                        if dataType_column.value in ['choice-yesno', 'choice-yesnocomment',
                                                             'choice-yesnodontknow']:
                            _choices_array[type_Column.row] = ['yes', 'no', 'dontknow']
                    except:
                        log += "\n%s - Error to save question %s" % (type_Column.row, text_en)

                        writeLog(log)
                        raise

    except:
        log += '\nError to save questionsets and questions of the questionnaire %s ' % questionnaire
        writeLog(log)
        raise

    # for a in slugs:
    #     (_slug, _desc, question) = a
    #     # Write Slug
    #     slugsAux = Slugs()
    #     slugsAux.slug1 = _slug
    #     slugsAux.description = _desc
    #     slugsAux.question = question
    #     slugsAux.save()

    log += '\nQuestionnaire %s, questionsets, questions and choices created with success!! ' % questionnaire
    writeLog(log)
    # print log

    return render_to_response(template_name, {'import_questionnaire': True,
                              'request': request, 'breadcrumb': True}, RequestContext(request))
