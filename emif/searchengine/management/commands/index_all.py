from django.core.management.base import BaseCommand, CommandError
from fingerprint.models import Fingerprint

class Command(BaseCommand):
    args = ''
    help = 'Indexes all Fingerprints in SOLR (WIP)'

    def handle(self, *args, **options):
        Fingerprint.index_all()

        self.stdout.write('-- Finished indexing all fingerprints in SOLR.\n')
