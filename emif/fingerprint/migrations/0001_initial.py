# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fingerprint'
        db.create_table('fingerprint_fingerprint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fingerprint_hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('fingerprint', ['Fingerprint'])


    def backwards(self, orm):
        # Deleting model 'Fingerprint'
        db.delete_table('fingerprint_fingerprint')


    models = {
        'fingerprint.fingerprint': {
            'Meta': {'object_name': 'Fingerprint'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fingerprint_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['fingerprint']
