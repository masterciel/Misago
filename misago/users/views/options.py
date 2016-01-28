from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from misago.users.decorators import deny_guests


@deny_guests
def index(request, *args, **kwargs):
    request.frontend_context.update({
        'USERNAME_CHANGES_API': reverse('misago:api:usernamechange-list'),

        'USER_OPTIONS': [
            {
                'name': _("Forum options"),
                'icon': 'settings',
                'component': 'forum-options',
            },
            {
                'name': _("Change username"),
                'icon': 'card_membership',
                'component': 'change-username',
            },
            {
                'name': _("Change sign-in credentials"),
                'icon': 'vpn_key',
                'component': 'sign-in-credentials',
            },
        ]
    });

    return render(request, 'misago/options/noscript.html')


class ChangeError(Exception):
    pass


def confirm_change_view(f):
    @deny_guests
    def decorator(request, token):
        try:
            return f(request, token)
        except ChangeError as e:
            return render(request, 'misago/options/credentials_error.html', {
                'message': e.args[0],
            }, status=400)
    return decorator


@confirm_change_view
def confirm_email_change(request, token):
    new_credentials = get_new_credentials(request.user, token)
    if not (new_credentials and new_credentials.get('email')):
        raise ChangeError(_("Confirmation link is invalid."))

    try:
        request.user.set_email(new_credentials['email'])
        request.user.save(update_fields=['email', 'email_hash']])
    except IntegrityError:
        raise ChangeError()

    message = _("%(user)s, your e-mail has been changed.")
    return render(request, 'misago/options/credentials_changed.html', {
            'message': message % {'user': inactive_user.username},
        })


@confirm_change_view
def confirm_password_change(request, token):
    new_credentials = get_new_credentials(request.user, token)
    if not (new_credentials and new_credentials.get('password')):
        raise ChangeError()

    request.user.password = new_credentials['password']
    update_session_auth_hash(request, request.user)
    request.user.save(update_fields=['password'])

    message = _("%(user)s, your password has been changed.")
    return render(request, 'misago/options/credentials_changed.html', {
            'message': message % {'user': inactive_user.username},
        })
