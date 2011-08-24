import decimal

from django.db import transaction
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404

from budget.forms import BudgetIncomeForm, BudgetExpenseForm
from budget.models import Budget

@login_required
def budget_list(request):
    profile = request.user.get_profile()
    start_date = profile.start_date
    end_date = profile.end_date
    account_q = profile.accounts.all()
    budget_q = profile.budgets.order_by('date').filter(
	date__gte=start_date).filter(
	date__lte=end_date).filter(
	is_applied=False)

    accounts = []
    budgets = []
    balance = {}
    for account in account_q:
	balance[account.id] = account.get_balance_on(start_date)
	accounts.append({
	    'name': account.name,
	    'balance': balance[account.id],
	})

    for budget in budget_q:
	payer = budget.payer
	payee = budget.payee
	amount = budget.amount
	if account_q.filter(id=payee.id).exists():
	    balance[payee.id] += amount
	    budget_balance = balance[payee.id]
	    account = payee.name
	    name = payer.name
	elif account_q.filter(id=payer.id).exists():
	    balance[payer.id] -= amount
	    budget_balance = balance[payer.id]
	    account = payer.name
	    name = payee.name

	budgets.append({
	    'id': budget.id,
	    'date': budget.date,
	    'name': name,
	    'amount': amount,
	    'account': account,
	    'balance': budget_balance,
	})

    c = RequestContext(request, {
	'accounts': accounts,
	'budgets': budgets,
    })

    return render(request, 'budget/budget_list.html', context_instance=c)

@login_required
def budget_list_applied(request):
    profile = request.user.get_profile()
    account_q = profile.accounts.all()
    budget_q = profile.budgets.order_by('date').filter(
	date__gte=start_date).filter(
	date__lte=end_date).filter(
	is_applied=True)

    budgets = []
    for budget in budget_q:
	payer = budget.payer
        payee = budget.payee
        amount = budget.amount
        
	if account_q.filter(id=payee.id).exists():
            account = payee.name
            name = payer.name
        elif account_q.filter(id=payer.id).exists():
            account = payer.name
            name = payee.name

	budgets.append({
	    'id': budget.id,
	    'date': budget.date,
	    'name': name,
	    'account': account,
	    'amount': amount,
	})

    c = RequestContext(request, {
	'budgets': budgets,
    })

    return render(request, 'budget/budget_list_applied.html',
	context_instance=c)

@transaction.commit_on_success
@login_required
def budget_add_income(request):
    if request.method == 'POST':
	form = BudgetIncomeForm(request.POST, uid=user.id)
	if form.is_valid():
	    form.process(user.id)
	    return redirect('/budget/')
    else:
	form = BudgetIncomeForm(uid=user.id)

    c = RequestContext(request, {
	'form': form,
    })

    return render(request, 'budget/budget_add.html', context_instance=c)

@transaction.commit_on_success
@login_required
def budget_add_expense(request):
    if request.method == 'POST':
	form = BudgetExpenseForm(request.POST, uid=user.id)
	if form.is_valid():
	    form.process(user.id)
	    return redirect('/budget/')
    else:
	form = BudgetExpenseForm(uid=user.id)

    c = RequestContext(request, {
	'form': form,
    })

    return render(request, 'budget/budget_add.html', context_instance=c)

@transaction.commit_on_success
@login_required
def budget_apply(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    budget.is_applied = not budget.is_applied
    budget.save()
    return redirect('/budget/')

