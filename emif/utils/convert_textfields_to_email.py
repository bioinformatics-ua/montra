from questionnaire.models import Question
def convert():

    print "\n----------------------------------------------"
    print "Start converting email questions to email type"
    print "-----------------------------------------------"
    #Find all questions related with email
    questions = Question.objects.filter(slug__icontains="email")
    for q in questions :
        if(q.type != 'email'):
            q.type='email'
            print "Found question with slug "+ q.slug + " mentioning email whose type isn't yet added, converting to email type."
            # Save changes to question
            q.save()
    print "-----------------------------------------------"
    print " End of email type conversion"
    print "-----------------------------------------------"


convert()   
