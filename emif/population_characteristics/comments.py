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

from .models import * 

class Comments(models.Model):
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    fingerprint_id = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    latest_date = models.DateTimeField(auto_now=True)
    document = models.ForeignKey(Characteristic, unique=False, blank=True, null=True)
    title = models.TextField()
    description = models.TextField()

class CommentManager(object):


    def __init__(self, fingerprint_id):
        self.fingerprint_id=fingerprint_id


    def comment(self, chart_id, title, description, user):
        comments = Comments()
        comments.user = user
        comments.fingerprint_id = self.fingerprint_id
        jerboa_documents = Characteristic.objects.filter(fingerprint_id=fingerprint_id).order_by('latest_date')
        contains_population = len(jerboa_files)!=0
        comments.document = None
        comments.title = title 
        comments.description = description
        pass


