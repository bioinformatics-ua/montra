"""
Execute tests
"""

from django.test import TestCase

from fingerprint.models import * 

class TestFingerprint(TestCase):

    def set_up(self):
        pass

    def list_all_databases(self):

        fp = FingerprintDescription("66a47f694ffb676bf7676dfde24900e6")
        pass


