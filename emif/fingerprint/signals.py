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
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.conf import settings

from fingerprint.models import Fingerprint, FingerprintSubscription
from accounts.models import EmifProfile, RestrictedUserDbs

def fingerprint_updated(sender, **kwargs):
    fingerprint = kwargs['instance']
    created = kwargs['created']

    if created:
        fingerprint.setSubscription(fingerprint.owner, True)

        # We also check if the fingerprint was added by a restricted user,
        # if it was we must add this fingerprint to the restricted user, otherwise he wouldnt have access to his own database
        RestrictedUserDbs.get_or_create(fingerprint.owner, fingerprint)

post_save.connect(fingerprint_updated, sender=Fingerprint)



def shared_updated(sender, **kwargs):
    action = kwargs['action']
    fingerprint = kwargs['instance']
    changed_ids = kwargs['pk_set']

    if action == 'post_add' or action == 'post_remove':
        for pk in changed_ids:
            try:
                shared_user = User.objects.get(id=pk)
                if action == 'post_add':
                    fingerprint.setSubscription(shared_user, True)

                    # we auto-add restricted users to the database when this database is shared with them
                    RestrictedUserDbs.get_or_create(shared_user, fingerprint)

                elif action == 'post_remove':
                    fingerprint.setSubscription(shared_user, False)

                    # we also remove it automatically when its unshared
                    RestrictedUserDbs.remove(shared_user, fingerprint)

            except User.DoesNotExist:
                print "-- ERROR: Couldnt get user with primary key"+pk

m2m_changed.connect(shared_updated, sender=Fingerprint.shared.through)


def subscription_updated(sender, **kwargs):
    subscription = kwargs['instance']

    subscription.setNewsletterSubs(subscription.isSubscribed())


post_save.connect(subscription_updated, sender=FingerprintSubscription)
