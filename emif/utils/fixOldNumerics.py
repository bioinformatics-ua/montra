from questionnaire.models import Question
from fingerprint.models import Answer, Fingerprint
from fingerprint.services import indexFingerprint

def fix():
    q = Question.objects.get(id=5358)
    q.type='numeric'
    q.save()

    ans = Answer.objects.filter(question = q)
    for a in ans:
        a.data=a.data.replace('.', "'")
        a.save()
        indexFingerprint(a.fingerprint_id.fingerprint_hash)

fix()
