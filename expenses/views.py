import decimal

from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect

from accounts.models import Posting
from expenses.forms import ExpenseAddForm

@login_required
def expense_list(request):
    profile = request.user.get_profile()
    account_q = profile.accounts.all()

    accounts = []
    for account in account_q:
	posting_q = Posting.objects.order_by('date').filter(
	    account=account).filter(amount__lt=0)

	expenses = []
	running_total = decimal.Decimal('0.00')
	for posting in posting_q:
	    amount = posting.amount
	    date = posting.date
	    journal = posting.journal.id
	    name = Posting.objects.filter(journal__id=journal).exclude(
		id=posting.id)[0].account.name
	    running_total += amount
	    expenses.append({
		'name': name,
		'date': date,
		'amount': amount,
		'total': running_total,
	    })

	accounts.append({
	    'id': account.id,
	    'name': account.name,
	    'balance': account.balance,
	    'expenses': expenses,
	})

    c = RequestContext(request, {
	'accounts': accounts,
    })

    return render(request, 'expenses/expense_list.html', context_instance=c)

@transaction.commit_on_success
@login_required
def expense_add(request, account_id):
    if request.method == 'POST':
	form = ExpenseAddForm(request.POST)
	if form.is_valid():
	    form.process(request.user.id, account_id)
	    return redirect('/expenses/')
    else:
	form = ExpenseAddForm()

    c = RequestContext(request, {
	'form': form,
    })

    return render(request, 'expenses/expense_add.html', context_instance=c)

