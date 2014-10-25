from django.conf.urls import patterns, include, url


from misago.threads.views.threads import ForumView
urlpatterns = patterns('',
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/(?P<page>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/sort-(?P<sort>[\w-]+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/sort-(?P<sort>[\w-]+)/(?P<page>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/show-(?P<show>[\w-]+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', ForumView.as_view(), name='forum'),
)


from misago.threads.views.threads import (ThreadView, GotoLastView,
                                          GotoNewView, GotoReportedView,
                                          GotoModeratedView, GotoPostView)
urlpatterns += patterns('',
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/$', ThreadView.as_view(), name='thread'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/(?P<page>\d+)/$', ThreadView.as_view(), name='thread'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/last/$', GotoLastView.as_view(), name='thread_last'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/new/$', GotoNewView.as_view(), name='thread_new'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/reported/$', GotoReportedView.as_view(), name='thread_reported'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/moderated/$', GotoModeratedView.as_view(), name='thread_moderated'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/post-(?P<post_id>\d+)/$', GotoPostView.as_view(), name='thread_post'),
)


from misago.threads.views.threads import StartThreadView, ReplyView, EditView
urlpatterns += patterns('',
    url(r'^start-thread/(?P<forum_id>\d+)/$', StartThreadView.as_view(), name='start_thread'),
    url(r'^reply-thread/(?P<forum_id>\d+)/(?P<thread_id>\d+)/$', ReplyView.as_view(), name='reply_thread'),
)


# new threads lists
from misago.threads.views.newthreads import NewThreadsView, clear_new_threads
urlpatterns += patterns('',
    url(r'^new-threads/$', NewThreadsView.as_view(), name='new_threads'),
    url(r'^new-threads/(?P<page>\d+)/$', NewThreadsView.as_view(), name='new_threads'),
    url(r'^new-threads/sort-(?P<sort>[\w-]+)$', NewThreadsView.as_view(), name='new_threads'),
    url(r'^new-threads/sort-(?P<sort>[\w-]+)(?P<page>\d+)/$', NewThreadsView.as_view(), name='new_threads'),
    url(r'^new-threads/clear/$', clear_new_threads, name='clear_new_threads'),
)


# unread threads lists
from misago.threads.views.unreadthreads import (UnreadThreadsView,
                                                clear_unread_threads)
urlpatterns += patterns('',
    url(r'^unread-threads/$', UnreadThreadsView.as_view(), name='unread_threads'),
    url(r'^unread-threads/(?P<page>\d+)/$', UnreadThreadsView.as_view(), name='unread_threads'),
    url(r'^unread-threads/sort-(?P<sort>[\w-]+)$', UnreadThreadsView.as_view(), name='unread_threads'),
    url(r'^unread-threads/sort-(?P<sort>[\w-]+)(?P<page>\d+)/$', UnreadThreadsView.as_view(), name='unread_threads'),
    url(r'^unread-threads/clear/$', clear_unread_threads, name='clear_unread_threads'),
)


# events moderation
from misago.threads.views.events import EventsView
urlpatterns += patterns('',
    url(r'^edit-event/(?P<event_id>\d+)/$', EventsView.as_view(), name='edit_event'),
)
