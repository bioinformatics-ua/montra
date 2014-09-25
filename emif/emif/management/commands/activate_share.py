# Copyright (C) 2014 Ricardo Ribeiro and Universidade de Aveiro
#
# Authors: Ricardo Ribeiro <ribeiro.r@ua.pt>
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

from django.core.management.base import BaseCommand, CommandError
from emif.models import SharePending
from emif.utils import activate_user

from django.contrib.auth.models import User

import os
import re
import fileinput

class Command(BaseCommand):

    args = '<email> <fingerprint_id>'
    help = 'Manually activates an user without the need to go through normal activation procedures'

    def handle(self, *args, **options):
        if len(args) == 2:
            try:
                this_user = User.objects.get(email=args[0])
                
                users_pending = SharePending.objects.filter(user=this_user, db_id=args[1])

                if(len(users_pending) >= 1):
                    user_pending = users_pending[0]

                    success = activate_user(user_pending.activation_code, this_user)

                    if success:
                        self.stdout.write("Username with email "+str(args[0])+" activated in db"+str(args[1])+".\n")
                    else:
                        self.stdout.write("-- Error: Username with email "+str(args[0])+" couldn't be activated on db "+str(args[1])+".\n")

                elif(len(users_pending) == 0):
                    self.stdout.write("-- Error: There's no user to activate with the email "+str(args[0])+" on db "+str(args[1])+".\n")

            except User.DoesNotExist:
                self.stdout.write("-- Error: There's no user with the email "+str(args[0])+" to activate db "+str(args[1])+".\n")
                pass


        else:
            self.stdout.write('-- USAGE: \n    '+
                'python manage.py activate_share <email> <fingerprint_id>'+
                '\n\n')