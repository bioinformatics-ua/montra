from questionnaire.models import *
from questionnaire import QuestionChoices

from searchengine.search_indexes import CoreEngine

from datetime import datetime

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
    suffix = assert_suffix(new_type)


    if suffix == None:
        print '-- Invalid new type, process cancelled.'
        return False

    c = CoreEngine()
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

def assert_suffix(type):
    if type == "numeric":
        return "_d"
    elif type == "datepicker":
        return "_dt"
    # else
    return None 

def convert_value(value, type):
    if type == "numeric":
        try:
            # remove separators if they exist on representation
            value = re.sub("[']", "", value)
            # replace usual mistake , to .
            value = re.sub("[,]", ".", value)
            value = float(value)
            return value
        except ValueError:
            pass            

    elif type == "datepicker":
        date = value
        try:
            # First we try converting to normalized format, yyyy-mm-dd
            date = datetime.strptime(value, "%Y-%m-%d")
            return date
        except ValueError:
            pass

        try:
            # We try yyyy/mm/dd
            date = datetime.strptime(value, "%Y/%m/%d")
            return date
        except ValueError:
            pass

        try:
            # We try just the year, yyyy
            date = datetime.strptime(value, "%Y")
            return date
        except ValueError:
            pass

    return None     

def convert(type):
    # do stuff
    fields = findFieldsOnSlugs(type)

    if len(fields) > 0:
        convertFieldsOnSolr(fields, type)

convert("datepicker")
