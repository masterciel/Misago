from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from misago.core.decorators import ajax_only, require_POST

from misago.users import validators
from misago.users.decorators import deny_guests


def api(f):
    @sensitive_post_parameters("email", "password")
    @ajax_only
    @require_POST
    def decorator(request, *args, **kwargs):
        if kwargs.get('user_id'):
            User = get_user_model()
            kwargs['user'] = get_object_or_404(User, pk=kwargs.pop('user_id'))

        try:
            return JsonResponse({
                'has_error': 0,
                'message': f(request, *args, **kwargs),
            })
        except ValidationError as e:
            return JsonResponse({
                'has_error': 1,
                'message': unicode(e.message)
            })
    return decorator


@api
def validate_username(request, user=None):
    try:
        validators.validate_username(request.POST['username'],
                                     exclude=user)
        return _("Entered username is valid.")
    except KeyError:
        raise ValidationError(_('Enter username.'))


@api
def validate_email(request, user=None):
    try:
        validators.validate_email(request.POST['email'],
                                  exclude=user)
        return _("Entered e-mail is valid.")
    except KeyError:
        raise ValidationError(_('Enter e-mail address.'))


@api
def validate_password(request):
    try:
        validators.validate_password(request.POST['password'])
        return _("Entered password is valid.")
    except KeyError:
        raise ValidationError(_('Enter password.'))


@ajax_only
@require_POST
@deny_guests
def suggestion_engine(request):
    suggestions = []

    username = request.POST.get('username', '').lower()
    if len(username) > 1:
        User = get_user_model()
        queryset = User.objects.filter(slug__startswith=username)

        for user in queryset.order_by('slug')[:5]:
            avatars = {}
            for size in settings.MISAGO_AVATARS_SIZES:
                avatars[size] = reverse('misago:user_avatar', kwargs={
                    'size': size, 'user_id': user.pk
                })

            suggestions.append({
                'avatar': avatars,
                'username': user.username,
                'url': user.get_absolute_url()
            })

    return JsonResponse({
        'profiles': suggestions
    })
