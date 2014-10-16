from questionnaire.models import Question
from fingerprint.models import Answer, Fingerprint
from fingerprint.services import indexFingerprint

def fix():
    qs = Question.objects.filter(type='numeric')

    for q in qs:
        ans = Answer.objects.filter(question = q)
        for a in ans:
            a.data=a.data.replace('.', "'")
            a.save()
            indexFingerprint(a.fingerprint_id.fingerprint_hash)

fix()
