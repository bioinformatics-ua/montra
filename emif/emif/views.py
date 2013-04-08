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

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.urlresolvers import *
from questionnaire.models import *
from questionnaire.parsers import *

from questionnaire.views import *
from questionnaire.models import *

import md5
import random


def index(request, template_name='index.html'):
    return render(request, template_name, {'request': request})

def quick_search(request, template_name='quick_search.html'):
    return render(request, template_name, {'request': request})

def results(request, template_name='results.html'):
    return render(request, template_name, {'request': request})

def results_diff(request, template_name='results_diff.html'):
    return render(request, template_name, {'request': request})

def advanced_search(request, questionnaire_id ):
    #return render(request, template_name, {'request': request})
    print questionnaire_id
    return show_full_questionnaire(request, questionnaire_id)

# Documentation 
def docs_api(request, template_name='docs/api.html'):
    return render(request, template_name, {'request': request})

def databases(request, template_name='databases.html'):

    # Get the list of databases for a specific user

    return render(request, template_name, {'request': request})


def get_questionsets_list(runinfo):
    # Get questionnaire
    current = runinfo.questionset
    sets = current.questionnaire.questionsets()
    return sets

def show_full_questionnaire(request, runinfo, errors={}):
    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """
    print "in show_full_questionnaire - head"
    r = assure_authenticated_or_redirect(request)
    print "in show_full_questionnaire - head2"
    #if r:
    #    return r
    questionnaire_id = runinfo
    qu = get_object_or_404(Questionnaire, id=questionnaire_id)
    print "in show_full_questionnaire - head3"
    print qu.questionsets().__class__.__name__
    if isinstance(qu.questionsets(), (list, tuple)):
        print "is list or tuple"
    else:
        print "is list or tuple - not"
    #qs = qu.questionsets()
    qs = qu.questionsets()[0]
    print "in show_full_questionnaire - head3.5"
    user = request.user
    print "in show_full_questionnaire - head3.6"
    su = Subject.objects.filter(user=user)
    print "in show_full_questionnaire - head3.7"
    if su:
        su = su[0]
        print "in show_full_questionnaire - head5"
    else:
        su = Subject(user=user,
                     first_name=user.first_name,
                     last_name=user.last_name,
                     email=user.email,
                     state='active')
        print "in show_full_questionnaire - head4"
        su.save()
    print "in show_full_questionnaire"
    hash = md5.new()
    hash.update("".join(map(lambda i: chr(random.randint(0, 255)), range(16))))
    hash.update(settings.SECRET_KEY)
    key = hash.hexdigest()
    run = RunInfo(subject=su, random=key, runid=key, questionset=qs)
    run.save()
    questionsets = run.questionset.questionnaire.questionsets()

    for qs in questionsets:
        questions = qs.questions()
        print qs.text
        for q in questions:
            print q

    print questions
    print reverse('questionaries_with_sets', kwargs={'runcode': key})

    return HttpResponseRedirect(reverse('questionaries_with_sets', kwargs={'runcode': key}))

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
                args=[ runinfo.random, runinfo.questionset.sortid ])

    print "redirect to url: " + url
    return HttpResponseRedirect(url)

@transaction.commit_on_success
def questionaries_with_sets(request, runcode=None, qs=None):
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
            print HttpResponseRedirect(reverse("questionaries_with_sets",args=[runcode,str(__qs)]))
            return HttpResponseRedirect(reverse("questionaries_with_sets",args=[runcode, str(__qs)]))

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
            print "runinfor.qs.sortid" + str( runinfo.questionset.sortid)
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
        items.append( (u'question_%s_Trigger953' % x.number, None) )

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
            if(len(answer) == 2):
                ans['ANSWER'] = value
            elif(len(answer) == 3):
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
            depon = cd.get('requiredif',None) or cd.get('dependent',None)
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

    questionset_done.send(sender=None,runinfo=runinfo,questionset=questionset)

    next = questionset.next()
    while next and not questionset_satisfies_checks(next, runinfo):
        next = next.next()
    runinfo.questionset = next
    runinfo.save()

    if next is None: # we are finished
        return finish_questionnaire(runinfo, questionnaire)

    transaction.commit()
    return redirect_to_qs(runinfo)

def show_fingerprint_page(request, runinfo, errors={}):
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
    for k,v in cookiedict.items():
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
            'template' : 'questionnaire/%s.html' % (Type),
            'qnum' : _qnum,
            'qalpha' : _qalpha,
            'qtype' : Type,
            'qnum_class' : (_qnum % 2 == 0) and " qeven" or " qodd",
            'qalpha_class' : _qalpha and (ord(_qalpha[-1]) % 2 \
                                          and ' alodd' or ' aleven') or '',
        }
        
        # substitute answer texts
        substitute_answer(qvalues, question)

        # add javascript dependency checks
        cd = question.getcheckdict()
        depon = cd.get('requiredif',None) or cd.get('dependent',None)
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
                
        qlist.append( (question, qdict) )
    
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
        for k,v in request.POST.items():
            if k.startswith("question_"):
                s = k.split("_")
                if len(s) == 4:
                    qvalues[s[1]+'_'+v] = '1' # evaluates true in JS
                elif len(s) == 3 and s[2] == 'comment':
                    qvalues[s[1]+'_'+s[2]] = v
                else:
                    qvalues[s[1]] = v
    errors = {}
    r = r2r("advanced_search.html", request,
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




