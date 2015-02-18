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
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User

from questionnaire.imports import ImportQuestionnaire

class Command(BaseCommand):

    args = '<file_path> <questionnaire_id>'
    help = 'Import the questionnaire from excel merging with an already existing questionnaire'

    def handle(self, *args, **options):
        if len(args) == 2:

            iq = ImportQuestionnaire.factory('excel', args[0])

            res = iq.import_questionnaire(merge=args[1])

            print "RESUKT:"
            print res

            print "-- Finished processing "+args[0]

        else:
            self.stdout.write('-- USAGE: \n    '+
                'python manage.py merge_questionnaire <path_file> <questionnaire_id>'+
                '\n\n')
