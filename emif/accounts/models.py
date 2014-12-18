from django.db import models

from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django_countries import CountryField
from django.core.validators import MaxLengthValidator

from questionnaire.models import Questionnaire


from django.core.cache import cache
from hitcount.models import Hit, HitCount
from fingerprint.models import Fingerprint

from django.utils import timezone
from datetime import timedelta


from fingerprint.models import Fingerprint

from django.db.models import Count

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

    mail_news   = models.BooleanField(default=True)
    mail_not    = models.BooleanField(default=False)

    restricted = models.BooleanField(default=False)

    def has_group(self, group_name):
        group = Group.objects.get(name=group_name)
        return True if group in self.user.groups.all() else False

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

    @staticmethod
    def top_users(limit=None, days_to_count=None):
        top_users = cache.get('topusers'+str(limit)+'_'+str(days_to_count))

        if top_users == None:
            top_users = {}

            hitcounts = HitCount.objects.all()

            for hitcount in hitcounts:
                try:
                    fingerprint = Fingerprint.objects.get(id=hitcount.object_pk)


                    cycle_count = hitcount.hits
                    if(days_to_count != None):
                        # we must count from hits, instead of used the summarized value
                        limit_date =timezone.now() - timedelta(days=days_to_count)

                        cycle_count = len(Hit.objects.filter(hitcount=hitcount, created__gte=limit_date))


                    if cycle_count > 0:
                        for user in fingerprint.unique_users():
                            if user in top_users:
                                top_users[user]['count'] = top_users[user]['count'] + cycle_count
                            else:
                                top_users[user] = {
                                'user': user.get_full_name(),
                                'email': user.email,
                                'count': cycle_count,
                                'owned': len(Fingerprint.objects.filter(owner=user)) + len(Fingerprint.objects.filter(shared__id=user.id))}

                except Fingerprint.DoesNotExist:
                    print "-- ERROR: Couldn't retrieve fingerprint refered by hitcount" + str(hitcount.id)

            top_users = sorted(top_users.values(), reverse=True, key=lambda x:x['count'])

            if limit != None:
                top_users = top_users[:limit]

            # keeping in cache 1 hour
            cache.set('topusers'+str(limit)+'_'+str(days_to_count), top_users, 60*60)

        return top_users

    @staticmethod
    def top_navigators(limit=None, days_to_count=None):
        top_users = cache.get('topnavigators'+str(limit)+'_'+str(days_to_count))

        if top_users == None:
            top_users = []

            limit_date = None

            if(days_to_count != None):
                # we must count from hits, instead of used the summarized value
                limit_date = timezone.now() - timedelta(days=days_to_count)

            log = None
            if(limit_date != None):
                log = NavigationHistory.objects.filter(date__gte=limit_date)
            else:
                log = NavigationHistory.objects.all()

            log = log.values('user').annotate(total=Count('user')).order_by('-total')

            if limit != None:
                log = log[:limit]

            for line in log:
                try:
                    this_user = User.objects.get(id=line['user'])

                    top_users.append({
                             'user': this_user.get_full_name(),
                             'email': this_user.email,
                             'count': line['total']
                             }
                    )

                except User.DoesNotExist:
                    print "-- ERROR: Cant find user with id "+str(line['user'])

            # keeping in cache 1 hour
            cache.set('topnavigators'+str(limit)+'_'+str(days_to_count), top_users, 60*60)

        return top_users


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

    @staticmethod
    def top_users(limit=None, days_to_count=None):
        top_users = cache.get('topusers'+str(limit))

        if top_users == None:
            top_users = {}

            hitcounts = HitCount.objects.all()

            for hitcount in hitcounts:
                try:
                    fingerprint = Fingerprint.objects.get(id=hitcount.object_pk)


                    cycle_count = hitcount.hits
                    if(days_to_count != None):
                        # we must count from hits, instead of used the summarized value
                        limit_date =timezone.now() - timedelta(days=days_to_count)

                        cycle_count = len(Hit.objects.filter(hitcount=hitcount, created__gte=limit_date))


                    if cycle_count > 0:
                        if fingerprint.owner in top_users:
                            top_users[fingerprint.owner]['count'] = top_users[fingerprint.owner]['count'] + cycle_count
                        else:
                            top_users[fingerprint.owner] = {
                            'user': fingerprint.owner.get_full_name(),
                            'email': fingerprint.owner.email,
                            'count': cycle_count,
                            'owned': len(Fingerprint.objects.filter(owner=fingerprint.owner))}

                except Fingerprint.DoesNotExist:
                    print "-- ERROR: Couldn't retrieve fingerprint refered by hitcount" + str(hitcount.id)

            top_users = sorted(top_users.values(), reverse=True, key=lambda x:x['count'])

            if limit != None:
                top_users = top_users[:limit]

            # keeping in cache 1 hour
            cache.set('topusers'+str(limit), top_users, 60*60)

        return top_users


class NavigationHistory(models.Model):
    user = models.ForeignKey(User)
    path = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


