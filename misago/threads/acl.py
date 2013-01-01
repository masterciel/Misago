from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from misago.acl.builder import BaseACL
from misago.acl.utils import ACLError403, ACLError404
from misago.forms import YesNoSwitch

def make_forum_form(request, role, form):
    form.base_fields['can_read_threads'] = forms.ChoiceField(choices=(
                                                                     ('0', _("No")),
                                                                     ('1', _("Yes, owned")),
                                                                     ('2', _("Yes, all")),
                                                                     ))
    form.base_fields['can_start_threads'] = forms.ChoiceField(choices=(
                                                                       ('0', _("No")),
                                                                       ('1', _("Yes, with moderation")),
                                                                       ('2', _("Yes")),
                                                                       ))
    form.base_fields['can_edit_own_threads'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_soft_delete_own_threads'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_write_posts'] = forms.ChoiceField(choices=(
                                                                     ('0', _("No")),
                                                                     ('1', _("Yes, with moderation")),
                                                                     ('2', _("Yes")),
                                                                     ))
    form.base_fields['can_edit_own_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_soft_delete_own_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_upvote_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_downvote_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_posts_scores'] = forms.ChoiceField(choices=(
                                                                          ('0', _("No")),
                                                                          ('1', _("Yes, final score")),
                                                                          ('2', _("Yes, both up and down-votes")),
                                                                          ))
    form.base_fields['can_see_votes'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_make_polls'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_vote_in_polls'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_poll_votes'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_attachments'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_upload_attachments'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_download_attachments'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['attachment_size'] = forms.IntegerField(min_value=0,initial=100)
    form.base_fields['attachment_limit'] = forms.IntegerField(min_value=0,initial=3)
    form.base_fields['can_approve'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_edit_labels'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_changelog'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_pin_threads'] = forms.ChoiceField(choices=(
                                                                     ('0', _("No")),
                                                                     ('1', _("Yes, to stickies")),
                                                                     ('2', _("Yes, to annoucements")),
                                                                     ))
    form.base_fields['can_edit_threads_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_move_threads_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_close_threads'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_protect_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_delete_threads'] = forms.ChoiceField(choices=(
                                                                        ('0', _("No")),
                                                                        ('1', _("Yes, soft-delete")),
                                                                        ('2', _("Yes, hard-delete")),
                                                                        ))
    form.base_fields['can_delete_posts'] = forms.ChoiceField(choices=(
                                                                      ('0', _("No")),
                                                                      ('1', _("Yes, soft-delete")),
                                                                      ('2', _("Yes, hard-delete")),
                                                                      ))
    form.base_fields['can_delete_polls'] = forms.ChoiceField(choices=(
                                                                      ('0', _("No")),
                                                                      ('1', _("Yes, soft-delete")),
                                                                      ('2', _("Yes, hard-delete")),
                                                                      ))
    form.base_fields['can_delete_attachments'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    
    form.layout.append((
                        _("Threads"),
                        (
                         ('can_read_threads', {'label': _("Can read threads")}),
                         ('can_start_threads', {'label': _("Can start new threads")}),
                         ('can_edit_own_threads', {'label': _("Can edit own threads")}),
                         ('can_soft_delete_own_threads', {'label': _("Can soft-delete own threads")}),
                        ),
                       ),)
    form.layout.append((
                        _("Posts"),
                        (
                         ('can_write_posts', {'label': _("Can write posts")}),
                         ('can_edit_own_posts', {'label': _("Can edit own posts")}),
                         ('can_soft_delete_own_posts', {'label': _("Can soft-delete own posts")}),
                        ),
                       ),)
    form.layout.append((
                        _("Karma"),
                        (
                         ('can_upvote_posts', {'label': _("Can upvote posts")}),
                         ('can_downvote_posts', {'label': _("Can downvote posts")}),
                         ('can_see_posts_scores', {'label': _("Can see post score")}),
                         ('can_see_votes', {'label': _("Can see who voted on post")}),
                        ),
                       ),)
    form.layout.append((
                        _("Polls"),
                        (
                         ('can_make_polls', {'label': _("Can make polls")}),
                         ('can_vote_in_polls', {'label': _("Can vote in polls")}),
                         ('can_see_poll_votes', {'label': _("Can see who voted in poll")}),
                        ),
                       ),)
    form.layout.append((
                        _("Attachments"),
                        (
                         ('can_see_attachments', {'label': _("Can see attachments")}),
                         ('can_upload_attachments', {'label': _("Can upload attachments")}),
                         ('can_download_attachments', {'label': _("Can download attachments")}),
                         ('attachment_size', {'label': _("Max size of single attachment (in Kb)"), 'help_text': _("Enter zero for no limit.")}),
                         ('attachment_limit', {'label': _("Max number of attachments per post"), 'help_text': _("Enter zero for no limit.")}),
                        ),
                       ),)
    form.layout.append((
                        _("Moderation"),
                        (
                         ('can_approve', {'label': _("Can accept threads and posts")}),
                         ('can_edit_labels', {'label': _("Can edit thread labels")}),
                         ('can_see_changelog', {'label': _("Can see edits history")}),
                         ('can_make_annoucements', {'label': _("Can make annoucements")}),
                         ('can_pin_threads', {'label': _("Can change threads weight")}),
                         ('can_edit_threads_posts', {'label': _("Can edit threads and posts")}),
                         ('can_move_threads_posts', {'label': _("Can move, merge and split threads and posts")}),
                         ('can_close_threads', {'label': _("Can close threads")}),
                         ('can_protect_posts', {'label': _("Can protect posts"), 'help_text': _("Protected posts cannot be changed by their owners.")}),
                         ('can_delete_threads', {'label': _("Can delete threads")}),
                         ('can_delete_posts', {'label': _("Can delete posts")}),
                         ('can_delete_polls', {'label': _("Can delete polls")}),
                         ('can_delete_attachments', {'label': _("Can delete attachments")}),
                        ),
                       ),)


class ThreadsACL(BaseACL):
    def get_role(self, forum):
        try:
            return self.acl[forum.pk]
        except KeyError:
            return {}
    
    def allow_thread_view(self, user, thread):
        try:
            forum_role = self.acl[thread.forum_id]
            if forum_role['can_read_threads'] == 0:
                raise ACLError403(_("You don't have permission to read threads in this forum."))
            if thread.moderated and not (forum_role['can_approve'] or (user.is_authenticated() and user == thread.start_poster)):
                raise ACLError404()
        except KeyError:
            raise ACLError403(_("You don't have permission to read threads in this forum."))
    
    def allow_post_view(self, user, thread, post):
        forum_role = self.acl[thread.forum_id]
        if post.moderated and not (forum_role['can_approve'] or (user.is_authenticated() and user == post.user)):
            raise ACLError404()
        if post.deleted and not (forum_role['can_delete_posts'] or (user.is_authenticated() and user == post.user)):
            raise ACLError404()
    
    def get_readable_forums(self, acl):
        readable = []
        for forum in self.acl:
            if acl.forums.can_browse(forum) and self.acl[forum]['can_read_threads']:
                readable.append(forum)
        return readable
    
    def filter_threads(self, request, forum, queryset):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_approve']:
                if request.user.is_authenticated():
                    queryset = queryset.filter(Q(moderated=0) | Q(start_poster=request.user))
                else:
                    queryset = queryset.filter(moderated=0)
        except KeyError:
            return False
        return queryset
    
    def filter_posts(self, request, thread, queryset):
        try:
            forum_role = self.acl[thread.forum.pk]
            if not forum_role['can_approve']:
                if request.user.is_authenticated():
                    queryset = queryset.filter(Q(moderated=0) | Q(user=request.user))
                else:
                    queryset = queryset.filter(moderated=0)
        except KeyError:
            return False
        return queryset
    
    def can_start_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if forum_role['can_read_threads'] == 0 or forum_role['can_start_threads'] == 0:
                return False
            if forum.closed and forum_role['can_close_threads'] == 0:
                return False
            return True
        except KeyError:
            return False
    
    def allow_new_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if forum_role['can_read_threads'] == 0 or forum_role['can_start_threads'] == 0:
                raise ACLError403(_("You don't have permission to start new threads in this forum."))
            if forum.closed and forum_role['can_close_threads'] == 0:
                raise ACLError403(_("This forum is closed, you can't start new threads in it."))
        except KeyError:
            raise ACLError403(_("You don't have permission to start new threads in this forum."))
    
    def can_edit_thread(self, user, forum, thread, post):
        try:
            forum_role = self.acl[thread.forum_id]
            if forum_role['can_close_threads'] == 0 and (forum.closed or thread.closed):
                return False
            if forum_role['can_edit_threads_posts']:
                return True
            if forum_role['can_edit_own_threads'] and not post.protected and post.user_id == user.pk:
                return True
            return False
        except KeyError:
            return False
    
    def allow_thread_edit(self, user, forum, thread, post):
        try:
            forum_role = self.acl[thread.forum_id]
            if not forum_role['can_close_threads']:
                if forum.closed:
                    raise ACLError403(_("You can't edit threads in closed forums."))
                if thread.closed:
                    raise ACLError403(_("You can't edit closed threads."))
            if not forum_role['can_edit_threads_posts']:
                if post.user_id != user.pk:
                    raise ACLError403(_("You can't edit other members threads."))
                if not forum_role['can_edit_own_threads']:
                    raise ACLError403(_("You can't edit your threads."))
                if post.protected:
                    raise ACLError403(_("This thread is protected, you cannot edit it."))
        except KeyError:
            raise ACLError403(_("You don't have permission to edit threads in this forum."))

    def can_reply(self, forum, thread):
        try:
            forum_role = self.acl[forum.pk]
            if forum_role['can_write_posts'] == 0:
                return False
            if (forum.closed or thread.closed) and forum_role['can_close_threads'] == 0:
                return False
            return True
        except KeyError:
            return False

    def allow_reply(self, forum, thread):
        try:
            forum_role = self.acl[thread.forum.pk]
            if forum_role['can_write_posts'] == 0:
                raise ACLError403(_("You don't have permission to write replies in this forum."))
            if forum_role['can_close_threads'] == 0:
                if forum.closed:
                    raise ACLError403(_("You can't write replies in closed forums."))
                if thread.closed:
                    raise ACLError403(_("You can't write replies in closed threads."))
        except KeyError:
            raise ACLError403(_("You don't have permission to write replies in this forum."))
    
    def can_edit_reply(self, user, forum, thread, post):
        try:
            forum_role = self.acl[thread.forum_id]
            if forum_role['can_close_threads'] == 0 and (forum.closed or thread.closed):
                return False
            if forum_role['can_edit_threads_posts']:
                return True
            if forum_role['can_edit_own_posts'] and not post.protected and post.user_id == user.pk:
                return True
            return False
        except KeyError:
            return False
    
    def allow_reply_edit(self, user, forum, thread, post):
        try:
            forum_role = self.acl[thread.forum_id]
            if not forum_role['can_close_threads']:
                if forum.closed:
                    raise ACLError403(_("You can't edit replies in closed forums."))
                if thread.closed:
                    raise ACLError403(_("You can't edit replies in closed threads."))
            if not forum_role['can_edit_threads_posts']:
                if post.user_id != user.pk:
                    raise ACLError403(_("You can't edit other members replies."))
                if not forum_role['can_edit_own_posts']:
                    raise ACLError403(_("You can't edit your replies."))
                if post.protected:
                    raise ACLError403(_("This reply is protected, you cannot edit it."))
        except KeyError:
            raise ACLError403(_("You don't have permission to edit replies in this forum."))
    
    def can_see_changelog(self, user, forum, post):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_see_changelog'] or user.pk == post.user_id
        except KeyError:
            return False
    
    def allow_changelog_view(self, user, forum, post):
        try:
            forum_role = self.acl[forum.pk]
            if not (forum_role['can_see_changelog'] or user.pk == post.user_id):
                raise ACLError403(_("You don't have permission to see history of changes made to this post."))
        except KeyError:
            raise ACLError403(_("You don't have permission to see history of changes made to this post."))
        
    def can_make_revert(self, forum, thread):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_close_threads'] and (forum.closed or thread.closed):
                return False
            return forum_role['can_edit_threads_posts']
        except KeyError:
            return False
    
    def allow_revert(self, forum, thread):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_close_threads']:
                if forum.closed:
                    raise ACLError403(_("You can't make reverts in closed forums."))
                if thread.closed:
                    raise ACLError403(_("You can't make reverts in closed threads."))
            if not forum_role['can_edit_threads_posts']:
                raise ACLError403(_("You don't have permission to make reverts in this forum."))
        except KeyError:
            raise ACLError403(_("You don't have permission to make reverts in this forum."))
            
    def can_mod_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return (
                    forum_role['can_approve']
                    or forum_role['can_pin_threads']
                    or forum_role['can_move_threads_posts']
                    or forum_role['can_close_threads']
                    or forum_role['can_delete_threads']
                    )
        except KeyError:
            return False
        
    def can_mod_posts(self, thread):
        try:
            forum_role = self.acl[thread.forum.pk]
            return (
                    forum_role['can_edit_threads_posts']
                    or forum_role['can_move_threads_posts']
                    or forum_role['can_close_threads']
                    or forum_role['can_delete_threads']
                    or forum_role['can_delete_posts']
                    )
        except KeyError:
            return False
        
    def can_mod_thread(self, thread):
        pass
    
    def can_approve(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_approve']
        except KeyError:
            return False


def build_forums(acl, perms, forums, forum_roles):
    acl.threads = ThreadsACL()
    for forum in forums:
        forum_role = {
                     'can_read_threads': 0,
                     'can_start_threads': 0,
                     'can_edit_own_threads': False,
                     'can_soft_delete_own_threads': False,
                     'can_write_posts': 0,
                     'can_edit_own_posts': False,
                     'can_soft_delete_own_posts': False,
                     'can_upvote_posts': False,
                     'can_downvote_posts': False,
                     'can_see_posts_scores': 0,
                     'can_see_votes': False,
                     'can_make_polls': False,
                     'can_vote_in_polls': False,
                     'can_see_poll_votes': False,
                     'can_see_attachments': False,
                     'can_upload_attachments': False,
                     'can_download_attachments': False,
                     'attachment_size': 100,
                     'attachment_limit': 3,
                     'can_approve': False,
                     'can_edit_labels': False,
                     'can_see_changelog': False,
                     'can_make_annoucements': False,
                     'can_pin_threads': 0,
                     'can_edit_threads_posts': False,
                     'can_move_threads_posts': False,
                     'can_close_threads': False,
                     'can_protect_posts': False,
                     'can_delete_threads': 0,
                     'can_delete_posts': 0,
                     'can_delete_polls': 0,
                     'can_delete_attachments': False,
                     }
        for perm in perms:
            try:
                role = forum_roles[perm['forums'][forum.pk]]
                for p in forum_role:
                    try:
                        if p in ['attachment_size', 'attachment_limit'] and role[p] == 0:
                            forum_role[p] = 0
                        elif int(role[p]) > forum_role[p]:
                            forum_role[p] = int(role[p])
                    except KeyError:
                        pass
            except KeyError:
                pass
        acl.threads.acl[forum.pk] = forum_role
            