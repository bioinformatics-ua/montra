# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
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

from django.db import models
from django.contrib.auth.models import User

from django.db.models.fields import *

from docs_manager.models import Document

import json


class Characteristic(Document):
    def __str__(self):
        return str(self.id)

class Comments(models.Model):
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    fingerprint_id = models.CharField(max_length=255)
    chart_id = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    latest_date = models.DateTimeField(auto_now=True)
    document = models.ForeignKey(Characteristic, unique=False, blank=True, null=True)
    title = models.TextField()
    description = models.TextField()




    def __str__(self):
        s = "User: " + str(self.user) + "\n"
        s += "Fingerprint ID: " + self.fingerprint_id + "\n"
        s += "created date: " + str(self.created_date) + "\n"
        s += "latest date: " + str(self.latest_date)+ "\n"
        s += "document: " + str(self.document)+ "\n"
        s += "title: " + self.title+ "\n"
        s += "description: " + self.description+ "\n"
        return s
