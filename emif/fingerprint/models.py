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

from description import fingerprint_description_slugs

class Fingerprint(models.Model):
  fingerprint_hash =  models.CharField(max_length=255, unique=True, blank=False, null=False)
  description = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(600)])
  questionnaire = models.ForeignKey(Questionnaire, null=True)
  removed = models.BooleanField(default=False, help_text="Remove logically the fingerprint")
  
  def __unicode__(self):
    return self.fingerprint_hash


"""
Answer of the Fingerprint 
"""
class Answer(models.Model):

    question = models.ForeignKey(Question)
    data = models.TextField() # Structure question 
    comment = models.TextField() # Comment
    fingerprint_id = models.ForeignKey(Fingerprint)

"""
This class wraps the Description of the Fingerprint.
It will be used to list fingerprints, for instance.
It is useful to centralized the code. 
Developed in first EMIF Hackthon. 
"""
class FingerprintDescription(object):

    def __init__(self, fingerprint_id):
        self.id = fingerprint_id
        self.type_name = ''
        self.type = ''
        
        #Fingerprint SnipetFields
        self.name = ''
        self.location = ''
        self.institution = ''
        self.created_date = ''
        self.date_modification = ''
        self.number_patients = ''
        
        
        self.email_contact = ''
        
        self.logo = ''
        self.last_activity = ''

        self.admin_name = ''
        self.admin_address = ''
        self.admin_email = ''
        self.admin_phone = ''

        self.scien_name = ''
        self.scien_address = ''
        self.scien_email = ''
        self.scien_phone = ''

        self.tec_name = ''
        self.tec_address = ''
        self.tec_email = ''
        self.tec_phone = ''

        self.__extract_summary_answers()

    def __str__(self):
        return str(self.id) + str(self.type_name) + str(self.type) + str(self.name)

    """ This function fill the values. Extract from the Answer table
    """
    def __extract_summary_answers(self):   
        fingerprint = Fingerprint.objects.get(fingerprint_hash=self.id);
        if fingerprint == None:
            raise u'Could not find fingerprint with hash: '+self.id
        self.type_name = fingerprint.questionnaire.name
        self.type = fingerprint.questionnaire.slug

        fingerprint_id = fingerprint.id
        fingerprint = None

        anss = Answer.objects.filter(fingerprint_id=fingerprint_id)#.filter(question__slug_fk__slug1__in=fingerprint_description_slugs).values("data", "question__slug_fk__slug1");
        print "ANS: "+str(len(anss))

        vmap = {}
        for a in anss:
            vmap[a["question__slug_fk__slug1"]] = a[data]

        self.name = vmap["database_name"]
        self.location = vmap["location"]
        self.institution = vmap["institution_name"]
        self.created_date = vmap["created"]
        #self.date_modification = vmap["location"]
        self.number_patients = vmap["number_active_patients_jan2012"]

'''
fingerprint_description_slugs = ["database_name", "location", 
            "institution_name", "contact_administrative", 
            "number_active_patients_jan2012", "created", "type" ]
'''
