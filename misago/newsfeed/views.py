from django.template import RequestContext
from misago.authn.decorators import block_guest
from misago.threads.models import Post

@block_guest
def newsfeed(request):
    follows = []
    for user in request.user.follows.iterator():
        follows.append(user.pk)
    queryset = []
    if follows:
        queryset = Post.objects.filter(forum_id__in=request.acl.threads.get_readable_forums(request.acl))
        queryset = queryset.filter(deleted=False).filter(moderated=False)
        queryset = queryset.filter(user_id__in=follows)
        queryset = queryset.prefetch_related('thread', 'forum', 'user').order_by('-id')
        queryset = queryset[:18]
    return request.theme.render_to_response('newsfeed.html',
                                            {
                                             'follows': follows,
                                             'posts': queryset,
                                             },
                                            context_instance=RequestContext(request))