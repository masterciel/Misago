from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.search.views',
    url(r'^$', 'search', name="search"),
    url(r'^results/$', 'show_results', name="search_results"),
)