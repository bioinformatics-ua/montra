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
#qsets = QuestionSet.objects.all()
slugs = []
import pysolr

from django.conf import settings

solr = pysolr.Solr('http://' + settings.SOLR_HOST+ ':'+ settings.SOLR_PORT+settings.SOLR_PATH)
start=0
rows=10000
fl=''

res = solr.search("Publications_t:*",**{
                'rows': rows,
                'start': start,
                'fl': "*"
            })

for doc in res:
    p = doc["Publications_t"]

    p = p.replace("\\'","__________")
    p = p.replace("'","\"")
    p = p.replace("__________","'")

    print p
    print '------'
    doc["Publications_t"] = p

    if not (p.startswith("[") and p.endswith("]")):
        doc["Publications_t"] = "["+ p + "]"

    slugs.append(doc)


solr.add(slugs)

#solr.delete(q="id:questionaire_*")

#if len(wrongs)> 0:
#    for s in changes:
#        questions = Question.objects.filter(id=s["id"])
#        for q in questions:
#            q.number = s["number"]
#            q.save()
#            print "Saved " +str(q)

# for qs in qsets:
#      print "iterate questions"
#      print qs
#      question = create_question(qs)
#     question.save()
#     print "Saved Question"
#     updateSlug(question)

print "QUITTING"
