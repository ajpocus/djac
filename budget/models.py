import decimal
from datetime import date, timedelta

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete

from accounts.models import Account, Journal, Posting


class AutoBudget(models.Model):
    delta = models.DecimalField(max_digits=14, decimal_places=2,
	default=decimal.Decimal('86400.0'))
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2,
	default=decimal.Decimal('0.00'))
    payer = models.ForeignKey(Account, related_name='+')
    payee = models.ForeignKey(Account, related_name='+')


class Budget(models.Model):
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=14, decimal_places=2,
	default='0.00')
    payer = models.ForeignKey(Account, related_name='+')
    payee = models.ForeignKey(Account, related_name='+')
    journal = models.ForeignKey(Journal, null=True)
    is_applied = models.BooleanField(default=False)
    auto_budget = models.ForeignKey(AutoBudget, null=True)

    def __unicode__(self):
	return "%s, %s, from %s to %s" % (self.date, self.amount,
	    self.payer.name, self.payee.name)

def budget_pre_save(sender, instance, **kwargs):
    try:
	instance.before_save = Budget.objects.get(id=instance.id)
    except Budget.DoesNotExist:
	instance.before_save = None

def budget_post_save(sender, instance, **kwargs):
    if (instance.before_save and 
	instance.is_applied != instance.before_save.is_applied):
	if instance.is_applied:
	    payer = instance.payer
	    payee = instance.payee
	    if (payer.userprofile_set.exists() and
		payee.userprofile_set.exists()):
		journal = Journal.objects.create(type="Transfer")
	    elif payer.userprofile_set.exists():
		journal = Journal.objects.create(type="Expense")
	    elif payee.userprofile_set.exists():
		journal = Journal.objects.create(type="Income")

	    credit_amt = instance.amount.to_eng_string()
	    debit_amt = '-' + credit_amt

	    credit = Posting.objects.create(date=instance.date,
		journal=journal, amount=credit_amt, account=instance.payee)
	    debit = Posting.objects.create(date=instance.date, journal=journal,
		amount=debit_amt, account=instance.payer)

	    instance.journal = journal
	    instance.save()

	else:
	    journal = instance.journal
	    Posting.objects.filter(journal=journal).delete()
	    instance.journal = None
	    instance.save()


pre_save.connect(budget_pre_save, sender=Budget)
post_save.connect(budget_post_save, sender=Budget)

