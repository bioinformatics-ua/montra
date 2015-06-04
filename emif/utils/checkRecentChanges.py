from questionnaire.models import Question
from fingerprint.models import Answer, AnswerChange

def checkRecentChanges():

    qsts = Question.objects.all()

    counter = 0
    empty_count = 0

    def arrayWithoutComms(l):
        tmp = []
        comms = 0
        nocomms = 0
        for elem in l:
            if not '{' in elem:
                tmp.append(elem)
                nocomms+=1
            else:
                comms+=1

        return (tmp, comms, nocomms)

    for q in qsts:
        if q.type in ['choice-multiple', 'choice-multiple-freeform-options']:
            ans = Answer.objects.filter(question=q)

            for a in ans:
                achanges = AnswerChange.objects.filter(answer=a).order_by('-revision_head__date')
                if(achanges.count() > 0):
                    lu = achanges[0]

                    if lu.old_value and len(lu.old_value) > 1:
                        if lu.old_value != lu.new_value and '{' in lu.old_value:
                            prev_opts = lu.old_value.split('#')
                            new_opts = []
                            try:
                                new_opts = lu.new_value.split('#')
                            except:
                                new_opts = []

                            if len(prev_opts) > len(new_opts):

                                (old_nocom, old_comms, old_nocomms) = arrayWithoutComms(prev_opts)
                                (new_nocom, new_comms, new_nocomms) = arrayWithoutComms(new_opts)

                                if old_comms > 0 and new_comms == 0:
                                    counter+=1
                                    print " Possible data losses for question %s - %s - %r" % (q.number, q.questionset.questionnaire.name, a.fingerprint_id)

                                    print "Old: %s" %lu.old_value
                                    print "New: %s" %lu.new_value
                                    print "--"
                                    if lu.new_value == None or lu.new_value == '':
                                        empty_count+=1

    print "--"
    print "Found %d possible data losses" % counter
    print "High risk one's are %d (got empty)" % empty_count
    raise Exception('PAra')

checkRecentChanges()
