
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
