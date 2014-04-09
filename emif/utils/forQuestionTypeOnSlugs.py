from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys

numericSlugs = ["number_active_patients_jan2012"]

for slug in numericSlugs:
	arr = Slugs.objects.filter(slug1=slug)
	print arr
	for s in arr:
		print "Slugging"
		s.question.type = "numeric"
		s.question.save()
		s.save()
		print s
		print "Saved Slug"

print "QUITTING"