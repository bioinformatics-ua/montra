from questionnaire.models import Question

qsts = Question.objects.filter(type='comment')

for qst in qsts:
    print qst
    qst.stats=False
    qst.category=True
    qst.save()
