# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Period'
        db.delete_table('budget_period')

        # Adding model 'AutoBudget'
        db.create_table('budget_autobudget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('delta', self.gf('django.db.models.fields.DecimalField')(default='86400.0', max_digits=14, decimal_places=2)),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=14, decimal_places=2)),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounts.Account'])),
            ('payee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounts.Account'])),
        ))
        db.send_create_signal('budget', ['AutoBudget'])

        # Deleting field 'Budget.period'
        db.delete_column('budget_budget', 'period_id')

        # Adding field 'Budget.auto_budget'
        db.add_column('budget_budget', 'auto_budget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.AutoBudget'], null=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Period'
        db.create_table('budget_period', (
            ('payee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounts.Account'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=14, decimal_places=2)),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounts.Account'])),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('delta', self.gf('django.db.models.fields.DecimalField')(default='86400.0', max_digits=14, decimal_places=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('budget', ['Period'])

        # Deleting model 'AutoBudget'
        db.delete_table('budget_autobudget')

        # Adding field 'Budget.period'
        db.add_column('budget_budget', 'period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['budget.Period'], null=True), keep_default=False)

        # Deleting field 'Budget.auto_budget'
        db.delete_column('budget_budget', 'auto_budget_id')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '14', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'accounts.journal': {
            'Meta': {'object_name': 'Journal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'budget.autobudget': {
            'Meta': {'object_name': 'AutoBudget'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '14', 'decimal_places': '2'}),
            'delta': ('django.db.models.fields.DecimalField', [], {'default': "'86400.0'", 'max_digits': '14', 'decimal_places': '2'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounts.Account']"}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounts.Account']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        'budget.budget': {
            'Meta': {'object_name': 'Budget'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '14', 'decimal_places': '2'}),
            'auto_budget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['budget.AutoBudget']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_applied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Journal']", 'null': 'True'}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounts.Account']"}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounts.Account']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['budget']
