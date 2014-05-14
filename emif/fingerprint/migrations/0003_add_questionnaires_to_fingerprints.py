# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from questionnaire.models import Questionnaire
from fingerprint.models import *

from searchengine.search_indexes import CoreEngine, convert_value, assert_suffix

class Migration(DataMigration):

    def forwards(self, orm):
        def add_questionnaires():

            print "\n----------------------------------------------"
            print "Start adding "
            print "-----------------------------------------------"
            #Find all questionnarie types
            questionnaires = Questionnaire.objects.all()

            c = CoreEngine()

            documents = c.search_fingerprint("*:*")

            # for each solr document
            for doc in documents:
                # get id and question type
                
                quest_type = None 
                this_id = doc['id']

                if "questionnaire_ " in this_id:
                    print "Passing "+this_id
                    continue

                try: 
                    quest_type = doc['type_t']
                except:
                    print "Found database "+this_id+" on solr without type_t"
                    continue

                # get fingerprint reference

                fingerprint = None

                try:
                    fingerprint = Fingerprint.objects.get(fingerprint_hash=this_id)
                except Fingerprint.DoesNotExist:
                    fingerprint = Fingerprint(fingerprint_hash=this_id)

                quest = get_questionnaire(questionnaires, quest_type)

                if quest != None :
                    fingerprint.questionnaire = quest

                    print fingerprint.fingerprint_hash + " - " +fingerprint.questionnaire.slug

                    fingerprint.save()



                else:
                    print "-- ERROR: cant find quest_type "+quest_type

            # we need to check if there are dummy fingerprints ids on the table

            fingerprints = Fingerprint.objects.all()

            for f in fingerprints:
                if f.questionnaire == None:
                    print "Deleting, questionnaire not on "+f.fingerprint_hash
                    f.delete()

            print "-----------------------------------------------"
            print " End"
            print "-----------------------------------------------"

        def get_questionnaire(questionnaires, slug):

            for q in questionnaires:
                if slug == q.slug:
                    return q

            return None

        add_questionnaires()   


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        'fingerprint.answer': {
            'Meta': {'object_name': 'Answer'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'fingerprint_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fingerprint.Fingerprint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Question']"})
        },
        'fingerprint.fingerprint': {
            'Meta': {'object_name': 'Fingerprint'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fingerprint_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Questionnaire']", 'null': 'True'})
        },
        'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            'category': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'checks': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'extra_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'footer_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '2255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'questionset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionSet']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.Slugs']", 'null': 'True', 'blank': 'True'}),
            'stats': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tooltip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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
    symmetrical = True
