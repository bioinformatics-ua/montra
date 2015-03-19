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
from questionnaire import QuestionChoices

from searchengine.search_indexes import CoreEngine, convert_value, assert_suffix

# Find fields slugs of a certain type
def findFieldsOnSlugs(type):

    if type == None:

        print "Must specify a valid type to find fields for"

        return []

    fields = []
    questiontype_exists = False

    for qchoice, qdesc in QuestionChoices:
        print qchoice
        if qchoice.lower() == type.lower():
            questiontype_exists = True
            break

    if questiontype_exists == True:
        print "The question type is valid, looking for questions with this type."

        questions = Question.objects.all()

        for question in questions:
            if question.type.lower() == type.lower():
                fields.append(question.slug_fk)

        print "Found all questions of this type, "+str(len(fields))+" results."

    else:
        print "-- Error: The type " + type + " doesn't exist."

    return fields

# convert all the solr documents to have the list of fields with proper suffix
def convertFieldsOnSolr(fields, new_type):
    c = CoreEngine()

    suffix = assert_suffix(new_type)


    if suffix == None:
        print '-- Invalid new type, process cancelled.'
        return False

    documents = c.search_fingerprint("*:*")

    print "Started converting fields on all databases, number of databases: "+str(len(documents))

    for document in documents:
        doc = document
        del doc['_version_']

        for field in fields:
            try:
                value = doc[str(field)+'_t']

                value = convert_value(value, new_type)

                if value == None:
                    print "-- Couldn't convert field "+str(field)+" for database " + doc['id'] + ". "+str(doc[str(field)+'_t'])+" is not of type " + str(new_type)
                else:
                    doc[str(field)+suffix] = value

            except KeyError:
                print "-- "+str(doc['id'])+' doesn\'t have the field '+str(field)+', ignoring this field on this database.'

        c.delete(doc['id'])
        c.index_fingerprint_as_json(doc)

    print "Done converting fields on all databases"
    return True

def convert(type):
    # do stuff
    fields = findFieldsOnSlugs(type)

    if len(fields) > 0:
        convertFieldsOnSolr(fields, type)

convert("datepicker")
convert("numeric")
