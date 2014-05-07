from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys
import re

#####################################################################
###_55_V2.0_20131114_HELIAD	Hellenic Epidemiological and Longitudinal Investigation of Aging and Diet	Clinical information			31
###31_V1.0_20131114_AddNeuroMed	Innovative Medicines for Europe (Innomed)	Clinical information			20
#####################################################################
tempIDS = [7075, 6748, 6749, 6750, 6751]
for i in tempIDS:
	questions = Question.objects.filter(id=i)
	q = questions[0]
	choices = Choice.objects.filter(question=q, sortid=4).order_by('sortid')
	if len(choices) == 0:
		nCh = Choice(question=q, sortid=4, 
			value="Repeated collection(Specify frequency and/or time interval)", 
			text_en="Repeated collection(Specify frequency and/or time interval)")
		nCh.save()
	else:
		nCh = choices[0]
		nCh.text_en = "Repeated collection(Specify frequency and/or time interval)"
		nCh.save()

	print q.choices()

#########################################################################
###_55_V2.0_20131114_HELIAD	Hellenic Epidemiological and Longitudinal Investigation of Aging and Diet	Inclusion_exclusion			48	only one publication w/o a PubMed ID but with at least an author and title can be entered in a database
#########################################################################
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
############################################################################
###_52_V2.0_20131114_Athens	UNK	CSF collection			51-53	Initial answer "No", still Excel table came with follow-up question that only should appear with an initial "Yes" answer.
###_52_V2.0_20131114_Athens	UNK	CSF collection			53	Initial answer "No", following column cell should be empty. But it's not!
############################################################################
questions = Question.objects.filter(id=6964)
q = questions[0]
q.text_en = "h3. Use of ice during collection? Specify how long it was stored on ice between collection and storage."
q.save()

#############################################################################
###EMIF-AD Study Characteristics Data collection_45_V1.0_20140417_Memento	Memento	Number of Subjects			7	no entry for numbers of subjects older and younger than 65 years old
#############################################################################
def fix_question_6_01_01_0X():
	questions = Question.objects.filter(id=6704)
	q = questions[0]
	
	model_choices = Choice.objects.filter(question=q).order_by('sortid')
	if len(model_choices) == 0:
		return

	to_fix_questions = []
	questions = Question.objects.filter(id=6705)
	to_fix_questions.append(questions[0])
	questions = Question.objects.filter(id=6706)
	to_fix_questions.append(questions[0])
	
	for q in to_fix_questions:
		Choice.objects.filter(question=q).delete()
		for ch in model_choices:
			nChoice = Choice(question=q, sortid=ch.sortid, 
				value=ch.value, 
				text_en=ch.text_en)
			nChoice.save()

fix_question_6_01_01_0X()
#################################################
#EMIF-AD Study Characteristics Data collection_58_V2.1_20140417_Perugia2	Rete Geriatrica Alzheimer (Italian Geriatric Network)	Blood collection			33,34	no place to enter "don't know" in database
###################################################
tempIDS = [6899, 6900, 6901, 6902, 6903, 6905, 6906, 6907, 6908, 6909, 6910, 6911, 6913, 6914, 6915, 6916, 6917, 6918, 6919, 6921, 6922]
for i in tempIDS:
	questions = Question.objects.filter(id=i)
	q = questions[0]
	choices = Choice.objects.filter(question=q, sortid=3).order_by('sortid')
	if len(choices) == 0:
		nCh = Choice(question=q, sortid=3, 
			value="Do not know", 
			text_en="Do not know")
		nCh.save()
	else:
		nCh = choices[0]
		nCh.text_en = "Do not know"
		nCh.save()

	print q.choices()
###################################################

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
'''