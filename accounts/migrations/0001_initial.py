# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Journal'
        db.create_table('accounts_journal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('accounts', ['Journal'])

        # Adding model 'Posting'
        db.create_table('accounts_posting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=14, decimal_places=2)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Journal'])),
        ))
        db.send_create_signal('accounts', ['Posting'])

        # Adding model 'Account'
        db.create_table('accounts_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal('accounts', ['Account'])


    def backwards(self, orm):
        
        # Deleting model 'Journal'
        db.delete_table('accounts_journal')

        # Deleting model 'Posting'
        db.delete_table('accounts_posting')

        # Deleting model 'Account'
        db.delete_table('accounts_account')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '14', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'accounts.journal': {
            'Meta': {'object_name': 'Journal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.posting': {
            'Meta': {'object_name': 'Posting'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '14', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Journal']"})
        }
    }

    complete_apps = ['accounts']
