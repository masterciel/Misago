"""
Misago UI views controller

UI views are small views that are called asynchronically to give UI knowledge
of changes in APP state and thus opportunity to update themselves in real time
"""
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve
from django.http import Http404, JsonResponse

from misago.core.decorators import ajax_only
from misago.core.utils import is_request_local


__all__ = ['uiview', 'uiserver']


UI_VIEWS = []


def uiview(name):
    """
    Decorator for registering UI views
    """
    def namespace_decorator(f):
        UI_VIEWS.append((name, f))
        return f
    return namespace_decorator


def get_resolver_match(request):
    if not is_request_local(request):
        raise PermissionDenied()

    requesting_path = request.META['HTTP_REFERER']
    requesting_path = requesting_path[len(request.scheme) + 3:]
    requesting_path = requesting_path[len(request.META['HTTP_HOST']):]

    return resolve(requesting_path)


@ajax_only
def uiserver(request):
    resolver_match = get_resolver_match(request)
    response_dict = {'total_count': 0}

    for name, view in UI_VIEWS:
        try:
            view_response = view(request, resolver_match)
            if view_response:
                response_dict['total_count'] += view_response.get('count', 0)
                response_dict[name] = view_response
        except (Http404, PermissionDenied):
            pass

    return JsonResponse(response_dict)
