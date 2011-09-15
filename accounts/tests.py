import decimal
from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account

class AccountTestCase(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
	self.user = User.objects.get(username='foobar')
	self.account = self.user.get_profile().accounts.get_or_create(
	    name='Bank', owner=self.user)[0]
	self.cash = self.user.get_profile().accounts.get_or_create(
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
	self.account.add_transfer(date.today(), self.cash, self.transfer_amt)
	balance = self.credit_amt - self.transfer_amt

	self.assertEqual(self.account.balance, balance)
	self.assertEqual(self.cash.balance, self.transfer_amt)

    def test_get_balance_on(self):
	second = date.today()
	first = second - timedelta(days=24)
	third = second + timedelta(days=15)

	self.account.add_credit(first, self.paycheck, self.credit_amt)
	self.account.add_debit(second, self.phone_bill, self.debit_amt)
	self.account.add_transfer(third, self.cash, self.transfer_amt)

	start_amt = self.credit_amt - self.debit_amt - self.transfer_amt
	first_amt = start_amt + self.credit_amt
	second_amt = first_amt - self.debit_amt
	third_amt = second_amt - self.transfer_amt
	zero = decimal.Decimal('0.00')
	days = timedelta(days=3)

	before_first = first - days
	after_first = first + days
	self.assertEqual(self.account.get_balance_on(before_first), zero)
	self.assertEqual(self.account.get_balance_on(after_first), first_amt)
	
	before_second = second - days
	after_second = second + days
	self.assertEqual(self.account.get_balance_on(before_second), first_amt)
	self.assertEqual(self.account.get_balance_on(after_second), second_amt)

	before_third = third - days
	after_third = third + days
	self.assertEqual(self.account.get_balance_on(before_third), second_amt)
	self.assertEqual(self.account.get_balance_on(after_third), third_amt)
	self.assertEqual(self.cash.get_balance_on(before_third), zero)
	self.assertEqual(self.cash.get_balance_on(after_third),
	    (self.transfer_amt * 2))

    def tearDown(self):
	self.user.delete()

