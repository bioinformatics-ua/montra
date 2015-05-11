from fingerprint.models import Answer
from questionnaire.models import Question

ans = Answer.objects.filter(data__contains='#Collected#Not Collected')
print "%d answers contain paradox answers" % (ans.count())
print "-----------------------------------"
for a in ans:
    print "%s - %s" % (a.question.number, a.fingerprint_id.fingerprint_hash)
print "-----------------------------------"
