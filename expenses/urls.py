from django.conf.urls.defaults import *

urlpatterns = patterns('expenses.views',
    url(r'^$', 'expense_list'),
    url(r'^add/(?P<account_id>\d*)/', 'expense_add'),
)
