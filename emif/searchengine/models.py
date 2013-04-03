from django.db import models




from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=40)
    body = models.TextField()

    def __unicode__(self):
        return self.name

