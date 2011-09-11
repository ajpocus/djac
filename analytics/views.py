import json
import decimal

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render

from accounts.models import Posting

def analytics_expenses_chart(request):
    c = RequestContext(request)
    return render(request, 'analytics/analytics_expenses_chart.html',
	context_instance=c)

def analytics_expenses_json(request):
    percents = {}
    total = decimal.Decimal('0.00')
    for account in request.user.get_profile().accounts.all():
	for posting in Posting.objects.order_by('date').filter(
	    account=account).filter(amount__lt=0):
		total -= posting.amount
		other = Posting.objects.filter(
		    journal=posting.journal).exclude(id=posting.id)[0]
		name = other.account.name
		if not name in percents:
		    percents[name] = decimal.Decimal('0.00')
		percents[name] -= posting.amount

    for name in percents:
	percents[name] /= total
	percents[name] = float(percents[name])

    return HttpResponse(json.dumps(percents), mimetype="application/json")

