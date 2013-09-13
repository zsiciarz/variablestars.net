# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VariabilityType'
        db.create_table(u'stars_variabilitytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=12, db_index=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('long_description', self.gf('django.db.models.fields.TextField')(default=u'')),
        ))
        db.send_create_signal(u'stars', ['VariabilityType'])


    def backwards(self, orm):
        # Deleting model 'VariabilityType'
        db.delete_table(u'stars_variabilitytype')


    models = {
        u'stars.star': {
            'Meta': {'ordering': "(u'constellation', u'name')", 'object_name': 'Star'},
            'constellation': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'dec': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '15'}),
            'epoch': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_magnitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'min_magnitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'period': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'ra': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '15'}),
            'variable_type': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '15'})
        },
        u'stars.variabilitytype': {
            'Meta': {'ordering': "(u'code',)", 'object_name': 'VariabilityType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['stars']