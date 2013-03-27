from django.utils.translation import ugettext as _
from misago.apps.threadtype.thread import ThreadBaseView, ThreadModeration, PostsModeration
from misago.models import Forum, Thread
from misago.apps.privatethreads.mixins import TypeMixin

class ThreadView(ThreadBaseView, ThreadModeration, PostsModeration, TypeMixin):
    def posts_actions(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        actions = []
        try:
            if acl['can_move_threads_posts']:
                actions.append(('merge', _('Merge posts into one')))
            if acl['can_protect_posts']:
                actions.append(('protect', _('Protect posts')))
                actions.append(('unprotect', _('Remove posts protection')))
            if acl['can_delete_posts']:
                if self.thread.replies_deleted > 0:
                    actions.append(('undelete', _('Undelete posts')))
                actions.append(('soft', _('Soft delete posts')))
            if acl['can_delete_posts'] == 2:
                actions.append(('hard', _('Hard delete posts')))
        except KeyError:
            pass
        return actions

    def thread_actions(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        actions = []
        try:
            if acl['can_close_threads']:
                if self.thread.closed:
                    actions.append(('open', _('Open this thread')))
                else:
                    actions.append(('close', _('Close this thread')))
            if acl['can_delete_threads']:
                if self.thread.deleted:
                    actions.append(('undelete', _('Undelete this thread')))
                else:
                    actions.append(('soft', _('Soft delete this thread')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Hard delete this thread')))
        except KeyError:
            pass
        return actions