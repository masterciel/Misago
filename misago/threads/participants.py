from django.utils.translation import ugettext as _
from misago.notifications import notify_user
from misago.threads.models import ThreadParticipant


def thread_has_participants(thread):
    return thread.threadparticipant_set.exists()


def make_thread_participants_aware(user, thread):
    thread.participants_list = []
    thread.participant = None

    participants_qs = ThreadParticipant.objects.filter(thread=thread)
    participants_qs = participants_qs.select_related('user')
    for participant in participants_qs.order_by('-is_owner', 'user__slug'):
        participant.thread = thread
        thread.participants_list.append(participant)
        if participant.user == user:
            thread.participant = participant
    return thread.participants_list


def set_thread_owner(thread, user):
    ThreadParticipant.objects.set_owner(thread, user)


def set_user_unread_private_threads_sync(user):
    user.sync_unread_private_threads = True
    user.save(update_fields=['sync_unread_private_threads'])


def add_participant(request, thread, user):
    """
    Add participant to thread, set "recound private threads" flag on user,
    notify user about being added to thread and mail him about it
    """
    ThreadParticipant.objects.add_participant(thread, user)

    notify_user(
        user,
        _("%(user)s added you to %(thread)s private thread."),
        thread.get_new_reply_url(),
        'see_thread_%s' % thread.pk,
        {'user': request.user.username, 'thread': thread.title},
        request.user)

    set_user_unread_private_threads_sync(user)

def add_owner(thread, user):
    """
    Add owner to thread, set "recound private threads" flag on user,
    notify user about being added to thread
    """
    ThreadParticipant.objects.add_participant(thread, user, True)
    set_user_unread_private_threads_sync(user)


def remove_participant(thread, user):
    """
    Remove thread participant, set "recound private threads" flag on user
    """
    thread.threadparticipant_set.filter(user=user).delete()
    set_user_unread_private_threads_sync(user)
