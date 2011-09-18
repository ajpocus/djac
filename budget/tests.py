import decimal
from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from budget.models import Budget
from accounts.models import Account, Posting

class BudgetTestCase(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
	self.user = User.objects.get(username='foobar')
	accounts = self.user.get_profile().accounts
	self.account = accounts.create(name='Bank', owner=self.user)
	self.check = Account.objects.create(name='Check', owner=self.user)

	self.payday = date.today() + timedelta(days=7)
	self.check_amt = decimal.Decimal('354.32')
	self.budget = Budget.objects.create(date=self.payday, payer=self.check,
	    payee=self.account, amount=self.check_amt)

    def tearDown(self):
	self.account.delete()
	self.check.delete()
	self.budget.delete()

    def test_not_applied(self):
	zero = decimal.Decimal('0.00')
	self.assertEqual(self.account.balance, zero)
	self.assertEqual(self.check.balance, zero)
	self.assertIsNone(self.budget.journal)
	self.assertFalse(self.budget.is_applied)

    def test_is_applied(self):
	self.budget.is_applied = True
	self.budget.save()

	self.assertEqual(self.account.balance, self.check_amt)
	self.assertEqual(self.check.balance, -self.check_amt)
	self.assertIsNotNone(self.budget.journal)

	postings = Posting.objects.filter(journal=self.budget.journal)
	credit = postings.get(amount__gt=0)
	debit = postings.get(amount__lt=0)
	self.assertEqual(credit.amount, self.check_amt)
	self.assertEqual(debit.amount, -self.check_amt)


