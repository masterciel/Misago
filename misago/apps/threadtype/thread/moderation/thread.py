from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.forms import Form, FormLayout
from misago.messages import Message
from misago.apps.threadtype.list.forms import MoveThreadsForm

class ThreadModeration(object):
    def thread_action_accept(self):
        # Sync thread and post
        self.thread.moderated = False
        self.thread.replies_moderated -= 1
        self.thread.save(force_update=True)
        self.thread.start_post.moderated = False
        self.thread.start_post.save(force_update=True)
        self.thread.last_post.set_checkpoint(self.request, 'accepted')
        # Sync user
        if self.thread.last_post.user:
            self.thread.start_post.user.threads += 1
            self.thread.start_post.user.posts += 1
            self.thread.start_post.user.save(force_update=True)
        # Sync forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor['threads'] = int(self.request.monitor['threads']) + 1
        self.request.monitor['posts'] = int(self.request.monitor['posts']) + self.thread.replies + 1
        self.request.messages.set_flash(Message(_('Thread has been marked as reviewed and made visible to other members.')), 'success', 'threads')

    def thread_action_annouce(self):
        self.thread.weight = 2
        self.thread.save(force_update=True)
        self.request.messages.set_flash(Message(_('Thread has been turned into announcement.')), 'success', 'threads')

    def thread_action_sticky(self):
        self.thread.weight = 1
        self.thread.save(force_update=True)
        self.request.messages.set_flash(Message(_('Thread has been turned into sticky.')), 'success', 'threads')

    def thread_action_normal(self):
        self.thread.weight = 0
        self.thread.save(force_update=True)
        self.request.messages.set_flash(Message(_('Thread weight has been changed to normal.')), 'success', 'threads')

    def thread_action_move(self):
        message = None
        if self.request.POST.get('do') == 'move':
            form = MoveThreadsForm(self.request.POST, request=self.request, forum=self.forum)
            if form.is_valid():
                new_forum = form.cleaned_data['new_forum']
                self.thread.move_to(new_forum)
                self.thread.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                new_forum.sync()
                new_forum.save(force_update=True)
                self.request.messages.set_flash(Message(_('Thread has been moved to "%(forum)s".') % {'forum': new_forum.name}), 'success', 'threads')
                return None
            message = Message(form.non_field_errors()[0], 'error')
        else:
            form = MoveThreadsForm(request=self.request, forum=self.forum)
        return self.request.theme.render_to_response('threads/move_thread.html',
                                                     {
                                                      'message': message,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'thread': self.thread,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def thread_action_open(self):
        self.thread.closed = False
        self.thread.save(force_update=True)
        self.thread.last_post.set_checkpoint(self.request, 'opened')
        self.request.messages.set_flash(Message(_('Thread has been opened.')), 'success', 'threads')

    def thread_action_close(self):
        self.thread.closed = True
        self.thread.save(force_update=True)
        self.thread.last_post.set_checkpoint(self.request, 'closed')
        self.request.messages.set_flash(Message(_('Thread has been closed.')), 'success', 'threads')

    def thread_action_undelete(self):
        # Update thread
        self.thread.deleted = False
        self.thread.replies_deleted -= 1
        self.thread.save(force_update=True)
        # Update first post in thread
        self.thread.start_post.deleted = False
        self.thread.start_post.save(force_update=True)
        # Set checkpoint
        self.thread.last_post.set_checkpoint(self.request, 'undeleted')
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor['threads'] = int(self.request.monitor['threads']) + 1
        self.request.monitor['posts'] = int(self.request.monitor['posts']) + self.thread.replies + 1
        self.request.messages.set_flash(Message(_('Thread has been undeleted.')), 'success', 'threads')

    def thread_action_soft(self):
        # Update thread
        self.thread.deleted = True
        self.thread.replies_deleted += 1
        self.thread.save(force_update=True)
        # Update first post in thread
        self.thread.start_post.deleted = True
        self.thread.start_post.save(force_update=True)
        # Set checkpoint
        self.thread.last_post.set_checkpoint(self.request, 'deleted')
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor['threads'] = int(self.request.monitor['threads']) - 1
        self.request.monitor['posts'] = int(self.request.monitor['posts']) - self.thread.replies - 1
        self.request.messages.set_flash(Message(_('Thread has been deleted.')), 'success', 'threads')

    def thread_action_hard(self):
        # Delete thread
        self.thread.delete()
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor['threads'] = int(self.request.monitor['threads']) - 1
        self.request.monitor['posts'] = int(self.request.monitor['posts']) - self.thread.replies - 1
        self.request.messages.set_flash(Message(_('Thread "%(thread)s" has been deleted.') % {'thread': self.thread.name}), 'success', 'threads')
        return self.threads_list_redirect()
