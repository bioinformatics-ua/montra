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

# There are three types of plugins:
class Plugin(models.Model):
    GLOBAL      = 0
    DATABASE    = 1
    THIRD_PARTY = 2

    TYPES = [
                (GLOBAL,        'Global plugin, for the main dashboard'),
                (DATABASE,      'Database related plugin, for the database view'),
                (THIRD_PARTY,   'Third party full-fledged applications')
            ]

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    type = models.IntegerField(choices=TYPES, default=GLOBAL)
    owner= models.ForeignKey(User)
    create_date     = models.DateTimeField(auto_now_add=True)
    latest_update   = models.DateTimeField(auto_now=True)


    approved = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def create_date_repr(self):
        return self.create_date.strftime("%Y-%m-%d %H:%M:%S")

    def latest_update_repr(self):
        return self.latest_update.strftime("%Y-%m-%d %H:%M:%S")

    def type_repr(self):
        return dict(self.TYPES)[self.type]

    @staticmethod
    def all(owner=None):
        tmp = Plugin.objects.filter(removed = False)

        if owner != None:
            tmp = tmp.filter(owner=owner)

        return tmp

    # gets the file from the filesystem
    def getLatest(self):
        try:
            return PluginVersion.all(plugin=self)[:1]
        except PluginVersion.DoesNotExist:
            return None

    class Meta:
        ordering = ['-latest_update']

class PluginVersion(models.Model):
    plugin      = models.ForeignKey(Plugin)
    is_remote   = models.BooleanField(default=False)
    path        = models.CharField(max_length=2000)
    version     = models.IntegerField()

    removed     = models.BooleanField(default=False)

    @staticmethod
    def all(plugin=None):
        tmp = PluginVersion.objects.filter(removed=False)

        if plugin != None:
            tmp = tmp.filter(plugin=tmp)

        return tmp

    def __str__(self):
        return '%s : v.%r' % (self.plugin.name, self.version)

    class Meta:
        ordering = ['-version']
