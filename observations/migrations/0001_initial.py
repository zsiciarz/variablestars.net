# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('observers', '0001_initial'),
        ('stars', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'Observation'
        db.create_table(u'observations_observation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('observer', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'observations', to=orm['observers.Observer'])),
            ('star', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'observations', to=orm['stars.Star'])),
            ('jd', self.gf('django.db.models.fields.FloatField')()),
            ('magnitude', self.gf('django.db.models.fields.FloatField')()),
            ('fainter_than', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comp1', self.gf('django.db.models.fields.CharField')(default=u'', max_length=5, blank=True)),
            ('comp2', self.gf('django.db.models.fields.CharField')(default=u'', max_length=5, blank=True)),
            ('comment_code', self.gf('django.db.models.fields.CharField')(default=u'', max_length=10, blank=True)),
            ('chart', self.gf('django.db.models.fields.CharField')(default=u'', max_length=20, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(default=u'', max_length=100, blank=True)),
        ))
        db.send_create_signal(u'observations', ['Observation'])


    def backwards(self, orm):
        # Deleting model 'Observation'
        db.delete_table(u'observations_observation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'observations.observation': {
            'Meta': {'ordering': "(u'-jd',)", 'object_name': 'Observation'},
            'chart': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '20', 'blank': 'True'}),
            'comment_code': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '10', 'blank': 'True'}),
            'comp1': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '5', 'blank': 'True'}),
            'comp2': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '5', 'blank': 'True'}),
            'fainter_than': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jd': ('django.db.models.fields.FloatField', [], {}),
            'magnitude': ('django.db.models.fields.FloatField', [], {}),
            'notes': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '100', 'blank': 'True'}),
            'observer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'observations'", 'to': u"orm['observers.Observer']"}),
            'star': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'observations'", 'to': u"orm['stars.Star']"})
        },
        u'observers.observer': {
            'Meta': {'ordering': "(u'-created',)", 'object_name': 'Observer'},
            'aavso_code': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '10', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limiting_magnitude': ('django.db.models.fields.FloatField', [], {'default': '6.0', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'observer'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
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

    complete_apps = ['observations']
