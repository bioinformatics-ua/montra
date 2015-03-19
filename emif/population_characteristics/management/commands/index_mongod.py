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

from emif.settings import jerboa_collection, jerboa_aggregation_collection

from fingerprint.models import *
#from fingerprint.services import indexFingerprint

from population_characteristics.models import *
from population_characteristics.tasks import aggregation
from population_characteristics.services import PopulationCharacteristic

class Command(BaseCommand):
    args = '<mode>'
    help = 'Indexes all Population Characteristic Files to mongodb'

    def handle(self, *args, **options):

        def clean():
            # do clean up job
            self.stdout.write('-- Cleaning population characteristics data\n')
            jerboa_collection.remove({})
            self.stdout.write('-- Cleaning aggregation data\n\n')
            jerboa_aggregation_collection.remove({})

        def index():
            fingerprints = Fingerprint.objects.all()

            for fingerprint in fingerprints:

                jerboa_files = Characteristic.objects.filter(fingerprint_id=fingerprint.fingerprint_hash).order_by('latest_date')

                if len(jerboa_files) > 0:
                    self.stdout.write('-- Indexing Jerboa Files from fingerprint '+str(fingerprint)+'.\n')

                for jerboa_file in jerboa_files:
                    pc = PopulationCharacteristic()
                    data_jerboa = pc.submit_new_revision(jerboa_file.user,
                        jerboa_file.fingerprint_id, jerboa_file.revision, jerboa_file.path)
                    aggregation.apply_async([jerboa_file.fingerprint_id, data_jerboa])

                    self.stdout.write('---- Indexing file '+str(jerboa_file.file_name)+'.\n')

            self.stdout.write('-- Finished indexing all population characteristic files to mongodb.\n')

        def print_usage():
            self.stdout.write('--------------------------------------------------\nUsage:\n')
            self.stdout.write('        Clean and Index after (default) :\n')
            self.stdout.write('            python manage.py index_mongod\n\n')
            self.stdout.write('        Index only :\n')
            self.stdout.write('            python manage.py index_mongod index\n\n')
            self.stdout.write('        Clean only :\n')
            self.stdout.write('           python manage.py index_mongod clean\n')
            self.stdout.write('\n--------------------------------------------------\n')

        if len(args) == 0:
            clean()
            index()
        elif len(args) == 1:
            param = args[0].lower()
            if param == 'index':
                index()
            if param == 'clean':
                clean()
            else:
                print_usage()
        else :
            print_usage()




