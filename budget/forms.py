import decimal
from datetime import date, timedelta

from django import forms
from django.contrib.auth.models import User
from budget.helpers import ordinal

from accounts.models import Account
from budget.models import Budget, AutoBudget


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


class AutoBudgetForm(forms.Form):
    frequency = forms.ChoiceField(choices=((n, ordinal(n))
	for n in xrange(2, 53)))
    delta = forms.ChoiceField(choices=(
        ('day', 'day'),
	('week', 'week'),
	('month', 'month'),
	('year', 'year'),
	('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ))
    start_date = forms.DateField(('%m/%d/%Y',),
        widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
            'class': 'input',
            'size': '15',
        })
    )
    end_date = forms.DateField(('%m/%d/%Y',),
        widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
            'class': 'input',
            'size': '15',
        })
    )
    name = forms.CharField()
    amount = forms.DecimalField(max_digits=14, decimal_places=2)

    def __init__(self, *args, **kwargs):
	self.uid = kwargs.pop('uid')
	super(AutoBudgetForm, self).__init__(*args, **kwargs)
	if self.uid:
            user = User.objects.get(id=self.uid)
            profile = user.get_profile()
            self.fields['account'] = forms.ModelChoiceField(
                queryset=profile.accounts.all(),
            )

    def get_tdelta(self, delta, freq):
        try:
            # delta involves a weekday
            freq = int(freq)
            now = date.today()
            day = now.weekday()

            # Weekday deltas use both a weeks and days value in the timedelta.
            # AutoBudgetForm.create_budgets takes this into account to give the
            # right dates.
            weeks = 1
            if day < freq:
                # the weekday is coming up this week
                days = (freq - day)
            else:
                days = (7 - (day - freq))

            tdelta = timedelta(days=days, weeks=weeks)

        except ValueError:
            # delta is one of (day, week, month)
            delta = ''.join([delta, 's'])
	    freq = int(freq)
            if delta == 'days':
		weeks = None
                tdelta = timedelta(days=freq)

            elif delta == 'weeks':
		weeks = freq
                tdelta = timedelta(weeks=freq)

            elif delta == 'months':
		weeks = None
                tdelta = timedelta(months=freq)

            else:
		weeks = None
                raise TypeError("Delta is a bad value.")

	return (tdelta, weeks)

    def create_budgets(self, auto, weeks):
	profile = User.objects.get(id=self.uid).get_profile()
	delta = timedelta(seconds=int(auto.delta))
        if weeks and delta.days:
            # weekday delta
            first_delta = timedelta(days=delta.days)
            first_date = auto.start_date + first_delta
            profile.budgets.create(date=first_date, amount=auto.amount,
                payer=auto.payer, payee=auto.payee, auto_budget=auto,
		is_applied=True)

            next_delta = timedelta(weeks=weeks)
            next_date = first_date + next_delta

	    if auto.end_date:
		end_date = auto.end_date
	    else:
		end_date = auto.start_date + timedelta(days=365)

	    while (next_date <= end_date):
		profile.budgets.create(date=next_date,
		    amount=auto.amount, payer=auto.payer, payee=auto.payee,
		    auto_budget=auto, is_applied=True)
		next_date += next_delta
        else:
            first_date = start_date
            profile.budgets.create(date=first_date, amount=auto.amount,
                payer=auto.payer, payee=auto.payee, auto_budget=auto,
		is_applied=True)
            next_date = first_date + delta
            while (next_date <= auto.end_date):
                profile.budgets.create(date=next_date,
		    amount=auto.amount, payer=auto.payer, payee=auto.payee,
		    auto_budget=auto, is_applied=True)
                next_date += delta


class AutoBudgetIncomeForm(AutoBudgetForm):
    def process(self, uid):
	data = self.cleaned_data
	delta = data['delta']
	freq = data['frequency']
	(tdelta, weeks) = self.get_tdelta(delta, freq)
	user = User.objects.get(id=uid)

	auto = AutoBudget()
	auto.payer = Account.objects.get_or_create(name=data['name'],
	    owner=user)[0]
	auto.payee = data['account']
	auto.delta = decimal.Decimal(tdelta.total_seconds())
	auto.amount = decimal.Decimal(data['amount'])
	auto.save()
	self.create_budgets(auto, weeks)

class AutoBudgetExpenseForm(AutoBudgetForm):
    def process(self, uid):
	data = self.cleaned_data
	delta = data['delta']
	freq = data['frequency']
	(tdelta, weeks) = self.get_tdelta(delta, freq)
	user = User.objects.get(id=uid)

	auto = AutoBudget()
	auto.payer = data['account']
	auto.payee = Account.objects.get_or_create(name=data['name'],
	    owner=user)[0]
	auto.delta = decimal.Decimal(tdelta.total_seconds())
	auto.amount = decimal.Decimal(data['amount'])
	auto.save()
	self.create_budgets(auto, weeks)


