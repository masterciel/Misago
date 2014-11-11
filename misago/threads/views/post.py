from django.contrib import messages
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from misago.acl import add_acl

from misago.threads import permissions, moderation, goto
from misago.threads.permissions import exclude_invisible_posts
from misago.threads.views.generic.base import ViewBase


__all__ = ['QuotePostView']


class PostView(ViewBase):
    is_atomic = True
    require_post = True

    def dispatch(self, request, *args, **kwargs):
        if request.method != "POST" and self.require_post:
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response

        post = None
        response = None

        if self.is_atomic:
            with atomic():
                post = self.get_post(request, True, **kwargs)
                response = self.real_dispatch(request, post)
        else:
            post = self.get_post(request, **kwargs)
            response = self.real_dispatch(request, post)

        if response:
            return response
        else:
            return self.redirect_to_post(request.user, post)

    def real_dispatch(self, request, post):
        raise NotImplementedError(
            "post views have to override real_dispatch method")

    def redirect_to_post(self, user, post):
        return redirect(goto.post(user, post.thread, post))


class QuotePostView(PostView):
    is_atomic = False
    require_post = False

    def real_dispatch(self, request, post):
        quote_tpl = u'[quote="%s, post:%s, topic:%s"]\n%s\n[/quote]'
        formats = (post.poster_name, post.pk, post.thread_id, post.original)
        return JsonResponse({
            'quote': quote_tpl % formats
        })


class UnhidePostView(PostView):
    def real_dispatch(self, request, post):
        permissions.allow_unhide_post(request.user, post)
        moderation.unhide_post(request.user, post)
        messages.success(request, _("Post has been made visible."))


class HidePostView(PostView):
    def real_dispatch(self, request, post):
        permissions.allow_hide_post(request.user, post)
        moderation.hide_post(request.user, post)
        messages.success(request, _("Post has been hidden."))


class DeletePostView(PostView):
    def real_dispatch(self, request, post):
        post_id = post.id

        permissions.allow_delete_post(request.user, post)
        moderation.delete_post(request.user, post)

        post.thread.synchronize()
        post.thread.save()
        post.forum.synchronize()
        post.forum.save()

        posts_queryset = exclude_invisible_posts(post.thread.post_set,
                                                 request.user,
                                                 post.forum)
        posts_queryset = posts_queryset.select_related('thread', 'forum')

        if post_id < post.thread.last_post_id:
            target_post = posts_queryset.order_by('id').filter(id__gt=post_id)
        else:
            target_post = posts_queryset.order_by('-id').filter(id__lt=post_id)

        target_post = target_post[:1][0]
        target_post.thread.forum = target_post.forum

        add_acl(request.user, target_post.forum)
        add_acl(request.user, target_post.thread)
        add_acl(request.user, target_post)

        messages.success(request, _("Post has been deleted."))
        return self.redirect_to_post(request.user, target_post)
