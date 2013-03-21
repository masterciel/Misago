from django.utils import timezone
from misago.apps.threadtype.posting.base import PostingBaseView
from misago.apps.threadtype.posting.forms import EditReplyForm
from misago.markdown import post_markdown

class EditReplyBaseView(PostingBaseView):
    form_type = EditReplyForm

    def set_context(self):
        self.set_thread_context()
        self.post = self.thread.post_set.get(id=self.kwargs.get('post'))
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)
        self.request.acl.threads.allow_reply_edit(self.request.user, self.proxy, self.thread, self.post)

    def form_initial_data(self):
        return {
                'weight': self.thread.weight,
                'post': self.post.post,
                }

    def post_form(self, form):
        now = timezone.now()
        old_post = self.post.post

        changed_thread = False
        changed_post = old_post != form.cleaned_data['post']

        if 'close_thread' in form.cleaned_data and form.cleaned_data['close_thread']:
            self.thread.closed = not self.thread.closed
            changed_thread = True
            if self.thread.closed:
                self.thread.last_post.set_checkpoint(self.request, 'closed')
            else:
                self.thread.last_post.set_checkpoint(self.request, 'opened')

        if ('thread_weight' in form.cleaned_data and
                form.cleaned_data['thread_weight'] != self.thread.weight):
            self.thread.weight = form.cleaned_data['thread_weight']
            changed_thread = True

        if changed_thread:
            self.thread.save(force_update=True)

        if changed_post:
            self.md, self.post.post_preparsed = post_markdown(self.request, form.cleaned_data['post'])
            self.post.edits += 1
            self.post.edit_date = now
            self.post.edit_user = self.request.user
            self.post.edit_user_name = self.request.user.username
            self.post.edit_user_slug = self.request.user.username_slug
            self.post.save(force_update=True)
            self.record_edit(form, self.thread.name, old_post)