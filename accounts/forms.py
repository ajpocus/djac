import datetime

from django import forms
from django.contrib.auth.models import User
from accounts.models import Account, Journal, Void, Posting

class AccountAddForm(forms.ModelForm):
    name = forms.CharField(max_length=64, label='Account Name')
    class Meta:
        model = Account
        fields = ('name',)

    def process(self, uid):
        data = self.cleaned_data
        name = data['name']
        user = User.objects.get(id=uid)
        profile = user.get_profile()
        accounts = profile.accounts

        account = Account(name=name, owner=user)
        account.save()
        accounts.add(account)
        profile.save()
        user.save()


class AccountTransferForm(forms.Form):
    payer = forms.CharField(max_length=64)
    payee = forms.CharField(max_length=64)
    date = forms.DateField(('%m/%d/%Y',),
        widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
            'class': 'input',
            'size': '15',
        })
    )
    amount = forms.DecimalField(max_digits=14, decimal_places=2)

    def process(self, uid):
	user = User.objects.get(id=uid)
	profile = user.get_profile()
	accounts = profile.accounts
	data = self.cleaned_data

	payer = data['payer']
	payee = data['payee']
	amount = data['amount']

	payer = accounts.get_or_create(name=payer, owner=user)[0]
	payee = accounts.get_or_create(name=payee, owner=user)[0]
	payer.add_transfer(data['date'], payee, amount)


class TransactionForm(forms.Form):
    name = forms.CharField(max_length=64)
    amount = forms.DecimalField(max_digits=14, decimal_places=2)
    date = forms.DateField(('%m/%d/%Y',),
        widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
            'class': 'input',
            'size': '15',
        })
    )

    def clean(self):
        super(TransactionForm, self).clean()
        data = self.cleaned_data
        date = data['date']
        today = datetime.date.today()
        if date > today:
            raise forms.ValidationError("This date is in the future.")

        return data

    def process(self, uid, account_id):
        data = self.cleaned_data
        user = User.objects.get(id=uid)
        profile = user.get_profile()

        name = data['name']
        amount = data['amount']
        date = data['date']


class VoidForm(forms.Form):
    journal = forms.IntegerField(initial='')

    def process(self):
	data = self.cleaned_data
	journal_id = data['journal']
	journal = Journal.objects.get(id=journal_id)

	postings = Posting.objects.select_related().filter(journal=journal)
        credit = postings.get(amount__gt=0)
        debit = postings.get(amount__lt=0)

        today = datetime.date.today()
        amount = credit.amount
        void = Void.objects.create(original=journal)
        void_debit = Posting(date=today, account=credit.account,
	    amount=-amount, journal=void)
        void_credit = Posting(date=today, account=debit.account, amount=amount,
	    journal=void)
	void_debit.save()
	void_credit.save()
	
