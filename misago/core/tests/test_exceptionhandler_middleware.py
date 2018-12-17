from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from misago.acl.useracl import get_user_acl
from misago.users.models import AnonymousUser

from misago.core.middleware import ExceptionHandlerMiddleware


def test_request():
    request = RequestFactory().get(reverse('misago:index'))
    request.cache_versions = {"acl": "abcdefgh"}
    request.user = AnonymousUser()
    request.user_acl = get_user_acl(request.user, request.cache_versions)
    request.include_frontend_context = True
    request.frontend_context = {}
    return request


class ExceptionHandlerMiddlewareTests(TestCase):
    def test_middleware_returns_response_for_supported_exception(self):
        """Middleware returns HttpResponse for supported exception"""
        middleware = ExceptionHandlerMiddleware()
        exception = Http404()
        assert middleware.process_exception(test_request(), exception)

    def test_middleware_returns_none_for_non_supported_exception(self):
        """Middleware returns None for non-supported exception"""
        middleware = ExceptionHandlerMiddleware()
        exception = TypeError()
        assert middleware.process_exception(test_request(), exception) is None
