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
from django.contrib.auth.models import Group, User

default_users = []

def addDeveloper():
    def addGroup(user, group):
        user.groups.add(group)
        user.save()
        pass

    developer = None
    try:
        developer = Group.objects.get(name='developers')

    except Group.DoesNotExist:
        developer = Group(name='developers')
        developer.save()

    for email in default_users:
        try:
            user = User.objects.get(email=email)

            addGroup(user, developer)

        except User.DoesNotExist:
            print "-- ERROR: Can't find user"+str(email)

addDeveloper()
