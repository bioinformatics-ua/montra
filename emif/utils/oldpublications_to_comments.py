from questionnaire.models import Question, Questionnaire

from searchengine.search_indexes import CoreEngine
from fingerprint.models import Answer, Fingerprint
from fingerprint.services import indexFingerprint

def old_publications_to_comments():
    # ars, gepard, hsd csd lpd, ipci, maas, pedianet, thin
    greenlist = ['768185357ce7e4e0aeae6d2e69f6d7e0', '45b7ccb3aca47bc37f9bd82504f09b3b', 
    '52d4981701f0126d947014244744efea', '54d8384917b21fb7928ba72a1e72326b', '7b128593480b53409ac83c9582badbb7',
    '5d8f88d91f1dc3e2806d825f61260b76', '7a205644571c31bc50965c68d7565622']

    this_questionnaire=None
    try:
        this_questionnaire = Questionnaire.objects.get(slug="observationaldatasources")
    except Questionnaire.DoesNotExist:
        print "-- Cant find observational data sources questionnaire"
        return

    try:
        this_question = Question.objects.get(slug_fk__slug1 ='Publications', questionset__questionnaire=this_questionnaire)

        print "\n----------------------------------------------"
        print "Start looking through publications "
        print "-----------------------------------------------"
        #Find all questionnarie types
        c = CoreEngine()

        documents = c.search_fingerprint("type_t:observationaldatasources")

        for document in documents:
            if document['id'] not in greenlist:
                print " Processing id " + str(document.get('id'))

                publications_comment = document.get('list_of_peer_reviewed_papers_based_on_your_data_ba_t', "")

                try:
                    this_fingerprint = Fingerprint.objects.get(fingerprint_hash=document['id'])

                    try:
                        this_answer = Answer.objects.get(fingerprint_id=this_fingerprint, question=this_question)

                        print this_answer.comment

                        this_answer.comment = publications_comment

                        this_answer.save()

                    except Answer.DoesNotExist:
                        print "--- Answer does not exist, creating new answer."
                        print publications_comment
                        this_answer = Answer(question=this_question, data="", comment=publications_comment, fingerprint_id=this_fingerprint)

                        this_answer.save()

                    # after save must reindex to update solr too
                    #indexFingerprint(this_fingerprint.fingerprint_hash)


                except Fingerprint.DoesNotExist:
                    print "--- ERROR: Fingerprint with id " + str(document.get('id')) + 'does not exist'
        
        print "-----------------------------------------------"
        print " End"
        print "-----------------------------------------------"

    except Question.DoesNotExist:
        print "--- ERROR: Theres no question with slug Publications_t"

old_publications_to_comments()   
