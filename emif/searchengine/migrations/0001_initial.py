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
