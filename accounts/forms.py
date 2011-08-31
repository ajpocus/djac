from django import forms
from django.contrib.auth.models import User
from accounts.models import Account

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
    amount = forms.DecimalField(max_digits=14, decimal_places=2)

    def process(self, uid):
	user = User.objects.get(id=uid)
	profile = user.get_profile()
	accounts = profile.accounts
	data = self.cleaned_data

	payer = data['payer']
	payee = data['payee']
	amount = data['amount']

	profile.add_transfer(payer, payee, amount)
