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

from accounts.models import EmifProfile
import sys

def setPagination(new_value):
    print '\nChanging default pagination for users to '+str(new_value)+'...\n'

    users = EmifProfile.objects.all()

    for user in users:
        if user.paginator < 10:
            user.paginator = new_value
            print user.user.username + " :" + str(user.paginator)
            user.save()

    print '\nend!'

setPagination(10)
