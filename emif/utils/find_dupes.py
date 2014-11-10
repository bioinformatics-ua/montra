from questionnaire.models import Question, Questionnaire
from searchengine.models import Slugs

def findDupes(q_slug):

    try:
        repeated_slugs = {}

        questionnaire = Questionnaire.objects.get(slug=q_slug)

        questions = Question.objects.filter(questionset__questionnaire=questionnaire).values_list('slug_fk__slug1', flat=True).distinct()

        for question in questions:
            qsts = Question.objects.filter(questionset__questionnaire=questionnaire, slug_fk__slug1=question)
            size = len(qsts)
            if size > 1:
                repeated_slugs[question] = qsts


        print "REPEATED SLUGS: "+str(len(repeated_slugs))
        for r in repeated_slugs:
            working_tag = r
            if r.endswith('_0'):
                working_tag = r[:-2]

            print working_tag
            for question in repeated_slugs[r][1:]:
                slug = next_free_slug(working_tag)
                if slug != None:
                    question.slug_fk = slug

                    print "Setting slug as "+str(slug.slug1)
                    question.slug = slug.slug1

                    question.save()

                else:
                    print "-- Error retrieving next free slug."

    except Questionnaire.DoesNotExist:
        print "Error retrieving questionnaire with slug "+str(q_slug)


def next_free_slug(slug_str):
    i=0
    worked = False
    # if we have 1000 slugs with the same name we have something wrong...
    while not worked and i < 1000:
        this_try = slug_str+'_'+str(i)

        slug = Slugs.objects.filter(slug1=this_try)

        if len(slug) == 0:
            worked=True

            slug = Slugs(slug1=this_try)
            slug.save()

            return slug

        else:
            i+=1

    return None


print "[ Taking a look at adcohort ]"
findDupes('adcohort')
print "[ Taking a look at observational data sources ]"
findDupes('observationaldatasources')
