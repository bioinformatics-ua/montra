from django.db import models

from django.contrib.auth.models import User
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
