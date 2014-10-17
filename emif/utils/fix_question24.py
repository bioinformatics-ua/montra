from questionnaire.models import Question, Choice

def fixQuestion():
    q = Question.objects.get(id=7045)
    if q.number == '24.01.02':
        q.type = 'choice-multiple'
        q.text_en = 'h2. Scanner (please specify each):'
        q.save()

        c = Choice.objects.filter(question=q)
        c.delete()

        options = ['Manufacturer', 'Model', 'Installation year', 'Software Version', 'Quality Control Method']
        i=1
        for option in options:
            new_choice = Choice(question=q, sortid=i, value=option, text_en=option)
            new_choice.save()
            i+=1

    else:
        print "-- ERROR: Question with id 7045 is not the question number 24.01.02"

fixQuestion()
