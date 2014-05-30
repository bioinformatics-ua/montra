from questionnaire.models import Question
from django.db.models import Q

def convert():
    print "\n----------------------------------------------"
    print "Start converting url questions to url type"
    print "-----------------------------------------------"
    #Find all questions related with url
    questions = Question.objects.filter(Q(slug__icontains="website") | Q(slug__icontains="url"))
    for q in questions :
        #print q.slug
        if(q.type != 'url'):
            q.type='url'
            print "Found question with slug "+ q.slug + " mentioning url whose type isn't yet added, converting to url type."
            # Save changes to question
            q.save()
    print "-----------------------------------------------"
    print " End of url type conversion"
    print "-----------------------------------------------"


convert()   
