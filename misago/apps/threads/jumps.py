from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago import messages
from misago.acl.exceptions import ACLError403, ACLError404
from misago.decorators import check_csrf
from misago.models import Poll, PollVote
from misago.apps.threadtype.jumps import *
from misago.apps.threads.forms import PollVoteForm
from misago.apps.threads.mixins import TypeMixin

class LastReplyView(LastReplyBaseView, TypeMixin):
    pass


class FindReplyView(FindReplyBaseView, TypeMixin):
    pass


class NewReplyView(NewReplyBaseView, TypeMixin):
    pass


class FirstModeratedView(FirstModeratedBaseView, TypeMixin):
    pass


class FirstReportedView(FirstReportedBaseView, TypeMixin):
    pass


class ShowHiddenRepliesView(ShowHiddenRepliesBaseView, TypeMixin):
    pass


class WatchThreadView(WatchThreadBaseView, TypeMixin):
    pass


class WatchEmailThreadView(WatchEmailThreadBaseView, TypeMixin):
    pass


class UnwatchThreadView(UnwatchThreadBaseView, TypeMixin):
    pass


class UnwatchEmailThreadView(UnwatchEmailThreadBaseView, TypeMixin):
    pass


class UpvotePostView(UpvotePostBaseView, TypeMixin):
    pass


class DownvotePostView(DownvotePostBaseView, TypeMixin):
    pass


class ReportPostView(ReportPostBaseView, TypeMixin):
    pass


class ShowPostReportView(ShowPostReportBaseView, TypeMixin):
    pass


class VoteInPollView(JumpView, TypeMixin):
    def check_permissions(self):
        if self.request.method != 'POST':
            raise ACLError404()
        if not self.request.user.is_authenticated():
            raise ACLError403(_("Only registered users can vote in polls."))

    def make_jump(self):
        @check_csrf
        @transaction.commit_on_success
        def view(request):
            self.fetch_poll()
            form = PollVoteForm(self.request.POST, request=self.request, poll=self.poll)
            if form.is_valid():
                if self.poll.user_votes:
                    self.poll.retract_votes(self.poll.user_votes)
                self.poll.make_vote(self.request, form.cleaned_data['options'])
                self.poll.save()
                messages.success(self.request, _("Your vote has been cast."), 'poll_%s' % self.poll.pk)
            else:
                messages.error(self.request, form.errors['__all__'][0], 'poll_%s' % self.poll.pk)
            return redirect(self.request.POST.get('retreat', reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug})) + '#poll')
        return view(self.request)

    def fetch_poll(self):
        self.poll = Poll.objects.select_for_update().get(thread=self.thread.pk)
        if not self.poll:
            raise ACLError404(_("Poll could not be found."))
        self.poll.option_set.all()
        self.poll.user_votes = self.request.user.pollvote_set.filter(poll=self.poll)
        self.request.acl.threads.allow_vote_in_polls(self.forum, self.thread, self.poll)