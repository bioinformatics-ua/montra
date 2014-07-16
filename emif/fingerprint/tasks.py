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

from fingerprint.models import Fingerprint, FingerprintReturned

from django.contrib.auth.models import User

@shared_task
def anotateshowonresults(query_filtered, user):
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
                fingerprintreturn = FingerprintReturned(fingerprint=fp, searcher=user)
                fingerprintreturn.save()
                
            except Fingerprint.DoesNotExist:
                print fingerprint_id + ' doesnt exist on db'
        
    print "ends annotation of databases appearing on results"
    return fingerprint_id

