from django.db import models

from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django_countries import CountryField
from django.core.validators import MaxLengthValidator

from questionnaire.models import Questionnaire

from fingerprint.models import Fingerprint

class Profile(models.Model):
    name = models.CharField(unique=True, max_length=60, verbose_name=_('Name'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'), validators=[MaxLengthValidator(600)])

    def __unicode__(self):
        return self.name

class EmifProfile(UserenaBaseProfile):
    options = (
        (5, '5'),
        (10, '10'),
        (25, '25'),
        (50, '50'),
        (-1, 'All'),
        )
    user = models.OneToOneField(User,
        unique=True,
        verbose_name=_('user'),
        related_name='emif_profile')

    country = CountryField()
    organization = models.CharField(_('organization'), max_length=255)

    profiles = models.ManyToManyField(Profile,
       verbose_name=_('profiles'),
       related_name='emif_profile')

    interests = models.ManyToManyField(Questionnaire,
       verbose_name=_('interests'),
       related_name='emif_profile')

    paginator = models.IntegerField(max_length=2,
      choices=options,
      default=10)

    restricted = models.BooleanField(default=False)

    def has_permission(self, hash):
        try:
            fingerprint = Fingerprint.objects.get(fingerprint_hash=hash)

            dbs = RestrictedGroup.hashes(self.user)

            for db in dbs:
                if db == hash:
                    return True

            dbs = RestrictedUserDbs.objects.filter(user=self.user)

            for db in dbs:
                if db.fingerprint.fingerprint_hash == hash:
                    return True

        except Fingerprint.DoesNotExist:
            print "-- ERROR: Fingerprint with hash "+str(hash)+"does not exist."

        return False

class RestrictedGroup(models.Model):
    group = models.OneToOneField(Group, unique=True)
    fingerprints = models.ManyToManyField(Fingerprint)

    def fingerprint_hashes(self):
        fingerprints = set()

        for fingerprint in self.fingerprints.all():
            fingerprints.add(fingerprint.fingerprint_hash)

        return fingerprints

    @staticmethod
    def hashes(user):
        rgroups = RestrictedGroup.objects.all()

        ugroups = user.groups.all()

        fingerprints = set()

        for group in ugroups:
            try:
                this_group = rgroups.get(group=group)

                fingerprints.update(this_group.fingerprint_hashes())
            except RestrictedGroup.DoesNotExist:
                pass

        return fingerprints


class RestrictedUserDbs(models.Model):
    user = models.ForeignKey(User)
    fingerprint = models.ForeignKey(Fingerprint)

    def findName(self):
        return self.fingerprint.findName()

    @staticmethod
    def get_or_create(user, fingerprint):
        try:
            eprofile = EmifProfile.objects.get(user=fingerprint.owner)

            if eprofile.restricted:
                allowed = None
                try:
                    allowed = RestrictedUserDbs.objects.get(user=user, fingerprint = fingerprint)
                except RestrictedUserDbs.DoesNotExist:
                    allowed = RestrictedUserDbs(user=user, fingerprint = fingerprint)
                    allowed.save()

                    return allowed

        except EmifProfile.DoesNotExist:
            print "-- ERROR: Couldn't get emif profile for user"

            return None

    @staticmethod
    def remove(user, fingerprint):
        try:
            eprofile = EmifProfile.objects.get(user=fingerprint.owner)

            if eprofile.restricted:
                allowed = None
                try:
                    allowed = RestrictedUserDbs.objects.get(user=user, fingerprint = fingerprint)

                    allowed.delete()

                except RestrictedUserDbs.DoesNotExist:
                    return True

            return False

        except EmifProfile.DoesNotExist:
            print "-- ERROR: Couldn't get emif profile for user"

            return False

class NavigationHistory(models.Model):
    user = models.ForeignKey(User)
    path = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


