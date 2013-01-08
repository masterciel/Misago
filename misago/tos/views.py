from django.template import RequestContext
from misago.views import error404

def forum_tos(request):
    if request.settings.tos_url or not request.settings.tos_content:
        return error404(request)
    return request.theme.render_to_response('forum_tos.html',
                                            context_instance=RequestContext(request));
