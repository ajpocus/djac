from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Accountant.views.home', name='home'),
    # url(r'^Accountant/', include('Accountant.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout',
        kwargs={'next_page': '/accounts/'}),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^incomes/', include('incomes.urls')),
    url(r'^expenses/', include('expenses.urls')),
    url(r'^budget/', include('budget.urls')),
)
