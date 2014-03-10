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

from django.db import models

#from questionnaire.models import *
from django import forms

from django.core.mail import send_mail, BadHeaderError


class Slugs(models.Model):
	slug1 = models.CharField(max_length=1256)
	# TODO: delete 
	description = models.TextField()
	#question = models.ForeignKey(Question, help_text = u"The question that this is an answer to")

	def __unicode__(self):
         return self.slug1


class Nomenclature(models.Model):
	name = models.CharField(max_length=256)

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    topic = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)