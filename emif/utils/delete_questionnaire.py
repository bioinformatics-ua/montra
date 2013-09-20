from questionnaire.models import *
from django.shortcuts import render_to_response, get_object_or_404

qu = get_object_or_404(Questionnaire, id=7)



qsets = qu.questionsets()

for qs in qsets:
	print "iterate questions"
	expected = qs.questions()
	
	for q in expected:
		print "iterate choices"
		print q.choices
		try:
			for c in q.choices:
				c.delete()
		except:
			pass
		q.delete()
	qs.delete()

qu.delete()
