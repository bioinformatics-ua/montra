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
from fingerprint.models import Fingerprint

from public.models import PublicFingerprintShare
from django.utils import timezone
from datetime import timedelta, date

from emif.settings import PUBLIC_LINK_MAX_VIEWS, PUBLIC_LINK_MAX_TIME
import uuid

def createFingerprintShare(fingerprint_id, user, description=None):
    try:
        fingerprint = Fingerprint.objects.get(fingerprint_hash=fingerprint_id)
        expiration_date = timezone.now() + timedelta(hours=PUBLIC_LINK_MAX_TIME)

        new_share = PublicFingerprintShare(fingerprint=fingerprint, user=user,
            hash=uuid.uuid4(),
            expiration_date=expiration_date, remaining_views=PUBLIC_LINK_MAX_VIEWS, description=description)

        new_share.save()

        return new_share
    except Fingerprint.DoesNotExist:
        print "Impossible to share fingerprint that doesn't exist"

    return None

def deleteFingerprintShare(share_id):
    try:
        share = PublicFingerprintShare.objects.get(id=share_id)

        share.delete()

        return True
    except Fingerprint.DoesNotExist:
        print "Impossible to delete a share that doesn't exist"

    return False

def shouldDelete(fingerprintshare):

    if fingerprintshare.remaining_views <= 0:
        print "No more views remaining"
        return True

    if timezone.now() > fingerprintshare.expiration_date:
        print "Time of share is up"
        return True

    return False
