import decimal
import datetime

from django.db import models
from django.db import transaction
from django.db.models import Sum, Manager
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save, post_save, pre_delete


class Journal(models.Model):
    type = models.CharField(max_length=128)

    def __unicode__(self):
        return self.type


class Posting(models.Model):
    date = models.DateField(default=datetime.date.today)
    amount = models.DecimalField(max_digits=14, decimal_places=2,
	default=decimal.Decimal('0.00'))
    account = models.ForeignKey('Account')
    journal = models.ForeignKey(Journal)

    def __unicode__(self):
	return "%s, %.2f, %s" % (self.date, self.amount, self.account.name)


def posting_pre_save(sender, instance, **kwargs):
    try:
	instance.before_save = Posting.objects.get(id=instance.id)
    except Posting.DoesNotExist:
	instance.before_save = None

def posting_post_save(sender, instance, created, **kwargs):
    if created:
	account = instance.account
	amount = decimal.Decimal(instance.amount)
	account.balance += amount
	account.save()
    else:
	before_save = instance.before_save
	account = instance.account
	if before_save.amount != instance.amount:
	    old_amt = decimal.Decimal(before_save.amount)
	    new_amt = decimal.Decimal(instance.amount)
	    if old_amt < new_amt:
		amount = new_amt - old_amt
		account.balance += amount
		account.save()
	    else:
		amount = old_amt - new_amt
		account.balance -= amount
		account.save()

def posting_pre_delete(sender, instance, **kwargs):
    instance.account.balance -= instance.amount
    instance.account.save()

pre_save.connect(posting_pre_save, sender=Posting)
post_save.connect(posting_post_save, sender=Posting)
pre_delete.connect(posting_pre_delete, sender=Posting)


# I used a custom QuerySet to allow filter chaining, rather than attaching the
# method to Account.objects through AccountManager.
class AccountQuerySet(QuerySet):
    def get_running_balance(self, start_date, end_date):
        accounts = []

        for account in self:
            posting_list = Posting.objects.order_by('date').filter(
                account=account).filter(
                date__gte=start_date).filter(
                date__lte=end_date)

            postings = []
            running_balance = account.get_balance_on(start_date)
            for posting in posting_list:
                name = Posting.objects.filter(journal=posting.journal).exclude(
                    account=account)[0].account.name
                running_balance += posting.amount
                postings.append({
                    'date': posting.date.strftime("%M %d, %Y"),
                    'name': name,
                    'amount': posting.amount,
                    'balance': running_balance,
                })

            accounts.append({
                'id': account.id,
                'name': account.name,
                'balance': account.balance,
                'postings': postings,
            })

        return accounts


class AccountManager(Manager):
    def get_query_set(self):
        return AccountQuerySet(self.model)


class Account(models.Model):
    name = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=14, decimal_places=2,
	default=decimal.Decimal('0.00'))
    objects = AccountManager()

    def __unicode__(self):
	return "%s: %.2f" % (self.name, self.balance)

    def get_balance_on(self, date):
	postings = Posting.objects.filter(account__id=self.id).filter(
	    date__lte=date)
	credits = postings.filter(amount__gt=0)
	debits = postings.filter(amount__lt=0)

	if credits and debits:
	    credit_total = credits.aggregate(Sum('amount'))['amount__sum']
	    debit_total = debits.aggregate(Sum('amount'))['amount__sum']
	    total = credit_total + debit_total
	    return self.balance - total
	else:
	    total = decimal.Decimal('0.00')
	    return total

    def add_credit(self, date, name, amount):
	# get_or_create returns (account, success) tuple
	payer = Account.objects.get_or_create(name=name)[0]

        journal = Journal(type="Income")
        journal.save()

        credit_amt = amount.to_eng_string()
        debit_amt = '-' + credit_amt

        debit = Posting.objects.create(date=date, amount=debit_amt,
	    account=payer, journal=journal)
        credit = Posting.objects.create(date=date, amount=credit_amt,
	    account=self, journal=journal)

    def add_debit(self, date, name, amount):
	# get_or_create returns (account, success) tuple
	payee = Account.objects.get_or_create(name=name)[0]

        journal = Journal(type="Expense")
        journal.save()

        credit_amt = amount.to_eng_string()
        debit_amt = '-' + credit_amt

        debit = Posting.objects.create(date=date, amount=debit_amt,
	    account=self, journal=journal)
        credit = Posting.objects.create(date=date, amount=credit_amt,
	    account=payee, journal=journal)

    def add_transfer(self, date, name, amount):
	# get_or_create returns (account, success) tuple
	payee = Account.objects.get_or_create(name=name)[0]

	journal = Journal(type="Transfer")
	journal.save()
	credit_amt = amount.to_eng_string()
	debit_amt = '-' + credit_amt

	debit = Posting.objects.create(date=date, amount=debit_amt,
	    account=self, journal=journal)
	credit = Posting.objects.create(date=date, amount=credit_amt,
	    account=payee, journal=journal)


