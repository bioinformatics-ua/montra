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
from searchengine.search_indexes import CoreEngine
from emif.models import QueryLog

class Command(BaseCommand):
    args = ''
    help = 'Indexes all user queries in SOLR for suggestions'

    def handle(self, *args, **options):

        self.__indexQueryLog()

        self.stdout.write('-- Finished indexing.\n')

    def __indexQueryLog(self):
        c = CoreEngine(core='suggestions')

        queries = QueryLog.objects.all()

        print "-- Indexing "+str(len(queries))+" simple queries"

        temp_array = []

        for query in queries:
            qdict = query.__dict__

            del qdict['_state']
            qdict['query'] = qdict['query'].strip().lower()
            temp_array.append(qdict)

            if len(temp_array) == 200:
                c.index_fingerprints(temp_array)
                temp_array = []

        if len(temp_array) > 0:
            c.index_fingerprints(temp_array)
