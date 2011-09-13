import decimal
import datetime

from django import forms
from django.contrib.auth.models import User

from accounts.models import Account
from accounts.forms import TransactionForm

class IncomeAddForm(TransactionForm):
    def process(self, uid, account_id):
        data = self.cleaned_data
        user = User.objects.get(id=uid)
        profile = user.get_profile()

        name = data['name']
        amount = data['amount']
        date = data['date']

	account = profile.accounts.get(id=account_id)
	payer = Account.objects.get_or_create(name=name, owner=user)[0]
	account.add_credit(date=date, payer=payer, amount=amount)

