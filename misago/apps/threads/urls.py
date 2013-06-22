from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.threads',
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'list.ThreadsListView', name="forum"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/(?P<page>[1-9]([0-9]+)?)/$', 'list.ThreadsListView', name="forum"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/start/$', 'posting.NewThreadView', name="thread_start"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/edit/$', 'posting.EditThreadView', name="thread_edit"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$', 'posting.NewReplyView', name="thread_reply"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<quote>\d+)/reply/$', 'posting.NewReplyView', name="thread_reply"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/edit/$', 'posting.EditReplyView', name="post_edit"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/$', 'thread.ThreadView', name="thread"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<page>[1-9]([0-9]+)?)/$', 'thread.ThreadView', name="thread"),
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
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/report/$', 'jumps.ReportPostView', name="post_report"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/show-report/$', 'jumps.ShowPostReportView', name="post_report_show"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/delete/$', 'delete.DeleteThreadView', name="thread_delete"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/hide/$', 'delete.HideThreadView', name="thread_hide"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/show/$', 'delete.ShowThreadView', name="thread_show"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/delete/$', 'delete.DeleteReplyView', name="post_delete"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/hide/$', 'delete.HideReplyView', name="post_hide"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/show/$', 'delete.ShowReplyView', name="post_show"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/delete/$', 'delete.DeleteCheckpointView', name="post_checkpoint_delete"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/hide/$', 'delete.HideCheckpointView', name="post_checkpoint_hide"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/show/$', 'delete.ShowCheckpointView', name="post_checkpoint_show"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/info/$', 'details.DetailsView', name="post_info"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/votes/$', 'details.KarmaVotesView', name="post_votes"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/$', 'changelog.ChangelogView', name="thread_changelog"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/$', 'changelog.ChangelogDiffView', name="thread_changelog_diff"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/revert/$', 'changelog.ChangelogRevertView', name="thread_changelog_revert"),
    # Searching
    url(r'^search/$', 'search.SearchView', name="search"),
    url(r'^search/results/$', 'search.ResultsView', name="search_results"),
    url(r'^search/results/(?P<page>[1-9]([0-9]+)?)/$', 'search.ResultsView', name="search_results"),
)
