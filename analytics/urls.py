from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('analytics.views',
    url(r'^expenses/json/', 'analytics_expenses_json'),
    url(r'^expenses/', 'analytics_expenses_chart'),
)
