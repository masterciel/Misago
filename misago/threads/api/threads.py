from django.db import transaction

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from misago.acl import add_acl
from misago.categories.models import CATEGORIES_TREE_ID
from misago.users.rest_permissions import IsAuthenticatedOrReadOnly
from misago.core.shortcuts import get_int_or_404, get_object_or_404

from misago.threads.api.threadendpoints.list import threads_list_endpoint
from misago.threads.models import Thread, Subscription
from misago.threads.permissions.threads import allow_see_thread
from misago.threads.serializers import ThreadSerializer
from misago.threads.subscriptions import make_subscription_aware


class ThreadViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    parser_classes=(JSONParser, )

    TREE_ID = CATEGORIES_TREE_ID

    def validate_thread_visible(self, user, thread):
        allow_see_thread(user, thread)

    def get_thread(self, user, thread_id):
        thread = get_object_or_404(Thread.objects.select_related('category'),
            id=get_int_or_404(thread_id),
            category__tree_id=self.TREE_ID,
        )

        add_acl(user, thread.category)
        add_acl(user, thread)

        self.validate_thread_visible(user, thread)
        return thread

    def list(self, request):
        return threads_list_endpoint(request)

    def retrieve(self, request, pk=None):
        thread = self.get_thread(request.user, pk)

        make_subscription_aware(request.user, thread)

        return Response(ThreadSerializer(thread).data)

    @detail_route(methods=['post'])
    def subscribe(self, request, pk=None):
        thread = self.get_thread(request.user, pk)

        with transaction.atomic():
            request.user.subscription_set.filter(thread=thread).delete()

            if request.data.get('notify'):
                request.user.subscription_set.create(
                    thread=thread,
                    category=thread.category,
                    last_read_on=thread.last_post_on,
                    send_email=False,
                )
            elif request.data.get('email'):
                request.user.subscription_set.create(
                    thread=thread,
                    category=thread.category,
                    last_read_on=thread.last_post_on,
                    send_email=True,
                )

            return Response({
                'detail': 'ok',
            })