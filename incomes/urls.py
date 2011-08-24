from django.conf.urls.defaults import *

urlpatterns = patterns('incomes.views',
    url(r'^$', 'income_list'),
    url(r'^add/(?P<account_id>\d*)/', 'income_add'),
)
