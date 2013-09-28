# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Star.observations_count'
        db.add_column(u'stars_star', 'observations_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Star.observations_count'
        db.delete_column(u'stars_star', 'observations_count')


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
            'observations_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'period': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'ra': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '15'}),
            'variability_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stars.VariabilityType']", 'null': 'True', 'blank': 'True'})
        },
        u'stars.variabilitytype': {
            'Meta': {'ordering': "(u'code',)", 'object_name': 'VariabilityType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'short_description': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['stars']