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
from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys
import re

import pysolr
import csv

from django.conf import settings

BLACKLIST = ["If_yes_:_repeated_measurements",
	"If_yes_:_repeated_measurements",
	"comment_question_How_would_you_characterize_your_database",
	"comment_question_if_is_a_disease_or_event_specific_registry" ]

table = []
cr = csv.reader(open("/tmp/output.csv","rb"))
for row in cr:
    r = {}
    r["id"] = row[0]
    r["slug1"] = row[1]
    r["description"] = row[2]
    r["question"] = row[3]
    table.append(r)

def search_in_table(t, value, field="slug1"):
	for r in t:
		if r[field] == value:
			return r
	return None

solr = pysolr.Solr('http://' + settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
start=0
rows=100000000
fl='*_t, id'

def find_doc_by_id(id):
	res = solr.search("id:"+str(id),**{
                'rows': rows,
                'start': start,
                'fl': "*"
            })
	for r in res:
		return r
	return None


def search_questionaire():
	query="*:*"
	results = solr.search(query,**{
                'rows': rows,
                'start': start,
                'fl': fl
            })
	return results

def check_mismatches(results):
	l = []
	docList = []
	for res in results:
		d = {}
		d["doc"] = res
		d["wrong_slugs"] = []
		for slug in res:
			slugs = Slugs.objects.filter(slug1=slug[:-2])
			#print slug[:-2]
			if len(slugs) == 0:
				#print "FUUUUUUUU!!!!!!"
				d["wrong_slugs"].append(slug[:-2])
				if slug[:-2] not in l:
					l.append(slug[:-2])
		if len(d["wrong_slugs"]) > 0:
			docList.append(d)
	return (l, docList)

def check_same(value, fl="id"):
	if fl == "id":
		slugs = Slugs.objects.filter(id=value)
	else:
		slugs = Slugs.objects.filter(question=value)

	#print slug[:-2]
	return len(slugs)

def compute_new_slug(oldslug):
	if oldslug:
		slugs = Slugs.objects.filter(id=oldslug["id"])
		for s in slugs:
			return s
	return None


def delete_entry(doc, oldSlug):
	del doc[oldSlug+"_t"]


def replace_entry(doc, oldSlug, newSlug):
	k = newSlug.slug1+"_t"
	doc[k] = doc[oldSlug+"_t"]
	delete_entry(doc, oldSlug)


results = search_questionaire()
(myL, fdocs) = check_mismatches(results)

print "### REPORT - Missmatched Slugs ###"
for s in myL:
	print s

print "Number Of Missmatched Slugs: "+ str(len(myL))
print "##################################"

i = 0
j=0
for s in myL:
	r = search_in_table(table, s)
	if r:
		#print s + " , " + r["slug1"] + " "+str(r["id"]) +", "+ str(r["question"]), ", "+ str(check_same(r["id"])), ", "+ str(check_same(r["question"]))
		i = i +1
		if check_same(r["id"], fl="id") == 1:
			j = j+1

print "Number of Unrecoverable Slugs:" + str(len(myL) - i)

print "Number of Unrecoverable Slugs:" + str(len(myL) - j)


## Pop new Slug List
newSlugDB = {}
for s in myL:
	newSlug = compute_new_slug(search_in_table(table, s))
	if newSlug:
		newSlugDB[s] = newSlug


print "### REPORT - Replacement Table ###"
for ss in newSlugDB:
	print "OLD: "+ss+" NEW:"+newSlugDB[ss].slug1

print "Number of Replacement Slugs" + str( len(newSlugDB))


replaced_slugs = 0
toreplace_slugs = 0
docToAdd = []
for reg in fdocs:
	doc = find_doc_by_id(reg["doc"]["id"])
	docToAdd.append(doc)
	for slug in BLACKLIST:
		if slug in doc:
			delete_entry(doc, slug)
	for oldSlug in reg["wrong_slugs"]:
		if oldSlug in newSlugDB:
			if newSlugDB[oldSlug] in doc:
				#print "REPLACED SLUG"
				replaced_slugs = replaced_slugs +1
				delete_entry(doc, oldSlug)
			else:
				toreplace_slugs = toreplace_slugs +1
				replace_entry(doc, oldSlug, newSlugDB[oldSlug])


print "Replaced Slugs: "+str(toreplace_slugs)
print "Allready Replaced Slugs: "+str(replaced_slugs)

solr.add(docToAdd)
solr.optimize()


print "QUITTING"
