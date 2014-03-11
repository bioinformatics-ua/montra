from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys
import re

quest_id = 49
#qsets = QuestionSet.objects.all()
slugs = []
questionaires = Questionnaire.objects.filter(id=49)
for quest in questionaires:
	id = quest.id
	obj = {"id":"questionaire_"+str(id)}
	print quest.id
	print quest.name
	
	qsets = QuestionSet.objects.filter(questionnaire=quest)
	for qs in qsets:
		questions = qs.questions();
		#print "QS: "+qs.help_text
		for q in questions:
			#print "-----> Q:"+q.help_text
			if not q.tooltip and len(q.help_text)>0:
				q.tooltip = True
				print "----> Set Tooltip: "+ str(q)
				q.save()
			if q.tooltip:
				print q

print "QUITTING"