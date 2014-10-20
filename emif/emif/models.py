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

from django import forms


from questionnaire.models import Questionnaire

from fingerprint.models import Fingerprint

from fingerprint.services import indexFingerprint

from django.dispatch import receiver
from userena.signals import signup_complete

from searchengine.search_indexes import CoreEngine
from django.db.models.signals import post_save


from newsletter.models import Subscription, Newsletter

class QueryLog(models.Model):
    id = AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    query = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    latest_date = models.DateTimeField(auto_now=True)
    removed = models.BooleanField(default=False)

def querylog_created(sender, **kwargs):
    query = kwargs['instance']
    c = CoreEngine(core='suggestions')
    qdict = query.__dict__
    cleanqdict = {}
    cleanqdict['query'] = qdict['query'].strip().lower()
    cleanqdict['user_id'] = qdict['user_id']
    cleanqdict['id'] = qdict['id']
    cleanqdict['created_date'] = qdict['created_date']


    c.index_fingerprint(cleanqdict)

post_save.connect(querylog_created, sender=QueryLog)

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
    qid = models.ForeignKey(Questionnaire, unique=False, blank=False, null=False)
    removed = models.BooleanField(default=False)

    def has_representation(self):
        try:
            advrep = AdvancedQueryAnswer.objects.get(refquery=self, question="boolrelwidget-boolean-representation")

            return True

        except AdvancedQueryAnswer.DoesNotExist:
            return False



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

    ## Add to subscription list

    # get newsletter
    try:
        newsl = Newsletter.objects.get(slug='emif-catalogue-newsletter')

        # create subscription
        user_sub = Subscription(user=user,  newsletter=newsl)

        user_sub.subscribe()

        user_sub.save()

    except Newsletter.DoesNotExist:
        print "Problem registering new user to emif default newsletter"

    # add invited dbs if any
    sps = InvitePending.objects.filter(email=user.email)

    for sp in sps:

        fingerprint = sp.fingerprint

        fingerprint.save()

        fingerprint.shared.add(user)

        sp.delete()

        # must reindex, because databases lists come from solr, to update user_t
        indexFingerprint(fingerprint.fingerprint_hash)


    #print "Added invited user databases to+"+str(user.email)+"!"

