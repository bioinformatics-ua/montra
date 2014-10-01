from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.urlresolvers import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from emif.utils import QuestionGroup, ordered_dict

from questionnaire.models import QuestionSet, Question
from fingerprint.models import Answer, Fingerprint
from fingerprint.services import unique_users_string

from emif.utils import QuestionGroup, ordered_dict, Tag, clean_value
from questionnaire import Fingerprint_Summary

from fingerprint.services import *
from fingerprint.models import *

# since createqset estructure isnt tippically made to be used in a row, i decided to implement it
# separated since the purpose is different, and this way we try to reduce at a maximum the number of repeated procedures
def creatematrixqsets(db_type, fingerprints, qsets):
    ans = []

    # questions stay in memory, are the same for all fingerprints

    qs_mem = []
    name_question = None # source for the name of fingerprint
    # first we get the questionsets questions and titles in place
    q_list = ['Name']
    for qset in qsets:
        questions = qset.questions()
        qs_mem.extend(questions)

        for question in questions:
            if question.slug_fk.slug1 == "database_name":
                name_question = question
            q_list.append(question.text)

    for fingerprint in fingerprints:
        answers = Answer.objects.filter(fingerprint_id=fingerprint)

        a_list = []
        name = None
        for question in qs_mem:
            try:
                answer = answers.get(question=question)


                if question.type in Fingerprint_Summary:
                    a_list.append([Fingerprint_Summary[question.type](answer.data), question.type])
                else:
                    a_list.append([answer.data, question.type])
            except Answer.DoesNotExist:
                a_list.append("")

        name = "Unnamed"

        # if we dont get name_question naturally, we must take the time (this is a bother) to look for it...
        if name_question == None:
            try:
                n = answers.get(question__slug_fk__slug1='database_name')
                name_question = n.question
            except Answer.DoesNotExist:
                print "There's no database_name slugged answer for "+fingerprint.fingerprint_hash+" (maybe this questionnaire is a draft still)."

        if name_question != None:
            try:
                name_answers = answers.get(question=name_question)

                name = name_answers.data

            except Answer.DoesNotExist:
                pass

        ans.append((name, (a_list)))

    return (q_list, ans)

def createqsets(runcode, qsets=None, clean=True, highlights=None, getAnswers=True, 
    choosenqsets=None, fullmode=True, noprocessing=False, changeSearch=False):
    try:
        if fullmode:
            fingerprint = Fingerprint.objects.get(fingerprint_hash=runcode)
        else:
            fingerprint = runcode

        if qsets == None:
            qsets = ordered_dict()

        rHighlights = None
        qhighlights = None

        if highlights != None:
            if "results" in highlights and runcode in highlights["results"]:
                rHighlights = highlights["results"][runcode]
            if "questions" in highlights:
                qhighlights = highlights["questions"]

        fingerprint_ttype = fingerprint.questionnaire.pk

        db_owners = unique_users_string(fingerprint)

        qsets_query = None
        if choosenqsets != None:
            qsets_query = choosenqsets
        else:
            qsets_query = QuestionSet.objects.filter(questionnaire=fingerprint.questionnaire).order_by('sortid')

        answers = Answer.objects.filter(fingerprint_id=fingerprint)
        name = None
        for qset in qsets_query:
            if qset.sortid != 0 and qset.sortid != 99:
                (qsets, name) = handle_qset(fingerprint, clean, qsets, qset, answers, fingerprint_ttype, rHighlights, qhighlights, getAnswers, noprocessing=noprocessing, changeSearch=changeSearch)

        return (qsets, name, db_owners, fingerprint_ttype)

    except Fingerprint.DoesNotExist:
        print "-- Error on createqset: Fingerprint "+str(runcode)+" does not exist"

    # Something is really wrong if it gets here
    return HttpResponse('Something is wrong on creating qsets', 500)

# Creates a hollow shell that is similar to the one created by createqset, but doesnt have all the
# questions and answers (so is a lot faster to create), essentially a useful shell for pages that allow questionset selection
def createhollowqsets(questionnaire, qsets=None, highlights=None):

    if qsets == None:
        qsets = ordered_dict()

    rHighlights = None
    qhighlights = None

    if highlights != None:
        if "results" in highlights and runcode in highlights["results"]:
            rHighlights = highlights["results"][runcode]
        if "questions" in highlights:
            qhighlights = highlights["questions"]

    qsets_query = QuestionSet.objects.filter(questionnaire=questionnaire).order_by('sortid')

    for qset in qsets_query:
        if qset.sortid != 0 and qset.sortid != 99:
            question_group = QuestionGroup()
            question_group.sortid = qset.sortid
            question_group.qsid = qset.id

            qsets[qset.text] = question_group

    return qsets


def createqset(runcode, qsid, qsets=None, clean=True, highlights=None):
    qsid = int(qsid)
    #print "Got into createqset!!" + str(qsid)

    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=runcode)

        if qsets == None:
            qsets = ordered_dict()

        rHighlights = None
        qhighlights = None

        if highlights != None:
            if "results" in highlights and runcode in highlights["results"]:
                rHighlights = highlights["results"][runcode]
            if "questions" in highlights:
                qhighlights = highlights["questions"]

        fingerprint_ttype = fingerprint.questionnaire.pk

        db_owners = unique_users_string(fingerprint)

        try:
            qset = QuestionSet.objects.get(questionnaire=fingerprint.questionnaire, sortid=qsid)
            answers = Answer.objects.filter(fingerprint_id=fingerprint)

            (qsets, name) = handle_qset(fingerprint, clean, qsets, qset, answers, fingerprint_ttype, rHighlights, qhighlights)

        except QuestionSet.DoesNotExist:
            print "-- Error: The questionset you want does not exist"
        except QuestionSet.MultipleObjectsReturned:
            print "-- Error: Multiple objects returned, sortid ar supposed to be unique"

        return (qsets, name, db_owners, fingerprint_ttype)

    except Fingerprint.DoesNotExist:
        print "-- Error on createqset: Fingerprint "+str(runcode)+" does not exist"


    # Something is really wrong if it gets here
    return HttpResponse('Something is wrong on creating qset '+qsid, 500)

# this handles the generation of the tag - value for a single qset, given a questionset reference
def handle_qset(fingerprint, clean, qsets, qset, answers, fingerprint_ttype, rHighlights, qhighlights, getAnswers=True, noprocessing=False, changeSearch=False):
    name = ""
    question_group = QuestionGroup()
    question_group.sortid = qset.sortid
    question_group.qsid = qset.id
    question_group.highlights = False
    
    qsets[qset.text] = question_group
    # questions() already gives us questions ordered by number
    list_questions = qset.questions()

    for question in list_questions:
        t = Tag()
        t.id = question.id
        t.tag = question.text
        t.value = ""
        t.number = question.number
        t.ttype = question.type
        t.lastChange = None
        question_group.list_ordered_tags.append(t)

    qsets[qset.text] = question_group

    if getAnswers:
        for answer in answers:
            question = answer.question

            slug = question.slug_fk.slug1

            t = Tag()

            qs = None
            question_group = None
            q_number = None


            if question != None:
                t.id = question.id

                text = question.slug_fk.description
                qs = qset.text
                q_number = qs = question.number

                if qsets.has_key(qset.text):
                    # Add the Tag to the QuestionGroup
                    question_group = qsets[qset.text]

            else:
                text = (slug, answer.data)

            info = text
            t.tag = info

            if question_group != None and question_group.list_ordered_tags != None:
                try:
                    t = question_group.list_ordered_tags[question_group.list_ordered_tags.index(t)]
                except:
                    pass

            raw_value = str(answer.data.encode('utf-8'))
            value = clean_value(raw_value)

            qs_text = slug + "qs"
            id_text = "questionaire_"+str(fingerprint_ttype)
            if qhighlights != None and id_text in qhighlights and qs_text in qhighlights[id_text]:
                t.tag = qhighlights[id_text][qs_text][0].encode('utf-8')

            if answer.comment != None:
                t.comment = answer.comment

            if changeSearch:
                changes = AnswerChange.objects.filter(answer=answer).order_by('-id')

                if len(changes) == 0:
                    t.lastChange = answer.fingerprint_id.created
                else:
                    t.lastChange = changes[0].revision_head.date

            if clean:
                t.value = value.replace("#", " ")

                if rHighlights != None and slug+'_t' in rHighlights:
                    try:
                        qsets[question.questionset.text].highlights = True
                    except:
                        pass

                    t.value = rHighlights[slug+'_t'][0].encode('utf-8')
                    #if len(highlights["results"][k])>1:
                    #print t.value

                if not noprocessing:
                    if t.ttype in Fingerprint_Summary:
                        t.value = Fingerprint_Summary[t.ttype](raw_value)

            else:
                t.value = value

            if slug == "database_name":
                name = raw_value

            if question_group != None:
                try:
                    question_group.list_ordered_tags[question_group.list_ordered_tags.index(t)] = t
                except:
                    pass

    return (qsets, name)