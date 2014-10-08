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

from fingerprint.models import Fingerprint, FingerprintReturnedSimple, FingerprintReturnedAdvanced
from fingerprint.services import findName, unindexFingerprint

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User

from celery.task.schedules import crontab
from celery.decorators import periodic_task

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

@periodic_task(run_every=crontab(minute=0, hour=3))
def remove_orphans():
    # Operations
    print "start removing old orphans databases"

    time = timezone.now() - timedelta(days=1)

    fingers = Fingerprint.objects.filter(last_modification__lte = time)

    for finger in fingers:

        name = findName(finger)

        if name == 'Unnamed':
            print "-- Removing orphan "+str(finger.fingerprint_hash)
            finger.removed=True
            finger.save()
            unindexFingerprint(finger.fingerprint_hash)


    print "ends removing old orphans databases"
    return 0

