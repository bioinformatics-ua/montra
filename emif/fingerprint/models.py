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

class Fingerprint(models.Model):
  fingerprint_hash =  models.CharField(max_length=255, unique=True, blank=False, null=False)
  description = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(600)])
  questionnaire = models.ForeignKey(Questionnaire, null=True)

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
        self.name = ''
        self.date = ''
        self.date_modification = ''
        self.institution = ''
        self.location = ''
        self.email_contact = ''
        self.number_patients = ''
        self.ttype = ''
        self.type_name = ''
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

        self. __extract_summary_answers()

    """ This function fill the values. Extract from the Answer table
    """
    def __extract_summary_answers(self):
        
        pass#Answer.objects.filter(fingerprint_hash=self.id).filter(question.slug_fk.slug1__in=static_slugs)


