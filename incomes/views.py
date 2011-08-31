import decimal

from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect

from accounts.models import Posting, Journal
from incomes.forms import IncomeAddForm

@login_required
def income_list(request):
    profile = request.user.get_profile()
    account_q = profile.accounts.all()

    accounts = []
    for account in account_q:
	posting_q = Posting.objects.order_by('date').filter(
	    account=account).filter(amount__gt=0)
	total_income = sum([posting.amount for posting in posting_q])
	running_total = decimal.Decimal('0.00')

	incomes = []
	for posting in posting_q:
	    amount = posting.amount
	    date = posting.date
	    journal = posting.journal.id
	    name = Posting.objects.filter(journal__id=journal).exclude(
		id=posting.id)[0].account.name
	    running_total += posting.amount
	    incomes.append({
		'name': name,
		'date': date,
		'amount': amount,
		'total': running_total,
	    })

	accounts.append({
	    'id': account.id,
	    'name': account.name,
	    'balance': account.balance,
	    'incomes': incomes,
	})

    c = RequestContext(request, {
	'accounts': accounts,
    })

    return render(request, 'incomes/income_list.html', context_instance=c)

@transaction.commit_on_success
@login_required
def income_add(request, account_id):
    if request.method == 'POST':
	form = IncomeAddForm(request.POST)
	if form.is_valid():
	    form.process(request.user.id, account_id)
	    return redirect('/incomes/')
    else:
	form = IncomeAddForm()

    c = RequestContext(request, {
	'form': form,
    })

    return render(request, 'incomes/income_add.html', context_instance=c)

