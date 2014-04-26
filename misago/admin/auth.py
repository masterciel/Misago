from hashlib import md5
from time import time
from django.conf import settings
from django.contrib import auth as dj_auth


KEY_TOKEN = 'misago_admin_session_token'
KEY_UPDATED = 'misago_admin_session_updated'


def make_user_admin_token(user):
    formula = '%s:%s:%s' % (user.pk, user.email, user.password)
    return md5(formula).hexdigest()


# Admin session state controls
def is_admin_session(request):
    if request.user.is_anonymous():
        return False

    if not (request.user.is_staff and request.user.is_superuser):
        return False

    admin_token = request.session.get(KEY_TOKEN)
    if not admin_token == make_user_admin_token(request.user):
        return False

    updated = request.session.get(KEY_UPDATED, 0)
    if updated < time() - (settings.MISAGO_ADMIN_SESSION_EXPIRATION * 60):
        return False

    return True


def start_admin_session(request, user):
    request.session[KEY_TOKEN] = make_user_admin_token(user)
    request.session[KEY_UPDATED] = int(time())


def update_admin_session(request):
    request.session[KEY_UPDATED] = int(time())


def close_admin_session(request):
    request.session.pop(KEY_TOKEN, None)
    request.session.pop(KEY_UPDATED, None)


# Login/logout wrappers for django auth used in sign in/out views
def login(request, user):
    start_admin_session(request, user)
    dj_auth.login(request, user)


def logout(request):
    close_admin_session(request)
    dj_auth.logout(request)


# Register signal for logout to make sure eventual admin session is closed
def django_logout_handler(sender, **kwargs):
    close_admin_session(kwargs['request'])
dj_auth.signals.user_logged_out.connect(django_logout_handler)
