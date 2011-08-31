from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    url(r'^$', 'account_list'),
    url(r'^range/', 'account_range'),
    url(r'^add/', 'account_add'),
    url(r'^transfer/', 'account_transfer'),
    url(r'^view/(?P<account_id>\d*)/', 'account_view'),
)

