# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Holder'
        db.create_table('quotaholder_app_holder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('holder', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4096, db_index=True)),
        ))
        db.send_create_signal('quotaholder_app', ['Holder'])


    def backwards(self, orm):
        # Deleting model 'Holder'
        db.delete_table('quotaholder_app_holder')


    models = {
        'quotaholder_app.commission': {
            'Meta': {'object_name': 'Commission'},
            'clientkey': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'issue_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4096'}),
            'serial': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'quotaholder_app.holder': {
            'Meta': {'object_name': 'Holder'},
            'holder': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4096', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'quotaholder_app.holding': {
            'Meta': {'unique_together': "(('holder', 'source', 'resource'),)", 'object_name': 'Holding'},
            'holder': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.BigIntegerField', [], {}),
            'resource': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True'}),
            'usage_max': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'usage_min': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'quotaholder_app.provision': {
            'Meta': {'object_name': 'Provision'},
            'holder': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.BigIntegerField', [], {}),
            'resource': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'serial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'provisions'", 'to': "orm['quotaholder_app.Commission']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True'})
        },
        'quotaholder_app.provisionlog': {
            'Meta': {'object_name': 'ProvisionLog'},
            'delta_quantity': ('django.db.models.fields.BigIntegerField', [], {}),
            'holder': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_time': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'limit': ('django.db.models.fields.BigIntegerField', [], {}),
            'log_time': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'resource': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'serial': ('django.db.models.fields.BigIntegerField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True'}),
            'usage_max': ('django.db.models.fields.BigIntegerField', [], {}),
            'usage_min': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['quotaholder_app']