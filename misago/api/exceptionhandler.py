from rest_framework.views import exception_handler as rest_exception_handler

from django.core.exceptions import PermissionDenied
from django.utils import six

from misago.core.exceptions import Banned


def handle_api_exception(exception, context):
    response = rest_exception_handler(exception, context)
    if response:
        if isinstance(exception, Banned):
            response.data = exception.ban.get_serialized_message()
        elif isinstance(exception, PermissionDenied) and exception.args:
            response.data = {
                'detail': six.text_type(exception),
            }
        return response
    else:
        return None
