# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
#          Tiago Godinho
#          Ricardo Ribeiro
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


from django.db import models

from django.core.validators import MaxLengthValidator

from questionnaire.models import *
from django.contrib.auth.models import User

from description import fingerprint_description_slugs

class Database:
    id = ''
    name = ''
    date = ''
    date_modification = ''
    institution = ''
    location = ''
    email_contact = ''
    number_patients = ''
    ttype = ''
    type_name = ''
    logo = ''
    last_activity = ''

    admin_name = ''
    admin_address = ''
    admin_email = ''
    admin_phone = ''

    scien_name = ''
    scien_address = ''
    scien_email = ''
    scien_phone = ''

    tec_name = ''
    tec_address = ''
    tec_email = ''
    tec_phone = ''

    percentage = 0


class RequestMonkeyPatch(object):
    POST = {}

    GET = {}

    session = {}

    META = None

    COOKIES = None

    method = POST

    user = None

    is_secure = False
    path = "None"
    host = None
    def __init__(self):
        self.POST = {}

    def get_post(self):
        return self.POST

    def get_session(self):
        return self.session

    def set_session(self, session_params):
        self.session = session_params

    def set_user(self, user):
        self.user = user

    def set_meta(self, meta):
        self.META = meta

    def set_cookies(self, cookies):
        self.COOKIES = cookies

    def set_host(self, host):
        self.host = host

    # mock methods
    def is_secure(self):
        return False

    def get_host(self):
        return self.host

class Fingerprint(models.Model):
    fingerprint_hash =  models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(600)])
    questionnaire = models.ForeignKey(Questionnaire, null=True)

    last_modification = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey(User, related_name="fingerprint_owner_fk")
    shared = models.ManyToManyField(User, null=True, related_name="fingerprint_shared_fk")
    hits = models.IntegerField(default=0, help_text="Hit count for this fingerprint")
    removed = models.BooleanField(default=False, help_text="Remove logically the fingerprint")

    fill = models.FloatField(default=0, help_text="Database Questionset")

    def __unicode__(self):
        return self.fingerprint_hash

    # def get_answers(self):
    #     if answers:
    #         return self.answers

    #     answers = Answer.objects.filter(fingerprint_id=self.id)
    #     print "ANSEWRS: "+str(len(anss))
    #     return self.answers

    def __len__(self):
        return Answer.objects.filter(fingerprint_id=self.id).count()

    def __getitem__(self, key):
        #answers = self.get_answers()
        a = None
        try:
            a = Answer.objects.filter(fingerprint_id=self.id).filter(question__slug_fk__slug1=key).get()
        except Exception, e:
            raise IndexError

        if a == None:
            raise KeyError
        return a

    def __iter__(self):
        #answers = self.get_answers()
        anss = Answer.objects.filter(fingerprint_id=self.id).all()
        for a in anss:
            yield a

    def keys(self):
        keys = Answer.objects.filter(fingerprint_id=self.id).all().values_list("question__slug_fk__slug1", flat=True)
        return keys

    def iterkeys(self):
        for x in keys:
            yield x

    def __contains__(self, key):
        try:
            a = Answer.objects.filter(fingerprint_id=self.id).filter(question__slug_fk__slug1=key).get()
        except Exception, e:
            return False
        return a != None

    @staticmethod
    def valid():
        return Fingerprint.objects.filter(removed=False)

def FingerprintFromHash(hash):
    return Fingerprint.objects.get(fingerprint_hash=hash);

# def FingerprintFromHash():
#     return Fingerprint.objects.all();


"""
    Answer of the Fingerprint
"""
class Answer(models.Model):
    question = models.ForeignKey(Question)
    data = models.TextField() # Structure question
    comment = models.TextField(null=True) # Comment
    fingerprint_id = models.ForeignKey(Fingerprint)

    def get_slug():
        return question.slug_fk.slug1

    def __str__(self):
     return "ANSWER{id="+str(self.id)+", question_slug="+self.question.slug_fk.slug1+", data="+self.data+", comment="+str(self.comment)+"}"

'''
    Fingerprint answers tracked change - a simple revision system

        Each time a already existing fingerprint has answers modified, there's a new object
        from this model, and one answer change for each answer change
'''
class FingerprintHead(models.Model):
    fingerprint_id = models.ForeignKey(Fingerprint)
    revision       = models.IntegerField()
    date           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "FINGERPRINT_ID:"+str(self.fingerprint_id)+" REVISION: "+str(self.revision) + " DATE: "+ str(self.date)

class AnswerChange(models.Model):
    revision_head = models.ForeignKey(FingerprintHead)
    answer        = models.ForeignKey(Answer)
    old_value     = models.TextField(null=True)
    new_value     = models.TextField(null=True)
    old_comment   = models.TextField(null=True)
    new_comment   = models.TextField(null=True)

''' The idea is showing the number of times the db is returned over time
'''
class FingerprintReturnedSimple(models.Model):
    fingerprint = models.ForeignKey(Fingerprint)
    searcher    = models.ForeignKey(User)
    date        = models.DateTimeField(auto_now_add=True)
    query_reference = models.ForeignKey('emif.QueryLog')

class FingerprintReturnedAdvanced(models.Model):
    fingerprint = models.ForeignKey(Fingerprint)
    searcher    = models.ForeignKey(User)
    date        = models.DateTimeField(auto_now_add=True)
    query_reference = models.ForeignKey('emif.AdvancedQuery')

class AnswerRequest(models.Model):
    fingerprint = models.ForeignKey(Fingerprint)
    question    = models.ForeignKey(Question)
    requester   = models.ForeignKey(User)
    date        = models.DateTimeField(auto_now=True)
    removed     = models.BooleanField(default=False)

"""
This class wraps the Description of the Fingerprint.
It will be used to list fingerprints, for instance.
It is useful to centralized the code.
Developed in first EMIF Hackthon.
"""
class FingerprintDescriptor(object):
    static_attr = ["id", "date", "date_modification", "last_activity", "ttype", "type_name"]
    slug_dict = {"name":"database_name",
                    "institution" : 'institution_name',
                    "email_contact" : 'contact_administrative',
                    "number_patients" : 'number_active_patients_jan2012',
                    "logo" : 'upload-image',
            }
    observational_spec = {
        "admin_name" : 'institution_name',
        "admin_address" : 'Administrative_contact_address',
        "admin_email" : 'Administrative_contact_email',
        "admin_phone" : 'Administrative_contact_phone',

        "scien_name" : 'Scientific_contact_name',
        "scien_address" : 'Scientific_contact_address',
        "scien_email" : 'Scientific_contact_email',
        "scien_phone" : 'Scientific_contact_phone',

        "tec_name" : 'Technical_contact_/_data_manager_contact_name',
        "tec_address" : 'Technical_contact_/_data_manager_contact_address',
        "tec_email" : 'Technical_contact_/_data_manager_contact_email',
        "tec_phone" : 'Technical_contact_/_data_manager_contact_phone',
    }
    ad_spec = {
        "admin_name" : 'Administrative_Contact__AC___Name',
        "admin_address" : 'AC__Address',
        "admin_email" : 'AC__email',
        "admin_phone" : 'AC__phone',

        "scien_name" : 'Scientific_Contact__SC___Name',
        "scien_address" : 'SC__Address',
        "scien_email" : 'SC__email',
        "scien_phone" : 'SC__phone',

        "tec_name" : 'Technical_Contact_Data_manager__TC___Name',
        "tec_address" : 'TC__Address',
        "tec_email" : 'TC__email',
        "tec_phone" : 'TC__phone',
    }

    spec = ["location"]
    def __init__(self, fingerprint):
        self.obj = fingerprint

    def __getattr__(self, name):
        try:
            #print name
            if name in self.static_attr:
                return self.parse_static_args(name)
            elif name in self.slug_dict:
                return self.obj[self.slug_dict[name]].data
            elif name in self.spec:
                return self.parse_specific(name).data
            elif name in self.observational_spec:
                return self.parse_type_spec(name).data
        except Exception, e:
            pass
        return ""

    def parse_type_spec(self, name):
        if self.type_name == "Observational Data Sources":
            return self.obj[self.observational_spec[name]]
        elif "AD Cohort" in self.type_name:
            return self.obj[self.ad_spec[name]]
    def parse_static_args(self,name):
        print "FOUND STATIC ARG"
        if name == "id":
            print "FOUND ID"
            return self.obj.fingerprint_hash

        if name == "date":
            return self.obj.created

        if name == "date_last_modification" or name == "last_activity":
            return self.obj.last_modification

        if name == "ttype":
            return self.obj.questionnaire.slug

        if name == "type_name":
            return self.obj.questionnaire.name

    def parse_specific(self,name):
        if name == "location":
            if "city" in self.obj:
                return self.obj['city']
            if "location" in self.obj:
                return self.obj['location']
            if "PI:_Address" in self.obj:
                return self.obj['PI:_Address']
