# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.utils.encoding import smart_str

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.models import LIMITS_PRIVATE_THREAD_INVITES_TO_FOLLOWED, LIMITS_PRIVATE_THREAD_INVITES_TO_NOBODY
from misago.users.testutils import AuthenticatedUserTestCase

from ..models import Thread, ThreadParticipant


class StartPrivateThreadTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(StartPrivateThreadTests, self).setUp()

        self.category = Category.objects.private_threads()
        self.api_link = reverse('misago:api:private-thread-list')

        User = get_user_model()
        self.other_user = get_user_model().objects.create_user(
            'BobBoberson', 'bob@boberson.com', 'pass123')

    def test_cant_start_thread_as_guest(self):
        """user has to be authenticated to be able to post private thread"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_cant_use_private_threads(self):
        """has no permission to see selected category"""
        override_acl(self.user, {'can_use_private_threads': 0})

        response = self.client.post(self.api_link)
        self.assertContains(response, "You can't use private threads.", status_code=403)

    def test_cant_start_private_thread(self):
        """permission to start private thread is validated"""
        override_acl(self.user, {'can_start_private_threads': 0})

        response = self.client.post(self.api_link)
        self.assertContains(response, "You can't start private threads.", status_code=403)

    def test_empty_data(self):
        """no data sent handling has no showstoppers"""
        response = self.client.post(self.api_link, data={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'to': [
                "You have to enter user names."
            ],
            'title':[
                "You have to enter thread title."
            ],
            'post': [
                "You have to enter a message."
            ]
        })

    def test_title_is_validated(self):
        """title is validated"""
        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "------",
            'post': "Lorem ipsum dolor met, sit amet elit!",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'title': [
                "Thread title should contain alpha-numeric characters."
            ]
        })

    def test_post_is_validated(self):
        """post is validated"""
        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "Lorem ipsum dolor met",
            'post': "a",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'post': [
                "Posted message should be at least 5 characters long (it has 1)."
            ]
        })

    def test_cant_invite_self(self):
        """api validates that you cant invite yourself to private thread"""
        response = self.client.post(self.api_link, data={
            'to': [self.user.username],
            'title': "Lorem ipsum dolor met",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'to': [
                "You can't include yourself on the list of users to invite to new thread."
            ]
        })

    def test_cant_invite_nonexisting(self):
        """api validates that you cant invite nonexisting user to thread"""
        response = self.client.post(self.api_link, data={
            'to': ['Ab', 'Cd'],
            'title': "Lorem ipsum dolor met",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'to': [
                "One or more users could not be found: ab, cd"
            ]
        })

    def test_cant_invite_too_many(self):
        """api validates that you cant invite too many users to thread"""
        response = self.client.post(self.api_link, data={
            'to': ['Username{}'.format(i) for i in range(50)],
            'title': "Lorem ipsum dolor met",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'to': [
                "You can't add more than 3 users to private thread (you've added 50)."
            ]
        })

    def test_cant_invite_blocking(self):
        """api validates that you cant invite blocking user to thread"""
        self.other_user.blocks.add(self.user)

        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "Lorem ipsum dolor met",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'to': [
                "BobBoberson is blocking you."
            ]
        })

        # allow us to bypass blocked check
        override_acl(self.user, {'can_add_everyone_to_private_threads': 1})

        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "-----",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'title': [
                "Thread title should contain alpha-numeric characters."
            ]
        })

    def test_cant_invite_followers_only(self):
        """api validates that you cant invite followers-only user to thread"""
        self.other_user.limits_private_thread_invites_to = LIMITS_PRIVATE_THREAD_INVITES_TO_FOLLOWED
        self.other_user.save()

        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "Lorem ipsum dolor met",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'to': [
                "BobBoberson limits invitations to private threads to followed users."
            ]
        })

        # allow us to bypass following check
        override_acl(self.user, {'can_add_everyone_to_private_threads': 1})

        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "-----",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'title': [
                "Thread title should contain alpha-numeric characters."
            ]
        })

        # make user follow us
        override_acl(self.user, {'can_add_everyone_to_private_threads': 0})
        self.other_user.follows.add(self.user)

        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "-----",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'title': [
                "Thread title should contain alpha-numeric characters."
            ]
        })

    def test_cant_invite_anyone(self):
        """api validates that you cant invite nobody user to thread"""
        self.other_user.limits_private_thread_invites_to = LIMITS_PRIVATE_THREAD_INVITES_TO_NOBODY
        self.other_user.save()

        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "Lorem ipsum dolor met",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'to': [
                "BobBoberson is not allowing invitations to private threads."
            ]
        })

        # allow us to bypass user preference check
        override_acl(self.user, {'can_add_everyone_to_private_threads': 1})

        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "-----",
            'post': "Lorem ipsum dolor.",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'title': [
                "Thread title should contain alpha-numeric characters."
            ]
        })

    def test_can_start_thread(self):
        """endpoint creates new thread"""
        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "Hello, I am test thread!",
            'post': "Lorem ipsum dolor met!"
        })
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]

        response_json = response.json()
        self.assertEqual(response_json['url'], thread.get_absolute_url())

        response = self.client.get(thread.get_absolute_url())
        self.assertContains(response, self.category.name)
        self.assertContains(response, thread.title)
        self.assertContains(response, "<p>Lorem ipsum dolor met!</p>")

        self.reload_user()
        self.assertEqual(self.user.threads, 1)
        self.assertEqual(self.user.posts, 1)

        self.assertEqual(thread.category_id, self.category.pk)
        self.assertEqual(thread.title, "Hello, I am test thread!")
        self.assertEqual(thread.starter_id, self.user.id)
        self.assertEqual(thread.starter_name, self.user.username)
        self.assertEqual(thread.starter_slug, self.user.slug)
        self.assertEqual(thread.last_poster_id, self.user.id)
        self.assertEqual(thread.last_poster_name, self.user.username)
        self.assertEqual(thread.last_poster_slug, self.user.slug)

        post = self.user.post_set.all()[:1][0]
        self.assertEqual(post.category_id, self.category.pk)
        self.assertEqual(post.original, 'Lorem ipsum dolor met!')
        self.assertEqual(post.poster_id, self.user.id)
        self.assertEqual(post.poster_name, self.user.username)

        # thread has two participants
        self.assertEqual(thread.participants.count(), 2)

        # we are thread owner
        ThreadParticipant.objects.get(
            thread=thread,
            user=self.user,
            is_owner=True
        )

        # other user was added to thread
        ThreadParticipant.objects.get(
            thread=thread,
            user=self.other_user,
            is_owner=False
        )

        # other user has sync_unread_private_threads flag
        User = get_user_model()
        user_to_sync = User.objects.get(sync_unread_private_threads=True)
        self.assertEqual(user_to_sync, self.other_user)

        # notification about new private thread was sent to other user
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[-1]

        self.assertIn(self.user.username, email.subject)
        self.assertIn(thread.title, email.subject)

        email_body = smart_str(email.body)

        self.assertIn(self.user.username, email_body)
        self.assertIn(thread.title, email_body)
        self.assertIn(thread.get_absolute_url(), email_body)

    def test_post_unicode(self):
        """unicode characters can be posted"""
        response = self.client.post(self.api_link, data={
            'to': [self.other_user.username],
            'title': "Brzęczyżczykiewicz",
            'post': "Chrzążczyżewoszyce, powiat Łękółody."
        })
        self.assertEqual(response.status_code, 200)
