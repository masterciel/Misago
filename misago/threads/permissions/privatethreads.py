from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from misago.acl import add_acl, algebra
from misago.acl.decorators import return_boolean
from misago.acl.models import Role
from misago.categories.models import PRIVATE_THREADS_ROOT_NAME, Category
from misago.core import forms

from ..models import Thread


__all__ = [
    'allow_use_private_threads',
    'can_use_private_threads',
    'allow_see_private_thread',
    'can_see_private_thread',
    'allow_see_private_post',
    'can_see_private_post',
    'allow_takeover',
    'can_takeover',
    'allow_add_participants',
    'can_add_participants',
    'allow_remove_participants',
    'can_remove_participants',
    'allow_add_participant',
    'can_add_participant',
    'allow_message_user',
    'can_message_user',
    'exclude_invisible_private_threads',
]


"""
Admin Permissions Form
"""
class PermissionsForm(forms.Form):
    legend = _("Private threads")

    can_use_private_threads = forms.YesNoSwitch(label=_("Can use private threads"))
    can_start_private_threads = forms.YesNoSwitch(label=_("Can start private threads"))
    max_private_thread_participants = forms.IntegerField(
        label=_("Max number of users invited to private thread"),
        help_text=_("Enter 0 to don't limit number of participants."),
        initial=3,
        min_value=0
    )
    can_add_everyone_to_private_threads = forms.YesNoSwitch(
        label=_("Can add everyone to threads"),
        help_text=_("Allows user to add users that are blocking him to private threads.")
    )
    can_report_private_threads = forms.YesNoSwitch(
        label=_("Can report private threads"),
        help_text=_("Allows user to report private threads they are "
                    "participating in, making them accessible to moderators.")
    )
    can_moderate_private_threads = forms.YesNoSwitch(
        label=_("Can moderate private threads"),
        help_text=_("Allows user to read, reply, edit and delete content "
                    "in reported private threads.")
    )


def change_permissions_form(role):
    if isinstance(role, Role) and role.special_role != 'anonymous':
        return PermissionsForm
    else:
        return None


"""
ACL Builder
"""
def build_acl(acl, roles, key_name):
    new_acl = {
        'can_use_private_threads': 0,
        'can_start_private_threads': 0,
        'max_private_thread_participants': 3,
        'can_add_everyone_to_private_threads': 0,
        'can_report_private_threads': 0,
        'can_moderate_private_threads': 0,
    }

    new_acl.update(acl)

    algebra.sum_acls(new_acl, roles=roles, key=key_name,
        can_use_private_threads=algebra.greater,
        can_start_private_threads=algebra.greater,
        max_private_thread_participants=algebra.greater_or_zero,
        can_add_everyone_to_private_threads=algebra.greater,
        can_report_private_threads=algebra.greater,
        can_moderate_private_threads=algebra.greater
    )

    if not new_acl['can_use_private_threads']:
        return new_acl

    private_category = Category.objects.private_threads()

    new_acl['visible_categories'].append(private_category.pk)
    new_acl['browseable_categories'].append(private_category.pk)

    if new_acl['can_moderate_private_threads']:
        new_acl['can_see_reports'].append(private_category.pk)

    category_acl = {
        'can_see': 1,
        'can_browse': 1,
        'can_see_all_threads': 1,
        'can_see_own_threads': 0,
        'can_start_threads': new_acl['can_start_private_threads'],
        'can_reply_threads': 1,
        'can_edit_threads': 1,
        'can_edit_posts': 1,
        'can_hide_own_threads': 0,
        'can_hide_own_posts': 1,
        'thread_edit_time': 0,
        'post_edit_time': 0,
        'can_hide_threads': 0,
        'can_hide_posts': 0,
        'can_protect_posts': 0,
        'can_move_posts': 0,
        'can_merge_posts': 0,
        'can_pin_threads': 0,
        'can_close_threads': 0,
        'can_move_threads': 0,
        'can_merge_threads': 0,
        'can_approve_content': 0,
        'can_report_content': new_acl['can_report_private_threads'],
        'can_see_reports': 0,
        'can_see_posts_likes': 0,
        'can_like_posts': 0,
        'can_hide_events': 0,
    }

    if new_acl['can_moderate_private_threads']:
        category_acl.update({
            'can_edit_threads': 2,
            'can_edit_posts': 2,
            'can_hide_threads': 2,
            'can_hide_posts': 2,
            'can_protect_posts': 1,
            'can_merge_posts': 1,
            'can_see_reports': 1,
            'can_hide_events': 2,
        })

    new_acl['categories'][private_category.pk] = category_acl

    return new_acl


def add_acl_to_thread(user, thread):
    if thread.thread_type.root_name != PRIVATE_THREADS_ROOT_NAME:
        return

    if not hasattr(thread, 'participant'):
        thread.participants_list = []
        thread.participant = None

    thread.acl.update({
        'can_takeover': can_takeover(user, thread),
        'can_add_participants': can_add_participants(user, thread),
        'can_remove_participants': can_remove_participants(user, thread)
    })


def register_with(registry):
    registry.acl_annotator(Thread, add_acl_to_thread)


"""
ACL tests
"""
def allow_use_private_threads(user):
    if user.is_anonymous():
        raise PermissionDenied(_("You have to sign in to use private threads."))
    if not user.acl['can_use_private_threads']:
        raise PermissionDenied(_("You can't use private threads."))
can_use_private_threads = return_boolean(allow_use_private_threads)


def allow_see_private_thread(user, target):
    if user.acl.get('can_moderate_private_threads'):
        can_see_reported = target.has_reported_posts
    else:
        can_see_reported = False

    can_see_participating = user in [p.user for p in target.participants_list]

    if not (can_see_participating or can_see_reported):
        raise Http404()
can_see_private_thread = return_boolean(allow_see_private_thread)


def allow_see_private_post(user, target):
    can_see_reported = user.acl['can_moderate_private_threads']
    if not (can_see_reported and target.thread.has_reported_posts):
        for participant in target.thread.participants_list:
            if participant.user == user and participant.is_removed:
                if post.posted_on > target.last_post_on:
                    raise Http404()
can_see_private_post = return_boolean(allow_see_private_post)


def allow_takeover(user, target):
    if target.participant and target.participant.is_owner:
        raise PermissionDenied(
            _("You are already this thread's owner."))
    if not user.acl['can_moderate_private_threads']:
        raise PermissionDenied(
            _("Only private threads moderators can take over private threads."))
can_takeover = return_boolean(allow_takeover)


def allow_add_participants(user, target):
    if not target.participant or not target.participant.is_owner:
        raise PermissionDenied(
            _("You have to be thread owner to add new participants to it."))

    max_participants = user.acl['max_private_thread_participants']
    current_participants = len(target.participants_list) - 1

    if current_participants >= max_participants :
        raise PermissionDenied(
            _("You can't add any more new users to this thread."))
can_add_participants = return_boolean(allow_add_participants)


def allow_remove_participants(user, target):
    if not target.participant or not target.participant.is_owner:
        raise PermissionDenied(
            _("You have to be thread owner to remove participants from it."))
can_remove_participants = return_boolean(allow_remove_participants)


def allow_add_participant(user, target):
    message_format = {'user': target.username}

    if not can_use_private_threads(target):
        raise PermissionDenied(
            _("%(user)s can't participate in private threads.") % message_format)

    if user.acl['can_add_everyone_to_private_threads']:
        return

    if user.acl['can_be_blocked'] and target.is_blocking(user):
        raise PermissionDenied(_("%(user)s is blocking you.") % message_format)

    if target.can_be_messaged_by_nobody:
        raise PermissionDenied(
            _("%(user)s is not allowing invitations to private threads.") % message_format)

    if target.can_be_messaged_by_followed and not target.is_following(user):
        message = _("%(user)s limits invitations to private threads to followed users.")
        raise PermissionDenied(message % message_format)
can_add_participant = return_boolean(allow_add_participant)


def allow_message_user(user, target):
    allow_use_private_threads(user)

    if user == target:
        raise PermissionDenied(_("You can't message yourself."))

    if not user.acl['can_start_private_threads']:
        raise PermissionDenied(_("You can't start private threads."))

    allow_add_participant(user, target)
can_message_user = return_boolean(allow_message_user)


"""
Queryset helpers
"""
def exclude_invisible_private_threads(queryset, user):
    if user.acl['can_moderate_private_threads']:
        see_participating = Q(participants=user)
        see_reported = Q(has_reported_posts=True)
        return queryset.filter(see_reported | see_participating)
    else:
        return queryset.filter(participants=user)
