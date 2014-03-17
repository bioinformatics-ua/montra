from django.db import models

from django.core.validators import MaxLengthValidator

class Fingerprint(models.Model):
  fingerprint_hash =  models.CharField(max_length=255, unique=True, blank=False, null=False)
  description = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(600)])



  def __unicode__(self):
    return self.fingerprint_hash