import decimal
from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account

class AccountTestCase(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
	self.user = User.objects.get(username='foobar')
	self.account = self.user.get_profile().accounts.get_or_create(
	    name='Bank', owner=self.user)[0]
	self.account = self.user.get_profile().accounts.get_or_create(
	    name='Cash', owner=self.user)[0]

	self.paycheck = Account.objects.create(name='Paycheck',
	    owner=self.user)
	self.phone_bill = Account.objects.create(name='Phone Bill',
	    owner=self.user)
	self.credit_amt = decimal.Decimal('354.32')
	self.debit_amt = decimal.Decimal('75.64')
	self.transfer_amt = decimal.Decimal('50.00')

    def test_add_credit(self):
	self.account.add_credit(date.today(), self.paycheck, self.credit_amt)

	self.assertEqual(self.account.balance, self.credit_amt)
	self.assertEqual(self.paycheck.balance, -self.credit_amt)

    def test_add_debit(self):
	self.account.add_credit(date.today(), self.paycheck, self.credit_amt)
	self.account.add_debit(date.today(), self.phone_bill, self.debit_amt)

	self.assertEqual(self.account.balance,
	    (self.credit_amt - self.debit_amt))
	self.assertEqual(self.phone_bill.balance, self.debit_amt)

    def test_add_transfer(self):
	self.account.add_credit(date.today(), self.paycheck, self.credit_amt)
	self.account.add_transfer(date.today(), 

    def tearDown(self):
	self.user.delete()

