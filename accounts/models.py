import decimal
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.db.models import Sum, Manager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save


class Journal(models.Model):
    type = models.CharField(max_length=128)

    def __unicode__(self):
        return self.type


class Void(Journal):
    original = models.ForeignKey(Journal, related_name='+')


class Posting(models.Model):
    date = models.DateField(default=datetime.date.today)
    amount = models.DecimalField(max_digits=14, decimal_places=2,
	default=decimal.Decimal('0.00'))
    account = models.ForeignKey('Account')
    journal = models.ForeignKey(Journal)

    def __unicode__(self):
	return "%s, %.2f, %s" % (self.date, self.amount, self.account.name)


def posting_post_save(sender, instance, created, **kwargs):
    if created:
	account = instance.account
	amount = decimal.Decimal(instance.amount)
	account.balance += amount
	account.save()

post_save.connect(posting_post_save, sender=Posting)

# I used a custom QuerySet to allow filter chaining with get_running_balance,
# rather than attaching the method to Account.objects through AccountManager.
class AccountQuerySet(QuerySet):
    def get_running_balance(self, start_date, end_date):
        accounts = []

        for account in self:
            posting_list = Posting.objects.select_related().order_by(
		'date').filter(
                account=account).filter(
                date__gte=start_date).filter(
                date__lte=end_date)

            postings = []
	    day = datetime.timedelta(days=1)
	    bal_start = start_date - day
            running_balance = account.get_balance_on(bal_start)
            for posting in posting_list:
                name = Posting.objects.select_related().order_by(
		    'date').filter(
		    journal=posting.journal).exclude(
                    account=account)[0].account.name
                running_balance += posting.amount
                postings.append({
                    'date': posting.date.strftime("%B %d, %Y"),
                    'name': name,
                    'amount': posting.amount,
                    'balance': running_balance,
		    'journal': posting.journal.id,
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

    def __getattr__(self, name):
	# This check stops a recursion depth problem described in Django
	# ticket #15062
	if name.startswith("_"):
	    raise AttributeError
	return getattr(self.get_query_set(), name)


class Account(models.Model):
    name = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=14, decimal_places=2,
	default=decimal.Decimal('0.00'))
    owner = models.ForeignKey(User)
    objects = AccountManager()

    def __unicode__(self):
	return "%s: %.2f" % (self.name, self.balance)

    def get_balance_on(self, date):
	postings = Posting.objects.order_by('date').filter(
	    account__id=self.id).filter(
	    date__lte=date)
	credits = postings.filter(amount__gt=0)
	debits = postings.filter(amount__lt=0)

	if credits.exists() or debits.exists():
	    credit_total = credits.aggregate(Sum('amount'))['amount__sum']
	    debit_total = debits.aggregate(Sum('amount'))['amount__sum']

	    if not credit_total:
		credit_total = decimal.Decimal('0.00')
	    if not debit_total:
		debit_total = decimal.Decimal('0.00')

	    total = credit_total + debit_total
	else:
	    total = decimal.Decimal('0.00')

	return total

    def add_credit(self, date, payer, amount):
        journal = Journal(type="Income")
        journal.save()

        credit_amt = amount.to_eng_string()
        debit_amt = '-' + credit_amt

        debit = Posting.objects.create(date=date, amount=debit_amt,
	    account=payer, journal=journal)
        credit = Posting.objects.create(date=date, amount=credit_amt,
	    account=self, journal=journal)

    def add_debit(self, date, payee, amount):
        journal = Journal(type="Expense")
        journal.save()

        credit_amt = amount.to_eng_string()
        debit_amt = '-' + credit_amt

        debit = Posting.objects.create(date=date, amount=debit_amt,
	    account=self, journal=journal)
        credit = Posting.objects.create(date=date, amount=credit_amt,
	    account=payee, journal=journal)

    def add_transfer(self, date, payee, amount):
	journal = Journal(type="Transfer")
	journal.save()

	credit_amt = amount.to_eng_string()
	debit_amt = '-' + credit_amt

	debit = Posting.objects.create(date=date, amount=debit_amt,
	    account=self, journal=journal)
	credit = Posting.objects.create(date=date, amount=credit_amt,
	    account=payee, journal=journal)


