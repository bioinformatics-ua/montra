from fingerprint.models import Fingerprint, Answer
from fingerprint.tasks import *

def fill():
    print "-- Starting calculating fingerprint filled rate"
    fingerprints = Fingerprint.objects.all()

    for fingerprint in fingerprints:
        calculateFillPercentage.delay(fingerprint)

    print "-- Finished calculating fingerprint filled rate!"

fill()
