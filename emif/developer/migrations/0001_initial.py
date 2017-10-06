# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Plugin'
        db.create_table('developer_plugin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('latest_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_remote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('remote_url', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('removed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('developer', ['Plugin'])


    def backwards(self, orm):
        # Deleting model 'Plugin'
        db.delete_table('developer_plugin')


    models = {
        'developer.plugin': {
            'Meta': {'object_name': 'Plugin'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_remote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latest_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remote_url': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['developer']