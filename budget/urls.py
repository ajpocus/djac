from django.conf.urls.defaults import *

urlpatterns = patterns('budget.views',
    url(r'^$', 'budget_list'),
    url(r'^applied', 'budget_list_applied'),
    url(r'^incomes/add', 'budget_add_income'),
    url(r'^expenses/add', 'budget_add_expense'),
    url(r'^apply/(?P<budget_id>\d*)/', 'budget_apply'),
)

