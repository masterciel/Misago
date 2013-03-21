from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.threads',
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'list.ThreadsListView', name="forum"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/(?P<page>\d+)/$', 'list.ThreadsListView', name="forum"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/new/$', 'posting.NewThreadView', name="thread_start"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/edit/$', 'posting.EditThreadView', name="thread_edit"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$', 'posting.NewReplyView', name="thread_reply"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<quote>\d+)/reply/$', 'posting.NewReplyView', name="thread_reply"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/edit/$', 'posting.EditReplyView', name="post_edit"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/$', 'thread.ThreadView', name="thread"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<page>\d+)/$', 'thread.ThreadView', name="thread"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/last/$', 'jumps.LastReplyView', name="thread_last"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/find-(?P<post>\d+)/$', 'jumps.FindReplyView', name="thread_find"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/new/$', 'jumps.NewReplyView', name="thread_new"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/moderated/$', 'jumps.FirstModeratedView', name="thread_moderated"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reported/$', 'jumps.FirstReportedView', name="thread_reported"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/show-hidden/$', 'jumps.ShowHiddenRepliesView', name="thread_show_hidden"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/watch/$', 'jumps.WatchThreadView', name="thread_watch"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/watch/email/$', 'jumps.WatchEmailThreadView', name="thread_watch_email"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/unwatch/$', 'jumps.UnwatchThreadView', name="thread_unwatch"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/unwatch/email/$', 'jumps.UnwatchEmailThreadView', name="thread_unwatch_email"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/upvote/$', 'jumps.UpvotePostView', name="post_upvote"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/downvote/$', 'jumps.DownvotePostView', name="post_downvote"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/delete/$', 'delete.DeleteThreadView', name="thread_delete", kwargs={'mode': 'delete_thread'}),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/hide/$', 'delete.HideThreadView', name="thread_hide", kwargs={'mode': 'hide_thread'}),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/delete/$', 'delete.DeleteReplyView', name="post_delete", kwargs={'mode': 'delete_post'}),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/hide/$', 'delete.HideReplyView', name="post_hide", kwargs={'mode': 'hide_post'}),
)

urlpatterns += patterns('misago.apps.errors',
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/info/$', 'error_not_implemented', name="post_info"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/votes/$', 'error_not_implemented', name="post_votes"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/$', 'error_not_implemented', name="changelog"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/$', 'error_not_implemented', name="changelog_diff"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/revert/$', 'error_not_implemented', name="changelog_revert"),
)
