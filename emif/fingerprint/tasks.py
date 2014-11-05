# -*- coding: utf-8 -*-

# Copyright (C) 2014 Ricardo Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo Ribeiro <ribeiro.r@ua.pt>
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


from __future__ import absolute_import

from celery import shared_task
import time

from searchengine.search_indexes import CoreEngine

from fingerprint.models import Fingerprint, FingerprintReturnedSimple, FingerprintReturnedAdvanced, Answer
from fingerprint.services import unindexFingerprint

from django.utils import timezone
from django.conf import settings

from datetime import timedelta

from django.contrib.auth.models import User

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from newsletter.models import Newsletter, Subscription, Article, Message, Submission

from django.contrib.comments import Comment
from population_characteristics.models import Characteristic

from django.template.loader import render_to_string

from fingerprint.models import FingerprintHead, AnswerChange

@shared_task
def anotateshowonresults(query_filtered, user, isadvanced, query_reference):
    # Operations
    print "start annotating database appearing on results"

    c = CoreEngine()
    results = c.search_fingerprint(query_filtered)
    for result in results:
        fingerprint_id = result['id']

        if not fingerprint_id.startswith("questionaire_"):
            try:
                fp = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)
                print "processing "+str(fp)

                if isadvanced:
                    fingerprintreturn = FingerprintReturnedAdvanced(fingerprint=fp, searcher=user, query_reference=query_reference)
                    fingerprintreturn.save()
                else:
                    fingerprintreturn = FingerprintReturnedSimple(fingerprint=fp, searcher=user, query_reference=query_reference)
                    fingerprintreturn.save()

            except Fingerprint.DoesNotExist:
                print fingerprint_id + ' doesnt exist on db'

    print "ends annotation of databases appearing on results"
    return 0

@periodic_task(run_every=crontab(minute=settings.NEWSLETTER_MIN, hour=settings.NEWSLETTER_HOUR, day_of_week=settings.NEWSLETTER_DAY))
def generate_newsmessages():
    # Operations
    print "start generating weekly newsletters messages"

    fingerprints = Fingerprint.valid()

    newsletters = Newsletter.objects.all().exclude(slug='emif-catalogue-newsletter')

    for fingerprint in fingerprints:
        try:
            newsletter = newsletters.get(slug=fingerprint.fingerprint_hash)

            report = generateWeekReport(fingerprint, newsletter)

            sendWeekReport(report, newsletter)

        except Newsletter.DoesNotExist:
            print "-- Error: Found hash not existent on newsletters: "+fingerprint.fingerprint_hash

    print "ends generation"
    return 0

def generateWeekReport(fingerprint, newsletter):

    returnable = {}

    latest_check = timezone.now() - timedelta(days=7)

    fh = FingerprintHead.objects.filter(fingerprint_id = fingerprint, date__gte = latest_check)

    if len(fh) == 0:
        returnable['db_changes'] = None
    else:
        returnable['db_changes'] = render_to_string('subscriptions/fingerprint_changes.html', {
                                        'changes': FingerprintHead.mergeChanges(fh),
                                        'fingerprint': fingerprint.fingerprint_hash
                                    })

    discussion = Comment.objects.filter(object_pk = fingerprint.id, submit_date__gte = latest_check)
    if len(discussion) == 0:
        returnable['discussion'] = None
    else:
        returnable['discussion'] = render_to_string('subscriptions/discussion_changes.html', {
                                        'discussions': discussion,
                                        'fingerprint': fingerprint.fingerprint_hash
                                    })

    characteristic = Characteristic.objects.filter(created_date__gte = latest_check).order_by('-created_date')
    if len(discussion) == 0:
        returnable['characteristic'] = None
    else:
        returnable['characteristic'] = render_to_string('subscriptions/pop_changes.html', {
                                        'pop': characteristic
                                    })

    return returnable

def sendWeekReport(report, newsletter):

    # if nothing changed, nothing to report, moving on.
    if report['db_changes'] == None and report['discussion'] != None and report['characteristic'] != None:
        return

    now = timezone.now()

    mess = Message(title=newsletter.title+" - Recent Changes - "+now.strftime("%Y-%m-%d %H:%M"),slug=newsletter.slug+'_'+now.strftime("%Y%m%d%H%M%S"), newsletter=newsletter)
    mess.save()

    if report['db_changes'] != None:
        art = Article(title="Changes on Database:", text=report['db_changes'], post=mess)
        art.save()

    if report['discussion'] != None:
        art2 = Article(title="New Discussion:", text=report['discussion'], post=mess)
        art2.save()

    if report['characteristic'] != None:
        art3 = Article(title="New Population Characteristic Data:", text=report['characteristic'], post=mess)
        art3.save()

    subm = Submission.from_message(mess)

    subm.prepared = True

    subm.save()


@shared_task
def calculateFillPercentage(fingerprint):
    fingerprint.updateFillPercentage()

@periodic_task(run_every=crontab(minute=0, hour=3))
def remove_orphans():
    # Operations
    print "start removing old orphans databases"

    time = timezone.now() - timedelta(days=1)

    fingers = Fingerprint.objects.filter(last_modification__lte = time)

    for finger in fingers:

        name = finger.findName()

        if name == 'Unnamed':
            print "-- Removing orphan "+str(finger.fingerprint_hash)
            finger.removed=True
            finger.save()
            unindexFingerprint(finger.fingerprint_hash)


    print "ends removing old orphans databases"
    return 0

