# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AnswerRequest.comment'
        db.add_column('fingerprint_answerrequest', 'comment',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1000),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AnswerRequest.comment'
        db.delete_column('fingerprint_answerrequest', 'comment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'emif.advancedquery': {
            'Meta': {'object_name': 'AdvancedQuery'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'qid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Questionnaire']"}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'serialized_query': ('django.db.models.fields.TextField', [], {}),
            'serialized_query_hash': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'emif.querylog': {
            'Meta': {'object_name': 'QueryLog'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'fingerprint.answer': {
            'Meta': {'object_name': 'Answer'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'fingerprint_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Fingerprint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Question']"})
        },
        'fingerprint.answerchange': {
            'Meta': {'object_name': 'AnswerChange'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Answer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'new_value': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'old_comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'old_value': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'revision_head': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.FingerprintHead']"})
        },
        'fingerprint.answerrequest': {
            'Meta': {'object_name': 'AnswerRequest'},
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'fingerprint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Fingerprint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Question']"}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'fingerprint.fingerprint': {
            'Meta': {'object_name': 'Fingerprint'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fill': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'fingerprint_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modification': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fingerprint_owner_fk'", 'to': "orm['auth.User']"}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Questionnaire']", 'null': 'True'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shared': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'fingerprint_shared_fk'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'fingerprint.fingerprinthead': {
            'Meta': {'object_name': 'FingerprintHead'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fingerprint_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Fingerprint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'revision': ('django.db.models.fields.IntegerField', [], {})
        },
        'fingerprint.fingerprintreturnedadvanced': {
            'Meta': {'object_name': 'FingerprintReturnedAdvanced'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fingerprint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Fingerprint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query_reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emif.AdvancedQuery']"}),
            'searcher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'fingerprint.fingerprintreturnedsimple': {
            'Meta': {'object_name': 'FingerprintReturnedSimple'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fingerprint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Fingerprint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query_reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emif.QueryLog']"}),
            'searcher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'fingerprint.fingerprintsubscription': {
            'Meta': {'object_name': 'FingerprintSubscription'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fingerprint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Fingerprint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'fingerprint.questionsetcompletion': {
            'Meta': {'object_name': 'QuestionSetCompletion'},
            'answered': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fill': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'fingerprint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Fingerprint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'possible': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'questionset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionSet']"})
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
        'searchengine.slugs': {
            'Meta': {'object_name': 'Slugs'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug1': ('django.db.models.fields.CharField', [], {'max_length': '1256'})
        }
    }

    complete_apps = ['fingerprint']
