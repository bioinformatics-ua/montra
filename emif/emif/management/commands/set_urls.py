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
from shutil import copyfile

import os
import re
import fileinput

class Command(BaseCommand):

    args = '<static_url base_url>'
    help = 'Replaces STATIC_URL and BASE_URL with the specified url in 404.html, 500.html, base.html, signin_form and index_new.html'

    def handle(self, *args, **options):

        path404         = 'emif/templates/404.html'
        path500         = 'emif/templates/500.html'
        pathbase        = 'emif/templates/base.html'
        pathindex       = 'emif/templates/index_new.html'
        signin_form     = 'accounts/templates/userena/signin_form.html'
        static_patt     = 'STATIC_URL=("[^"]*"|STATIC_URL)'
        base_patt       = 'BASE_URL=("[^"]*"|BASE_URL)'

        files = [path404, path500, pathbase, pathindex, signin_form]

        def changeOnFiles(static, base):
            if  os.path.exists(path404)   and \
                os.path.exists(path500)   and \
                os.path.exists(pathbase)  and \
                os.path.exists(pathindex):

                    # Treat files
                    for file in files:
                        # Create file backup
                        copyfile(file, file+'.backup')

                        # on the old file replace with variable assignments
                        # i did it this way so we can redefine the variables as much times as we may need
                        for line in fileinput.input(file, inplace = True):
                            new_line =re.sub(static_patt, 'STATIC_URL='+static, line)
                            new_line =re.sub(base_patt, 'BASE_URL='+base, new_line)

                            print new_line,

                    self.stdout.write('Replaced STATIC_URL WITH: '+static+' and BASE_URL WITH '+base+'\n')

            else:
                self.stdout.write('One (or all) of the templates didn\'t exist. Please confirm the following files exist: \n'
                + path404 + '\n' + path500 + '\n'+pathindex+'\n'+pathbase+'\n\n')




        if len(args) == 1 and args[0] == 'reset':
            changeOnFiles('STATIC_URL', 'BASE_URL')


        elif len(args) == 2:
            static = args[0].replace(' ', '%20').replace('"','')
            base = args[1].replace(' ', '%20').replace('"','')

            changeOnFiles('"'+static+'"', '"'+base+'"')

        else:
            self.stdout.write('-- USAGE: \n    '+
                'For replacement:\n        '+
                'python manage.py set_urls <static_url_to_set> <base_url_to_set>'+
                '\n\n    For resetting to default:'+
                '\n        python manage.py set_urls reset'+
                '\n\n')
