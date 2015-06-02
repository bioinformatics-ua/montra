from questionnaire.models import Question
from fingerprint.models import Answer, AnswerChange

def checkRecentChanges():

    qsts = Question.objects.all()

    counter = 0
    for q in qsts:
        if q.type in ['choice-multiple', 'choice-multiple-freeform-options']:
            ans = Answer.objects.filter(question=q)

            for a in ans:
                achanges = AnswerChange.objects.filter(answer=a).order_by('-revision_head__date')
                if(achanges.count() > 0):
                    lu = achanges[0]

                    if lu.old_value and len(lu.old_value) > 1:
                        if lu.old_value != lu.new_value and '{' in lu.old_value:
                            counter+=1
                            print " Possible data losses for question %s - %s" % (q.number, q.questionset.questionnaire.name)

                            print "Old: %s" %lu.old_value
                            print "New: %s" %lu.new_value
                            print "--"

    print "--"
    print "Found %d possible data losses" % counter
    raise Exception('PAra')

checkRecentChanges()
