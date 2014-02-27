from questionnaire.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

desiredQN = "10.01.11"

def getQuestionObj(id):
	arr = Question.objects.filter(questionset=id, number=desiredQN)
	for x in arr:
		return x
	return Question()

def create_question(qset):
	#Create Question;
	q = getQuestionObj(qset.id)
	q.questionset = qset
	q.number = desiredQN


	# PLEASE HELP!!! CANT SET THE TEXT FIELD WHY!!	
	#q.text = "h2. Specify any other scales"
	
	q.type = "open-textfield"
	q.help_text = "Specify each scale in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Subgroup, Items score available."
	q.slug = "neuropsychiatric_scales_other"
	q.checks = "dependent=\"10.01,yes\""
	return q

qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychiatric_Scales")
print qsets
print len(qsets)
for qs in qsets:
 	print "iterate questions"
 	print qs
 	question = create_question(qs)
	question.save()
	print "Saved Question"

print "QUITTING"