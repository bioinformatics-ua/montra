from fingerprint.models import Fingerprint


def syncDbs():
    print "-- Starting syncing databases newsletters, this will set a subscript"

    fingerprints = Fingerprint.valid()

    for fingerprint in fingerprints:

        fingerprint.save() # syncs owner, creates objects as necessary via signals

        for shared in fingerprint.shared.all():
            fingerprint.setSubscription(shared, True) # sync shared owners already existing

    print "-- Finished !!"


syncDbs()
