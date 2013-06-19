from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.privatethreads',
    url(r'^$', 'list.ThreadsListView', name="private_threads"),
    url(r'^(?P<page>[1-9]([0-9]+)?)/$', 'list.ThreadsListView', name="private_threads"),
    url(r'^start/$', 'posting.NewThreadView', name="private_thread_start"),
    url(r'^start/(?P<username>\w+)-(?P<user>\d+)/$', 'posting.NewThreadView', name="private_thread_start_with"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/edit/$', 'posting.EditThreadView', name="private_thread_edit"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$', 'posting.NewReplyView', name="private_thread_reply"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<quote>\d+)/reply/$', 'posting.NewReplyView', name="private_thread_reply"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/edit/$', 'posting.EditReplyView', name="private_post_edit"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/$', 'thread.ThreadView', name="private_thread"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<page>[1-9]([0-9]+)?)/$', 'thread.ThreadView', name="private_thread"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/last/$', 'jumps.LastReplyView', name="private_thread_last"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/find-(?P<post>\d+)/$', 'jumps.FindReplyView', name="private_thread_find"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/new/$', 'jumps.NewReplyView', name="private_thread_new"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/reported/$', 'jumps.FirstReportedView', name="private_thread_reported"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/show-hidden/$', 'jumps.ShowHiddenRepliesView', name="private_thread_show_hidden"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/report/$', 'jumps.ReportPostView', name="private_post_report"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/show-report/$', 'jumps.ShowPostReportView', name="private_post_report_show"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/watch/$', 'jumps.WatchThreadView', name="private_thread_watch"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/watch/email/$', 'jumps.WatchEmailThreadView', name="private_thread_watch_email"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/unwatch/$', 'jumps.UnwatchThreadView', name="private_thread_unwatch"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/unwatch/email/$', 'jumps.UnwatchEmailThreadView', name="private_thread_unwatch_email"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/invite/$', 'jumps.InviteUserView', name="private_thread_invite_user"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/remove/$', 'jumps.RemoveUserView', name="private_thread_remove_user"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/delete/$', 'delete.DeleteThreadView', name="private_thread_delete"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/hide/$', 'delete.HideThreadView', name="private_thread_hide"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/show/$', 'delete.ShowThreadView', name="private_thread_show"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/delete/$', 'delete.DeleteReplyView', name="private_post_delete"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/hide/$', 'delete.HideReplyView', name="private_post_hide"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/show/$', 'delete.ShowReplyView', name="private_post_show"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/delete/$', 'delete.DeleteCheckpointView', name="private_post_checkpoint_delete"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/hide/$', 'delete.HideCheckpointView', name="private_post_checkpoint_hide"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/show/$', 'delete.ShowCheckpointView', name="private_post_checkpoint_show"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/info/$', 'details.DetailsView', name="private_post_info"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/$', 'changelog.ChangelogView', name="private_thread_changelog"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/$', 'changelog.ChangelogDiffView', name="private_thread_changelog_diff"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/revert/$', 'changelog.ChangelogRevertView', name="private_thread_changelog_revert"),
    # Extra search routes
    url(r'^search/$', 'search.search_private_threads', name="private_threads_search"),
    url(r'^search/results/$', 'search.show_private_threads_results', name="private_threads_search_results"),
)
