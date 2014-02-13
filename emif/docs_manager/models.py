# -*- coding: utf-8 -*-

# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
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

class Document(models.Model):
    id = AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    fingerprint_id = models.CharField()
    created_date = models.DateTimeField(auto_now_add=True)
    latest_date = models.DateTimeField(auto_now=True)
    revision = models.CharField()
    path = models.CharField()
    name = models.CharField()
    descriptoin = models.TextField()


    def get_name(self):
        pass

    def get_description(self):
        pass

    def store(self):
        pass

    def load(self):
        pass

