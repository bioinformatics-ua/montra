

from django.contrib.auth.models import User
from django.db import models

from django.db.models.fields import * 
#from questionnaire.models import Subject
#
from django import forms


class QueryLog(models.Model):
	id = AutoField(primary_key=True)
	user =  models.ForeignKey(User, unique=False,  blank = True, null = True)
	query = models.TextField()
	created_date =  models.DateTimeField(auto_now_add=True)
	latest_date = models.DateTimeField(auto_now=True)


class Log(models.Model):
	description = models.TextField()
	created_date = models.DateField()
	latest_date = models.DateField()



class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    topic = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)