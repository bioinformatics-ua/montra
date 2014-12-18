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
from fingerprint.listings import get_databases_from_solr

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

from fingerprint.services import define_rows

def get_api_info(fingerprint_id):
    """This is an auxiliar method to get the API Info
    """
    result = {}


    results = FingerprintAPI.objects.filter(fingerprintID=fingerprint_id)
    result = {}
    for r in results:
        result[r.field] = r.value
    return result

def index(request, template_name='index_new.html'):
    referal = request.GET.get('ref', None)

    if request.user.is_authenticated():
        if referal != None:
            return HttpResponseRedirect(settings.BASE_URL + referal)
        else:
            return HttpResponseRedirect(settings.BASE_URL + 'wherenext')
    else:
        return render(request, template_name, {'request': request, 'referal': referal})

def about(request, template_name='about.html'):
    return render(request, template_name, {'request': request, 'breadcrumb': True})

def bootstrap_ie_compatibility(request, template_name='bootstrap_ie_compatibility.css'):
    return render(request, template_name, {'request': request, 'breadcrumb': False})

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
        if request.user.is_authenticated():
            form=ContactForm(initial={'name': request.user.get_full_name(),'email':request.user.email})

    return render(request, template_name, {'form': form, 'request': request, 'breadcrumb': True})

        # return render_to_response('feedback.html', {'form': ContactForm()},
        #     RequestContext(request))


def feedback_thankyou(request, template_name='feedback_thankyou.html'):
    return render(request, template_name, {'request': request, 'breadcrumb': True})

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
        notification=(fingerprint.findName()+" has been shared with you, please click here to activate it."), type=Notification.SYSTEM, href=link_activation)

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

    return activate_user(activation_code, request.user, context = request, template_name=template_name)


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
                    'fingerprint.listings.all_databases_user')
                return HttpResponseRedirect(reverse(redirect))

        interests = emifprofile.interests.all()
        if interests:
            return HttpResponseRedirect(reverse('fingerprint.listings.all_databases_user'))
    except:
        logging.warn("User has no emifprofile nor interests")
        return HttpResponseRedirect(reverse ('fingerprint.listings.all_databases'))
