from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    url(r'^$', 'account_list'),
    url(r'^json/', 'account_json'),
    url(r'^add/', 'account_add'),
    url(r'^transfer/', 'account_transfer'),
    url(r'^view/(?P<account_id>\d*)/', 'account_view'),
)

