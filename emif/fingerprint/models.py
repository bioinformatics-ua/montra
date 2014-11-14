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

from newsletter.models import Newsletter, Subscription

from searchengine.search_indexes import CoreEngine, generateFreeText, setProperFields, generateMltText

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

    def __eq__(self, other):
        return other.id == self.id

    def __str__(self):
        print id

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

    def setSubscription(self, user, value):
        try:
            subscription = FingerprintSubscription.objects.get(user = user, fingerprint = self)
            subscription.removed = not value
            subscription.save()

        except FingerprintSubscription.DoesNotExist:
            # we dont create in case its false it doesnt exist, pointless work
            if value:
                subscription = FingerprintSubscription(user = user, fingerprint = self)
                subscription.save()

    def findName(self):
        name = ""
        try:
            name_ans = Answer.objects.get(question__slug_fk__slug1='database_name', fingerprint_id=self)

            name = name_ans.data

        except Answer.DoesNotExist:
            name ="Unnamed"

        return name

    def unique_users(self):
        users = set()

        users.add(self.owner)

        for share in self.shared.all():
            users.add(share)

        return users

    def unique_users_string(self):
        users = set()
        users.add(self.owner.username)
        for share in self.shared.all():
            users.add(share.username)

        users = list(users)
        users_string = users[0]

        for i in xrange(1, len(users)):
            users_string+= ' \\ ' + users[i]

        return users_string

    # GET permissions model
    def getPermissions(self, question_set):

        if question_set == None:
            return None


        permissions = None
        try:
            permissions = QuestionSetPermissions.objects.get(fingerprint_id=self.fingerprint_hash, qs=question_set)

        except QuestionSetPermissions.DoesNotExist:
            print "Does not exist yet, creating a new permissions object."
            permissions = QuestionSetPermissions(fingerprint_id=self.fingerprint_hash, qs=question_set, visibility=0,
             allow_printing=True, allow_indexing=True, allow_exporting=True)
            permissions.save()

        except QuestionSetPermissions.MultipleObjectsReturned:
            print "Error retrieved several models for this questionset, its impossible, so something went very wrong."

        return permissions

    @staticmethod
    def index_all():
        indexes = []
        c = CoreEngine()

        fingerprints = Fingerprint.valid()

        c.deleteQuery('type_t:*')
        for fingerprint in fingerprints:
            print "-- Indexing fingerprint hash "+str(fingerprint.fingerprint_hash)
            indexes.append(fingerprint.indexFingerprint(batch_mode=True))

        print "-- Committing to solr"
        c.index_fingerprints(indexes)

    def indexFingerprint(self, batch_mode=False):
        def is_if_yes_no(question):
            return question.type in 'choice-yesno' or \
                    question.type in 'choice-yesnocomment' or \
                    question.type in 'choice-yesnodontknow'

        d = {}

        # Get parameters that are only on fingerprint
        # type_t
        d['id']=self.fingerprint_hash
        d['type_t'] = self.questionnaire.slug
        d['date_last_modification_t'] = self.last_modification.strftime('%Y-%m-%d %H:%M:%S.%f')
        d['created_t'] = self.created.strftime('%Y-%m-%d %H:%M:%S.%f')

        d['user_t'] = self.unique_users_string()

        d['percentage_d'] = self.fill

        adicional_text = ""


        # Add answers
        answers = Answer.objects.filter(fingerprint_id=self)

        for answer in answers:
            question = answer.question

            # We try to get permissions preferences for this question
            permissions = self.getPermissions(QuestionSet.objects.get(id=question.questionset.id))

            slug = question.slug_fk.slug1

            if permissions.allow_indexing or slug == 'database_name':
                setProperFields(d, question, slug, answer.data)
                if is_if_yes_no(question) and 'yes' in answer.data:
                    adicional_text += question.text+ " "
                if answer.comment != None:
                    d['comment_question_'+slug+'_t'] = answer.comment


        d['text_t']= generateFreeText(d) +  " " + adicional_text
        d['mlt_t'] = generateMltText(d)

        if batch_mode:
            return d
        else:
            print "-- Indexing unique fingerprint hash "+str(self.fingerprint_hash)
            c = CoreEngine()

            results = c.search_fingerprint("id:"+self.fingerprint_hash)
            if len(results) == 1:
                # Delete old entry if any
                c.delete(results.docs[0]['id'])

            c.index_fingerprint_as_json(d)




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

    def changes(self):
        return AnswerChange.objects.filter(revision_head=self)

    @staticmethod
    def mergeChanges(fingerprintheads):
        answermap = {}
        for head in fingerprintheads.order_by('date'):
            for change in head.changes():
                answermap[change.answer] = change

        return answermap.values()



class AnswerChange(models.Model):
    revision_head = models.ForeignKey(FingerprintHead)
    answer        = models.ForeignKey(Answer)
    old_value     = models.TextField(null=True)
    new_value     = models.TextField(null=True)
    old_comment   = models.TextField(null=True)
    new_comment   = models.TextField(null=True)

    def __str__(self):
        return "QUESTION: "+str(self.answer.question.number)

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

class FingerprintSubscription(models.Model):
    fingerprint     = models.ForeignKey(Fingerprint)
    user            = models.ForeignKey(User)
    date            = models.DateTimeField(auto_now_add=True)
    latest_update   = models.DateTimeField(auto_now=True)
    removed         = models.BooleanField(default=False)

    @staticmethod
    def active():
        return FingerprintSubscription.objects.filter(removed=False)

    def isSubscribed(self):
        return not self.removed

    def getNewsletter(self):
        newsl = None
        try:
            newsl = Newsletter.objects.get(slug=self.fingerprint.fingerprint_hash)

        except Newsletter.DoesNotExist:

            newsl = Newsletter( title=self.fingerprint.findName()+' Updates',
                            slug=self.fingerprint.fingerprint_hash,
                            email=settings.DEFAULT_FROM_EMAIL,
                            sender="Emif Catalogue")
            newsl.save()

        return newsl

    def setNewsletterSubs(self, new_status):
        newsl = self.getNewsletter()

        newsl_sub = None
        try:
            newsl_sub = Subscription.objects.get(user=self.user,  newsletter=newsl)
        except Subscription.DoesNotExist:
            newsl_sub = Subscription(user=self.user, newsletter = newsl)

        if(new_status):
            newsl_sub.subscribe()
        else:
            newsl_sub.unsubscribe()

        newsl_sub.save()
