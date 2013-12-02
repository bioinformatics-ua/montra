from questionnaire.models import *
from searchengine.models import * 
from django.shortcuts import render_to_response, get_object_or_404
import sys

id_questionnaire = 1

qu = get_object_or_404(Questionnaire, id=id_questionnaire)


def get_number_of_h(number):
	return str(number.count('.'))

qsets = qu.questionsets()
for qs in qsets:
	print "iterate questions"
	questions = qs.questions()
	for q in questions:
		print q
		print q.text
		t = q.text
		q.text_en = "h" + get_number_of_h(q.number) + ". " + t


		print q.text
		q.save()
		slugs = Slugs.objects.filter(question=q.pk)
		for s in slugs:
			s.description = q.text 
			s.save()

