#qsets = QuestionSet.objects.all()
slugs = []
import pysolr

host1 = "localhost"
port1 = str(8983)

solr = pysolr.Solr('http://' +host1+ ':'+ port1+'/solr')
start=0
rows=10000
fl=''

res = solr.search("Publications_t:*",**{
                'rows': rows,
                'start': start,
                'fl': "*"
            })

for doc in res:
    p = doc["Publications_t"]

    p = p.replace("\\'","__________")
    p = p.replace("'","\"")
    p = p.replace("__________","'")

    print p
    print '------'
    doc["Publications_t"] = p
    
    if not (p.startswith("[") and p.endswith("]")):
        doc["Publications_t"] = "["+ p + "]"
    
    slugs.append(doc)


solr.add(slugs)

#solr.delete(q="id:questionaire_*")

#if len(wrongs)> 0:
#    for s in changes:
#        questions = Question.objects.filter(id=s["id"])
#        for q in questions:
#            q.number = s["number"]
#            q.save()
#            print "Saved " +str(q)

# for qs in qsets:
#      print "iterate questions"
#      print qs
#      question = create_question(qs)
#     question.save()
#     print "Saved Question"
#     updateSlug(question)

print "QUITTING"