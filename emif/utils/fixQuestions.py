from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys
import re

#qsets = QuestionSet.objects.all()

#Linha 6
questions = Question.objects.filter(id=7075)
q = questions[0]
choices = Choice.objects.filter(question=q, sortid=4).order_by('sortid')
if len(choices) == 0:
	nCh = Choice(question=q, sortid=4, 
		value="Repeated collection(Specify frequency and/or time interval)", 
		text_en="Repeated collection(Specify frequency and/or time interval)")
else:
	nCh = choices[0]
	nCh.text_en = "Repeated collection(Specify frequency and/or time interval)"
	nCh.save()

print q.choices()

#Linha X
questions = Question.objects.filter(id=6698)
q = questions[0]
q.type = "choice"
choices = Choice.objects.filter(question=q).order_by('sortid')
choiceArr = {}
choiceArr[1] = Choice(question=q, sortid=1, 
		value="Yes", 
		text_en="Yes")
choiceArr[2]=Choice(question=q, sortid=2, 
		value="No", 
		text_en="No")
choiceArr[3]=Choice(question=q, sortid=3, 
		value="Some", 
		text_en="Some")
choiceArr[4]=Choice(question=q, sortid=4, 
		value="Dont know", 
		text_en="Dont know")

for c in choices:
	choiceArr[c.sortid] = c

for x in xrange(1,5):
	nCh = choiceArr[x]
	nCh.save()

q.save()

print "QUITTING"

'''
class Choice(models.Model):
    __metaclass__ = TransMeta

    question = models.ForeignKey(Question)
    sortid = models.IntegerField()
    value = models.CharField(u"Short Value", max_length=1000)
    text = models.CharField(u"Choice Text", max_length=2000)

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.number, self.sortid, self.text)

    class Meta:
        translate = ('text',)