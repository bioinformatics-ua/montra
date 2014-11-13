# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Slugs'
        db.create_table('searchengine_slugs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug1', self.gf('django.db.models.fields.CharField')(max_length=1256)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('searchengine', ['Slugs'])

        # Adding model 'Nomenclature'
        db.create_table('searchengine_nomenclature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('searchengine', ['Nomenclature'])


    def backwards(self, orm):
        # Deleting model 'Slugs'
        db.delete_table('searchengine_slugs')

        # Deleting model 'Nomenclature'
        db.delete_table('searchengine_nomenclature')


    models = {
        'searchengine.nomenclature': {
            'Meta': {'object_name': 'Nomenclature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'searchengine.slugs': {
            'Meta': {'object_name': 'Slugs'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug1': ('django.db.models.fields.CharField', [], {'max_length': '1256'})
        }
    }

    complete_apps = ['searchengine']
