# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Budget'
        db.create_table('budget_budget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=14, decimal_places=2)),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounts.Account'])),
            ('payee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounts.Account'])),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Journal'], null=True)),
            ('is_applied', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('budget', ['Budget'])


    def backwards(self, orm):
        
        # Deleting model 'Budget'
        db.delete_table('budget_budget')


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
        'budget.budget': {
            'Meta': {'object_name': 'Budget'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '14', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_applied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Journal']", 'null': 'True'}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounts.Account']"}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounts.Account']"})
        }
    }

    complete_apps = ['budget']
