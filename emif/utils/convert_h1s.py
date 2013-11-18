from questionnaire.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

id_questionnaire = 49

qu = get_object_or_404(Questionnaire, id=id_questionnaire)


def get_number_of_h(number):
	return str(number.count('.'))

qsets = qu.questionsets()
for qs in qsets:
	print "iterate questions"
	q = Question.objects.filter(questionset=qs.id).order_by('number')
	print q.text
	q.text = "h" + get_number_of_h(q.number) + ". " + q.text
	print q.text

