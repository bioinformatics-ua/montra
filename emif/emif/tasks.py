# -*- coding: utf-8 -*-

# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
#          Ricardo Ribeiro       <ribeiro.r@ua.pt>
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

from celery import Celery

from celery.task.schedules import crontab
from celery.decorators import periodic_task

import json
from django.conf import settings

from docs_manager.storage_handler import *
from emif.models import QueryLog
from django.db.models import Count

import os

celery = Celery('emif', broker='amqp://guest@localhost//') #!

@periodic_task(run_every=crontab(minute=0, hour=2))
def generatesearchsuggestions():
    # Operations
    print "start generating free text suggestion file"

    outFile = os.path.join(os.path.abspath(PATH_STORE_FILES), "quicksearch/freetext.json")

    output = []

    unique_queries = QueryLog.objects.values("query").annotate(times_appeared=Count('query')).order_by('-times_appeared')

    for query in unique_queries:   
        if "type_t:" not in query['query']:
            #print str(query['query']) + ": " + str(query['times_appeared'])
            output.append({"query": query['query'], "count": query['times_appeared']})

    with open(outFile, 'w') as outfile:
        json.dump(output, outfile, sort_keys=True,indent=4, separators=(',', ': '))
        
    print "end generating free text suggestion file"
    return 0