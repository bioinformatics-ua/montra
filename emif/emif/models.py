

from django.contrib.auth.models import User
from django.db import models

from django.db.models.fields import * 
#from questionnaire.models import Subject

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


