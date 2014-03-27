# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Slugs.question'
        db.delete_column('searchengine_slugs', 'question_id')


    def backwards(self, orm):
        # Adding field 'Slugs.question'
        db.add_column('searchengine_slugs', 'question',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=datetime.datetime(2014, 3, 27, 0, 0), to=orm['questionnaire.Question']),
                      keep_default=False)


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