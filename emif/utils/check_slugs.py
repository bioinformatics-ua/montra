# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
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

from django.http import HttpResponse, HttpResponseRedirect

from questionnaire.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

from searchengine.models import *

from django.conf import settings

####
#### The goal of this script is to verify if anything from the solr is missing mapping in
#### the fingerprint template.
#### ...
####




import pysolr


solr = pysolr.Solr('http://' + settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
start=0
rows=100
fl=''


query="*:*"
results = solr.search(query,**{
                'rows': rows,
                'start': start,
                'fl': fl
            })
r_aux = None
docs = []
ignore_keys = ['type_t', '_version_', 'type_t', 'text_t', 'created_t',  'user_t', 'date_last_modification']
for r in results:
    if (r.keys()==None):
        continue
    to_swap = False
    for k in r.keys():
        if k in ignore_keys:
            continue
        qu = get_object_or_404(Questionnaire, slug=r['type_t'])
        slugs = Slugs.objects.filter(slug1=k[0:-2])
        if (len(slugs)==0):
            print "fingerprint id" + r['id']
            print "problem in " + k[0:-2]
