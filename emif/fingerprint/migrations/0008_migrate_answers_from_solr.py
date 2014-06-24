# -*- coding: utf-8 -*-
import datetime

from south.db import db
from south.v2 import DataMigration
from django.db import models
from fingerprint.models import *

from searchengine.search_indexes import CoreEngine

class Migration(DataMigration):

    def forwards(self, orm):
        c = CoreEngine()

        # get all documents and add them to answer with the following fields:

        def getFingerprint(hash):
            try:
                fingerprint = Fingerprint.objects.get(fingerprint_hash=hash)

                return fingerprint

            except Fingerprint.DoesNotExist:
                return None

        def getQuestion(questions, slug):
            #print slug
            for q in questions:
                if q.slug_fk.slug1 == slug[:-2]:

                    return q

            return None

        def fix_wrong_names_on_observational():
            c = CoreEngine()
            documents = c.search_fingerprint("type_t:observationaldatasources")
            for doc in documents:
                old = None
                try:
                    old = doc['If_yes_:_repeated_measurements__t']
                    del doc['If_yes_:_repeated_measurements__t']
                except:
                    pass
                try:
                    old = doc['If_yes_:_repeated_measurements_t']
                    del doc['If_yes_:_repeated_measurements_t']
                except:
                    pass
                if old != None:
                    print "Replacing"
                    doc['If_yes__repeated_measurements_t'] = old
                    c.update(doc)

        def convertAnswerToJson(question, value):
            ''' TYPES : TO DO
             open
            open-button
            open-upload-image
            open-textfield
            choice-yesno
            choice-yesnocomment
            choice-yesnodontknow
            datepicker
            email
            url
            comment
            choice
            choice-freeform
            choice-multiple
            choice-multiple-freeform
            choice-multiple-freeform-options
            range
            timeperiod
            custom
            publication
            numeric
            sameas
            '''
            return value;

        def getOwners(owners_string):

            owners_split = owners_string.split(' \\ ')

            owners = []

            for o in owners_split:
                try: 
                    user = User.objects.get(username=o)

                    owners.append(user)

                except User.DoesNotExist:
                    print "Couldnt find user "+o

            if len(owners) == 0:
                return (None, None)
            elif len(owners) == 1:
                return (owners[0], [owners[0]])
            else:
                return (owners[0], owners[1:])


        # First we need to fix wrongly named fields on observational_data_sources
        fix_wrong_names_on_observational()

        documents = c.search_fingerprint("*:*")

        for doc in documents:

            ignorelist = ['id', 'type_t', '_version_', 'text_t', 'date_last_modification_t', 'user_t', 'created_t']
            this_id = doc['id']
            
            print "-- Processing ---------------------- " + this_id + "\n"

            if "questionaire_" not in this_id:

                fingerprint_id = getFingerprint(this_id)
                date_last_modification = None
                try:
                    date_last_modification = doc['date_last_modification_t']
                except:
                    date_last_modification = "1970-01-01 00:00:00.000000"

                date_create = doc['created_t']
                user = doc['user_t']

                # update parameters from data from solr
                if date_last_modification and date_create and user: 
                    fingerprint_id.last_modification = datetime.datetime.strptime(date_last_modification, '%Y-%m-%d %H:%M:%S.%f')
                    fingerprint_id.created = datetime.datetime.strptime(date_create, '%Y-%m-%d %H:%M:%S.%f')

                    (owner, shared) = getOwners(user)

                    fingerprint_id.owner = owner

                    for share in shared:
                        fingerprint_id.shared.add(share)

                    fingerprint_id.save()

                questions_possible = fingerprint_id.questionnaire.questions()
                for key in doc:
                    if key not in ignorelist and not key.startswith('comment_question_') and key.endswith('_t'):

                        question = getQuestion(questions_possible, key)
                        data = convertAnswerToJson(question, doc[key])
                        comment = None
                        try:
                            comment = doc['comment_question_'+key]
                        except:
                            pass   

                        if question == None:
                            print "EMPTY KEY ON:"+key   

                        ans = Answer(question=question, data=data, comment=comment, fingerprint_id=fingerprint_id) 
                        ans.save()     
            print "---------------------------------------- "          
            print " "
        
        #raise RuntimeError("You can't stop the music...")
    
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
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Questionnaire']", 'null': 'True'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
