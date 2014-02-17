from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django_countries import CountryField
from django.core.validators import MaxLengthValidator


class EmifProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='emif_profile')
    country = CountryField()
    organization = models.CharField(_('organization'), max_length=255)

class Profile(models.Model):
	name = models.CharField(unique=True, max_length=60, verbose_name=_('Name'))
	description = models.TextField(blank=True, null=True, verbose_name=_('Description'), validators=[MaxLengthValidator(600)])
	users = models.ManyToManyField(User, blank=True, verbose_name=_('Users'))

	def __unicode__(self):
		return self.name
