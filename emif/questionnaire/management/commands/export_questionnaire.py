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

from django.contrib.auth.models import User

from questionnaire.models import Questionnaire

from questionnaire.export import ExportQuestionnaire

class Command(BaseCommand):

    args = '<database_slug> <file_path>'
    help = 'Export the questionnaire to excel'

    def handle(self, *args, **options):
        if len(args) == 2:
            slug = args[0]
            file_path = args[1]

            exporter = ExportQuestionnaire.factory("excel", Questionnaire.objects.get(slug=slug), file_path)
            exporter.export()

        else:
            self.stdout.write('-- USAGE: \n    '+
                'python manage.py export_questionnaire <database_slug> <path_file>'+
                '\n\n')
