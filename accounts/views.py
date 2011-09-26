import decimal
import datetime
import json

from django.db import transaction
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from accounts.forms import AccountAddForm, AccountTransferForm, VoidForm
from accounts.models import Posting

@login_required
def account_list(request):
    profile = request.user.get_profile()
    start_date = profile.start_date
    end_date = profile.end_date
    accounts = profile.accounts.all().get_running_balance(start_date, end_date)

    c = RequestContext(request, {
	'accounts': accounts,
    })

    return render(request, 'accounts/account_list.html', context_instance=c)

@login_required
def account_range(request):
    start_year = int(request.GET.get('start_year'))
    start_month = int(request.GET.get('start_month'))
    start_day = int(request.GET.get('start_day'))
    end_year = int(request.GET.get('end_year'))
    end_month = int(request.GET.get('end_month'))
    end_day = int(request.GET.get('end_day'))

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    profile = request.user.get_profile()
    accounts = profile.accounts.all().get_running_balance(start_date, end_date)

    c = RequestContext(request, {
	'accounts': accounts,
    })
    return render(request, "accounts/account_list.html", context_instance=c)
	    
@transaction.commit_on_success
@login_required
def account_add(request):
    user = request.user
    profile = user.get_profile()
    total = profile.get_total_balance()

    if request.method == 'POST':
	form = AccountAddForm(request.POST)
	if form.is_valid():
	    form.process(user.id)
	    return redirect('/accounts/')
    else:
	form = AccountAddForm()

    c = RequestContext(request, {
	'form': form,
    })

    return render(request, 'accounts/account_add.html', context_instance=c)

@transaction.commit_on_success
@login_required
def account_transfer(request):
    user = request.user
    profile = user.get_profile()
    total = profile.get_total_balance()

    if request.method == 'POST':
	form = AccountTransferForm(request.POST)
	if form.is_valid():
	    form.process(user.id)
	    return redirect('/accounts/')
    else:
	form = AccountTransferForm()

    c = RequestContext(request, {
	'form': form,
    })

    return render(request, 'accounts/account_transfer.html',
	context_instance=c)

@login_required
def account_view(request, account_id):
    user = request.user
    profile = user.get_profile()
    total = profile.get_total_balance()
    account_q = profile.accounts.get(id=account_id)

    account = {}
    account['id'] = account_q.id
    account['name'] = account_q.name
    account['balance'] = account_q.balance
    account['postings'] = []

    posting_q = Posting.objects.order_by('date').filter(
	account__id=account['id'])
    running_balance = decimal.Decimal('0.00')
    for posting in posting_q:
	date = posting.date
	journal_id = posting.journal.id
	name = Posting.objects.filter(journal__id=journal_id).exclude(
	    id=posting.id)[0].account.name
	amount = posting.amount
	running_balance += amount
	account['postings'].append({
	    'date': date,
	    'name': name,
	    'amount': amount,
	    'balance': running_balance,
	})

    c = RequestContext(request, {
	'account': account,
    })

    return render(request, 'accounts/account_view.html', context_instance=c)

@transaction.commit_on_success
@login_required
def account_void(request):
    if request.method == 'POST':
	form = VoidForm(request.POST)
	if form.is_valid():
	    form.process()
	    
    return redirect('/accounts/')

