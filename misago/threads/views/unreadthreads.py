from datetime import timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from misago.core.uiviews import uiview
from misago.users.decorators import deny_guests
from django.db.models import F
from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.threads.models import Thread
from misago.threads.permissions import exclude_invisible_threads
from misago.threads.views.generic.threads import Threads, ThreadsView


class UnreadThreads(Threads):
    def get_queryset(self):
        cutoff_days = settings.MISAGO_FRESH_CONTENT_PERIOD
        cutoff_date = timezone.now() - timedelta(days=cutoff_days)
        if cutoff_date < self.user.joined_on:
            cutoff_date = self.user.joined_on

        queryset = Thread.objects.filter(last_post_on__gte=cutoff_date)
        queryset = queryset.select_related('forum')
        queryset = queryset.filter(threadread__user=self.user)
        queryset = queryset.filter(
            threadread__last_read_on__lt=F('last_post_on'))
        queryset = exclude_invisible_threads(queryset, self.user)
        return queryset


class UnreadThreadsView(ThreadsView):
    link_name = 'misago:unread_threads'
    template = 'misago/threads/unread.html'

    Threads = UnreadThreads

    def process_context(self, request, context):
        context['show_threads_locations'] = True
        context['fresh_period'] = settings.MISAGO_FRESH_CONTENT_PERIOD

        if request.user.unread_threads != context['threads_count']:
            request.user.unread_threads.set(context['threads_count'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            message = _("You have to sign in to see your list of "
                        "threads with unread replies.")
            raise PermissionDenied(message)
        else:
            return super(UnreadThreadsView, self).dispatch(
                request, *args, **kwargs)


@uiview("unread_threads")
@deny_guests
def event_sender(request, resolver_match):
    return int(request.user.unread_threads)
