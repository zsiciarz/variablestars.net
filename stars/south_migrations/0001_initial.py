# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Star'
        db.create_table(u'stars_star', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('constellation', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('ra', self.gf('django.db.models.fields.CharField')(default=u'', max_length=15)),
            ('dec', self.gf('django.db.models.fields.CharField')(default=u'', max_length=15)),
            ('variable_type', self.gf('django.db.models.fields.CharField')(default=u'', max_length=15)),
            ('max_magnitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('min_magnitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('epoch', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('period', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'stars', ['Star'])


    def backwards(self, orm):
        # Deleting model 'Star'
        db.delete_table(u'stars_star')


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
        }
    }

    complete_apps = ['stars']