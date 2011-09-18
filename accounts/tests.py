import decimal
from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account, Posting, Journal

class AccountTestCase(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
	self.user = User.objects.get(username='foobar')
	self.account = self.user.get_profile().accounts.create(name='Bank',
	    owner=self.user)
	self.cash = self.user.get_profile().accounts.create(name='Cash',
	    owner=self.user)

	self.paycheck = Account.objects.create(name='Paycheck',
	    owner=self.user)
	self.phone_bill = Account.objects.create(name='Phone Bill',
	    owner=self.user)
	self.credit_amt = decimal.Decimal('354.32')
	self.debit_amt = decimal.Decimal('75.64')
	self.transfer_amt = decimal.Decimal('50.00')

    def tearDown(self):
	self.account.delete()
	self.cash.delete()
	self.paycheck.delete()
	self.phone_bill.delete()
	
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
	td = timedelta(days=15)
	second = date.today()
	first = second - td
	third = second + td

	first_amt = self.credit_amt
	second_amt = first_amt - self.debit_amt
	third_amt = second_amt - self.transfer_amt
	zero = decimal.Decimal('0.00')
	days = timedelta(days=3)

	self.account.add_credit(first, self.paycheck, self.credit_amt)
	self.account.add_debit(second, self.phone_bill, self.debit_amt)
	self.account.add_transfer(third, self.cash, self.transfer_amt)

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
	    self.transfer_amt)

    def test_get_running_balance(self):
	td = timedelta(days=15)
	second = date.today()
	first = second - td
	third = second + td
	zero = decimal.Decimal('0.00')

	self.account.add_credit(first, self.paycheck, self.credit_amt)
	self.account.add_debit(second, self.phone_bill, self.debit_amt)
	self.account.add_transfer(third, self.cash, self.transfer_amt)

	bal = self.user.get_profile().accounts.get_running_balance(
	    first, third)
	for account in bal:
	    if account['name'] == 'Bank':
		acct = account

	first_amt = self.credit_amt
	second_amt = first_amt - self.debit_amt
	third_amt = second_amt - self.transfer_amt

	self.assertEqual(len(acct['postings']), 3)
	self.assertEqual(acct['balance'], self.account.balance)
	self.assertEqual(acct['postings'][0]['balance'], first_amt)
	self.assertEqual(acct['postings'][1]['balance'], second_amt)
	self.assertEqual(acct['postings'][2]['balance'], third_amt)

class PostingTestCase(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
	self.user = User.objects.get(username='foobar')
        self.account = self.user.get_profile().accounts.create(name='Bank',
            owner=self.user)
	self.paycheck = Account.objects.create(name='Paycheck',
	    owner=self.user)
	self.phone_bill = Account.objects.create(name='Phone Bill',
	    owner=self.user)

	self.credit_amt = decimal.Decimal('354.32')
	self.debit_amt = decimal.Decimal('75.64')
	self.account.add_credit(date.today(), self.paycheck, self.credit_amt)
	self.account.add_debit(date.today(), self.phone_bill, self.debit_amt)

    def tearDown(self):
	self.account.delete()
	self.paycheck.delete()
	self.phone_bill.delete()

    def test_posting_create(self):
	pay_credit = Posting.objects.get(account=self.account, amount__gt=0)
	pay_debit = Posting.objects.get(account=self.paycheck, amount__lt=0)

	self.assertEqual(pay_credit.amount, self.credit_amt)
	self.assertEqual(pay_debit.amount, -self.credit_amt)

	bill_credit = Posting.objects.get(account=self.phone_bill,
	    amount__gt=0)
	bill_debit = Posting.objects.get(account=self.account, amount__lt=0)

	self.assertEqual(bill_credit.amount, self.debit_amt)
	self.assertEqual(bill_debit.amount, -self.debit_amt)

	self.assertEqual(self.account.balance,
	    (self.credit_amt - self.debit_amt))
	self.assertEqual(self.paycheck.balance, -self.credit_amt)
	self.assertEqual(self.phone_bill.balance, self.debit_amt)

    def test_posting_delete(self):
	Posting.objects.filter(account=self.account).delete()
	self.assertFalse(Posting.objects.filter(account=self.account).exists())
	self.assertFalse(Posting.objects.filter(
	    account=self.paycheck).exists())
	self.assertFalse(Posting.objects.filter(
	    account=self.phone_bill).exists())
	self.assertFalse(Journal.objects.filter(type="Income").exists())
	self.assertFalse(Journal.objects.filter(type="Expense").exists())

