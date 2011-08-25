from datetime import date

from django import forms
from django.contrib.auth.models import User

from accounts.models import Account
from budget.models import Budget

class BudgetForm(forms.Form):
    """This provides a common base for BudgetExpenseForm and BudgetIncomeForm,
	which differ only in their process() methods.
    """

    date = forms.DateField()
    name = forms.CharField(max_length=64)
    amount = forms.DecimalField(max_digits=14, decimal_places=2)
    # One more field defined below, dependent on user ID supplied in form init.

    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('uid')
        super(BudgetForm, self).__init__(*args, **kwargs)
        if uid:
            user = User.objects.get(id=uid)
            profile = user.get_profile()
            self.fields['account'] = forms.ModelChoiceField(
                queryset=profile.accounts.all(),
            )


class BudgetIncomeForm(BudgetForm):
    def process(self, uid):
	data = self.cleaned_data
	user = User.objects.get(id=uid)
	profile = user.get_profile()

	# get_or_create returns (account, success) tuple
	payer = Account.objects.get_or_create(name=data['name'])[0]
	payee = data['account']
	date = data['date']
	amount = data['amount']
	budget = Budget.objects.create(payer=payer, payee=payee, date=date,
	    amount=amount)
	profile.budgets.add(budget)
	profile.save()


class BudgetExpenseForm(BudgetForm):
    def process(self, uid):
	data = self.cleaned_data
	user = User.objects.get(id=uid)
	profile = user.get_profile()

	payer = data['account']
	# get_or_create returns (account, success) tuple
	payee = Account.objects.get_or_create(name=data['name'])[0]
	date = data['date']
	amount = data['amount']
	budget = Budget.objects.create(payer=payer, payee=payee, date=date,
	    amount=amount)
	profile.budgets.add(budget)
	profile.save()


