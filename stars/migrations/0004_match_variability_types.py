# -*- coding: utf-8 -*-
import datetime

import frogress

from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        Star = orm['stars.Star']
        VariabilityType = orm['stars.VariabilityType']
        types_dict = {t.code: t for t in VariabilityType.objects.all()}
        stars = list(Star.objects.all())
        for star in frogress.bar(stars):
            code = star.variable_type
            # remove uncertainty flag
            code = code.replace(' ', '')
            code = code.replace(':', '')
            if not code:
                # nothing we can do, empty type
                continue
            if '/' in code:
                code = code.split('/')[0]
            if '+' in code:
                code = code.split('+')[0]
            if 'IN' in code and '(YY)' in code:
                code = 'IN(YY)'
            code = code.replace('(B)', '')
            if code in types_dict:
                # assign star to that type
                star.variability_type = types_dict[code]
                star.save()

    def backwards(self, orm):
        Star = orm['stars.Star']
        Star.objects.update(variability_type=None)

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
            'variability_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stars.VariabilityType']", 'null': 'True', 'blank': 'True'}),
            'variable_type': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '15'})
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
    symmetrical = True
