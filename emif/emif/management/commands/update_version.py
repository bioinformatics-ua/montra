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
#
from django.core.management.base import BaseCommand, CommandError
from emif.models import SharePending
from emif.utils import activate_user
from shutil import copyfile

from django.contrib.auth.models import User

import os
import re
import fileinput
import os.path
import datetime
import time

class Command(BaseCommand):

    args = '<new_version_number>'
    help = 'Updates the references to the version number and last updated by running through all the files in the deploy'

    recorded = 0
    version_patt     = "VERSION = '[^']*'"
    versiondate_patt = "VERSION_DATE = '[^']*'"

    def update_settings(self, version, version_date):
        settings_path = './emif/settings.py'

        #backup current file for case of something going wrong
        copyfile(settings_path, settings_path+'.backup')

        for line in fileinput.input(settings_path, inplace = True):
            new_line = re.sub(self.version_patt, "VERSION = '%s'" % version , line)
            new_line = re.sub(self.versiondate_patt, "VERSION_DATE = '%s'" % version_date, new_line)

            print new_line,

    def handle(self, *args, **options):

        # Recursive function that executes in each step
        def step(ext, dirname, names):
            ext = ext.lower()

            for name in names:
                stat = os.stat("%s/%s" % (dirname, name))
                if stat.st_mtime > self.recorded:
                    self.recorded=stat.st_mtime

        if len(args) == 1:
            os.path.walk('.', step, '.txt')

            new_time = datetime.datetime.fromtimestamp(self.recorded).strftime('%Y.%b.%d - %H:%MUTC')
            print "New version: %s" % args[0]
            print "Latest Update: %s" % new_time

            self.update_settings(args[0], new_time)

        else:
            self.stdout.write('-- USAGE: \n    '+
                'python manage.py update_version <new_version_number>'+
                '\n\n')
