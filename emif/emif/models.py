# -*- coding: utf-8 -*-

# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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
#

from django.contrib.auth.models import User
from django.db import models

from django.db.models.fields import *
#from questionnaire.models import Subject
#
from django import forms

from fingerprint.models import Fingerprint

from django.dispatch import receiver
from userena.signals import signup_complete

from searchengine.search_indexes import CoreEngine

class QueryLog(models.Model):
    id = AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    query = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    latest_date = models.DateTimeField(auto_now=True)

class Log(models.Model):
    description = models.TextField()
    created_date = models.DateField()
    latest_date = models.DateField()

class SharePending(models.Model):
    id = AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, blank=True, null=True, related_name='user_invited')
    user_invite = models.ForeignKey(User,related_name='user_that_invites', unique=False, blank=True, null=True)
    db_id = models.TextField()
    activation_code = models.TextField()
    pending = models.BooleanField()

class InvitePending(models.Model):
    fingerprint = models.ForeignKey(Fingerprint)
    email = models.TextField()

class City(models.Model):
    id = AutoField(primary_key=True)
    name = models.TextField()
    lat = models.FloatField()
    long = models.FloatField()
    
class AdvancedQuery(models.Model):
    id = AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, blank=False, null=False)
    name = models.TextField(unique=True)
    serialized_query_hash = models.TextField(unique=False) #only unique for each user, not unique between users
    serialized_query = models.TextField(unique=False)
    date = models.DateTimeField(auto_now=True)
    qid = models.IntegerField(unique=False, blank=False, null=False)
    
class AdvancedQueryAnswer(models.Model):
    id = AutoField(primary_key=True)
    refquery = models.ForeignKey('AdvancedQuery')
    question = models.TextField(unique=False)
    answer = models.TextField(unique=False)
    
class ContactForm(forms.Form):
    name = forms.CharField(label='Name')
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'cols': 30, 'rows': 10, 'class': 'span6'}))
    topic = forms.CharField()

@receiver(signup_complete)
def add_invited(user, sender, **kwargs):

    sps = InvitePending.objects.filter(email=user.email)
    
    c = CoreEngine()
    
    for sp in sps:
        runcode = sp.fingerprint.fingerprint_hash

        # This will change on dev branch, but since i must do it on master, i have to do it on the searchengine and then change
        results = c.search_fingerprint("id:" + runcode)

        for result in results:
            old_users = ""
            d = result
            try:
                old_users = d['user_t']
            except KeyError:
                pass

            d['user_t']  = old_users+" \\ "+user.username

            del d['_version_']

            c.index_fingerprint_as_json(d)

            break


    print "Added invited user databases to+"+str(user.email)+"!"

