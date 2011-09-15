import decimal

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account

class AccountTestCase(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
	self.user = User.objects.get(username="foobar")
	self.account = self.user.get_profile().accounts.get_or_create(
	    name='Test', owner=self.user)[0]

    def test_balance_init(self):
	self.assertEqual(self.account.balance, decimal.Decimal('0.00'))
	
    def tearDown(self):
	self.user.delete()

