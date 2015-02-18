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

from django import forms

class Slugs(models.Model):
    slug1 = models.CharField(max_length=1256, blank=False)
    # TODO: delete
    description = models.TextField()
    #question = models.ForeignKey(Question, help_text = u"The question that this is an answer to")

    def __unicode__(self):
        return self.slug1


class Nomenclature(models.Model):
    name = models.CharField(max_length=256)
