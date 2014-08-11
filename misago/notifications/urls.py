from django.conf.urls import include, patterns, url


urlpatterns = patterns('misago.notifications.views',
    url(r'^notifications/$', 'notifications', name='notifications'),
    url(r'^notifications/event-sender/$', 'event_sender', name='notifications_event_sender'),
    url(r'^notifications/new/$', 'new_notification', name='new_notification'),
)
