# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

def q_5_02_04():

	desiredQN = "5.02.04"


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
		q.text_en = "h2. Others"
		q.type = "choice-yesnodontknow"
		q.help_text = "Specify each criteria in a separate line."
		q.slug = "exclusion_criteria_other_5_02_04"
		q.checks = ""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Inclusion_/_Exclusion_Criteria")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"


def q_7_03_10():

	desiredQN = "7.03.10"


	def getQuestionObj(id):
		arr = Question.objects.filter(questionset=id, number=desiredQN)
		for x in arr:
			print "TAKE CARE: it has the question, it means that a overwriten will take place"
			print x.number
			return x

		return Question()

	def create_question(qset):
		#Create Question;
		q = getQuestionObj(qset.id)
		q.questionset = qset
		q.number = desiredQN
		q.text_en = "h2. Other major somatic disorders"
		q.type = "choice-multiple"
		q.help_text = "Specify each criteria in a separate line."
		q.slug = "Other_major_somatic_disorders_7_03_10"
		q.checks = ""

		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Clinical_Information")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		c1 = Choice()
		c1.question = question
		c1.sortid = "1"
		c1.value = "Routine"
		c1.text_en = "Routine"
		c1.save()
		c1 = Choice()
		c1.question = question
		c1.sortid = "2"
		c1.value = "Subgroup(Specify)"
		c1.text_en = "Subgroup(Specify)"
		c1.save()
		c1 = Choice()
		c1.question = question
		c1.sortid = "3"
		c1.value = "Not Collected"
		c1.text_en = "Not Collected"
		c1.save()

		print "Saved Question"
		updateSlug(question)

	print "QUITTING"

def q_8_02_12():

	desiredQN = "8.01.12"

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
		q.text_en = "h2. Specify any other scales"
		q.type = "open-textfield"
		q.help_text = "Specify each scale in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Subgroup, Items score available."
		q.slug = "Dementia_scales_other"
		q.checks = "dependent=\"8.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Dementia_rating_scales")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"


def q_16_01_01_10():

	desiredQN = "16.01.01.10"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_01_10"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"

def q_16_01_02_08():

	desiredQN = "16.01.02.08"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_02_08"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"

def q_16_01_02_08():

	desiredQN = "16.01.02.08"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_02_08"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"


def q_16_01_03_06():

	desiredQN = "16.01.03.06"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_03_06"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"



def q_16_01_04_06():

	desiredQN = "16.01.04.06"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_04_06"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"


def q_16_01_05_06():

	desiredQN = "16.01.05.06"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_05_06"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"


def q_16_01_06_05():

	desiredQN = "16.01.06.05"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_06_05"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"



def q_16_01_07_07():

	desiredQN = "16.01.07.07"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_07_07"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"


def q_16_01_08_04():

	desiredQN = "16.01.08.04"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Norms available, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_16_01_08_04"
		q.checks = "dependent=\"16.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Neuropsychological_Tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"




def q_9_01_06():

	desiredQN = "9.01.06"

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
		q.text_en = "h2. Specify any other scales"
		q.type = "open-textfield"
		q.help_text = "Specify each scale in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Subgroup, Items score available."
		q.slug = "Specify_any_other_tests_9_01_06"
		q.checks = "dependent=\"9.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Subjective_Cognitive_Impairment")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"




def q_11_01_10():

	desiredQN = "11.01.10"

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
		q.text_en = "h2. Specify any other scales"
		q.type = "open-textfield"
		q.help_text = "Specify each scale in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Subgroup, Items score available."
		q.slug = "Specify_any_other_tests_11_01_10"
		q.checks = "dependent=\"11.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Quality_of_Life")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"


def q_12_01_10():

	desiredQN = "12.01.10"

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
		q.text_en = "h2. Specify any other scales"
		q.type = "open-textfield"
		q.help_text = "Specify each scale in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Subgroup, Items score available."
		q.slug = "Specify_any_other_tests_12_01_10"
		q.checks = "dependent=\"12.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Caregiver")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"




def q_15_01_06():

	desiredQN = "15.01.06"

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
		q.text_en = "h2. Specify any other tests"
		q.type = "open-textfield"
		q.help_text = "Specify each test in a separate line. Try to follow the above questions when possible.<br>Example.  Collected, Version Cummings et al., 1994, Routine, If subgroup specify subgroup, Repeated collection (yes/no), If different from study characteristics then specify frequency and/or time interval"
		q.slug = "Specify_any_other_tests_15_01_06"
		q.checks = "dependent=\"15.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Cognitive_screening_tests")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"



def q_20_02_13():

	desiredQN = "20.01.02.13"

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
		q.text_en = "h2. Specify other assessements"
		q.type = "open-textfield"
		q.help_text = "Specify other analytics of interests separated by line."
		q.slug = "Specify_any_other_tests_20_01_02_13"
		q.checks = "dependent=\"20.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_CSF_collection")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"

# q_5_02_04()
# q_7_03_10()
# q_8_02_12()
# q_16_01_01_10()
# q_16_01_02_08()
# q_16_01_03_06()
# q_16_01_04_06()
# q_16_01_05_06()
# q_16_01_06_05()
# q_16_01_07_07()
# q_16_01_08_04()
# q_9_01_06()
# q_11_01_10()
# q_12_01_10()
# q_15_01_06()
# q_20_02_13()

#18.01.08
def q_18_01_08():

	desiredQN = "18.01.08"

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
		q.text_en = "h2. Specify any others"
		q.type = "open-textfield"
		q.help_text = "Specify each examination in a separate line. Try to follow the above questions when possible.<br>Example.  Blood Pressure, Subgroup in participants with plasma and CSF, Repeated collection (more than once)."
		q.slug = "Specify_any_other_examinations_18_01_08"
		q.checks = "dependent=\"18.01,yes\""
		return q

	def updateSlug(qs):
		arr = Slugs.objects.filter(question=qs)
		if len(arr) == 0:
			x = Slugs()
			x.question = qs
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
			return
		for x in arr:
			x.slug1 = qs.slug
			x.description = qs.text
			print x
			x.save()
		return


	qsets = QuestionSet.objects.filter(heading="adcohort_Physical_Examination")
	print qsets
	print len(qsets)
	for qs in qsets:
	 	print "iterate questions"
	 	print qs
	 	question = create_question(qs)
		question.save()
		print "Saved Question"
		updateSlug(question)

	print "QUITTING"

q_18_01_08()
