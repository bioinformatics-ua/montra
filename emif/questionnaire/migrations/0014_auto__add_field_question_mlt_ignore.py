# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.mlt_ignore'
        db.add_column('questionnaire_question', 'mlt_ignore',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.mlt_ignore'
        db.delete_column('questionnaire_question', 'mlt_ignore')


    models = {
        'questionnaire.choice': {
            'Meta': {'object_name': 'Choice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Question']"}),
            'sortid': ('django.db.models.fields.IntegerField', [], {}),
            'text_en': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            'category': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'checks': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'extra_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'footer_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '2255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mlt_ignore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'questionset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionSet']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.Slugs']", 'null': 'True', 'blank': 'True'}),
            'stats': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tooltip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'visible_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'disable': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'redirect_url': ('django.db.models.fields.CharField', [], {'default': "'/static/complete.html'", 'max_length': '128'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'questionnaire.questionset': {
            'Meta': {'object_name': 'QuestionSet'},
            'checks': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '2255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Questionnaire']"}),
            'sortid': ('django.db.models.fields.IntegerField', [], {}),
            'text_en': ('django.db.models.fields.TextField', [], {}),
            'tooltip': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'questionnaire.questionsetpermissions': {
            'Meta': {'object_name': 'QuestionSetPermissions'},
            'allow_exporting': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_indexing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_printing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fingerprint_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionSet']"}),
            'visibility': ('django.db.models.fields.IntegerField', [], {})
        },
        'searchengine.slugs': {
            'Meta': {'object_name': 'Slugs'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug1': ('django.db.models.fields.CharField', [], {'max_length': '1256'})
        }
    }

    complete_apps = ['questionnaire']