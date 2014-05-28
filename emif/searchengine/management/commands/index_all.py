from django.core.management.base import BaseCommand, CommandError
from fingerprint.models import *

from fingerprint.services import indexFingerprint

class Command(BaseCommand):
    args = ''
    help = 'Indexes all Fingerprints in SOLR (WIP)'

    def handle(self, *args, **options):
        all_fingerprints = Fingerprint.objects.all()

        for fingerprint in all_fingerprints:
            self.stdout.write('-- Indexing '+fingerprint.fingerprint_hash+'.\n')
            indexFingerprint(fingerprint.fingerprint_hash)
            

        self.stdout.write('-- Finished indexing all fingerprints in SOLR.\n')