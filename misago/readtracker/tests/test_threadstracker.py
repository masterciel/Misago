from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.acl.objectacl import add_acl_to_obj
from misago.acl.useracl import get_user_acl
from misago.categories.models import Category
from misago.conf import settings
from misago.conftest import get_cache_versions
from misago.readtracker import poststracker, threadstracker
from misago.readtracker.models import PostRead
from misago.threads import testutils

User = get_user_model()

cache_versions = get_cache_versions()


class AnonymousUser(object):
    is_authenticated = False
    is_anonymous = True


class ThreadsTrackerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("UserA", "testa@user.com", 'Pass.123')
        self.user_acl = get_user_acl(self.user, cache_versions)
        self.category = Category.objects.get(slug='first-category')

        add_acl_to_obj(self.user_acl, self.category)

    def test_falsy_value(self):
        """passing falsy value to readtracker causes no errors"""
        threadstracker.make_read_aware(self.user, self.user_acl, None)
        threadstracker.make_read_aware(self.user, self.user_acl, False)
        threadstracker.make_read_aware(self.user, self.user_acl, [])

    def test_anon_thread_before_cutoff(self):
        """non-tracked thread is marked as read for anonymous users"""
        started_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        thread = testutils.post_thread(self.category, started_on=started_on)

        threadstracker.make_read_aware(AnonymousUser(), None, thread)
        self.assertTrue(thread.is_read)
        self.assertFalse(thread.is_new)

    def test_anon_thread_after_cutoff(self):
        """tracked thread is marked as read for anonymous users"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())

        threadstracker.make_read_aware(AnonymousUser(), None, thread)
        self.assertTrue(thread.is_read)
        self.assertFalse(thread.is_new)

    def test_user_thread_before_cutoff(self):
        """non-tracked thread is marked as read for authenticated users"""
        started_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        thread = testutils.post_thread(self.category, started_on=started_on)

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertTrue(thread.is_read)
        self.assertFalse(thread.is_new)

    def test_user_unread_thread(self):
        """tracked thread is marked as unread for authenticated users"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertFalse(thread.is_read)
        self.assertTrue(thread.is_new)

    def test_user_created_after_thread(self):
        """tracked thread older than user is marked as read"""
        started_on = timezone.now() - timedelta(days=1)
        thread = testutils.post_thread(self.category, started_on=started_on)

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertTrue(thread.is_read)
        self.assertFalse(thread.is_new)

    def test_user_read_post(self):
        """tracked thread with read post marked as read"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())

        poststracker.save_read(self.user, thread.first_post)

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertTrue(thread.is_read)
        self.assertFalse(thread.is_new)

    def test_user_first_unread_last_read_post(self):
        """tracked thread with unread first and last read post marked as unread"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())

        post = testutils.reply_thread(thread, posted_on=timezone.now())
        poststracker.save_read(self.user, post)

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertFalse(thread.is_read)
        self.assertTrue(thread.is_new)

    def test_user_first_read_post_unread_event(self):
        """tracked thread with read first post and unread event"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        testutils.reply_thread(thread, posted_on=timezone.now(), is_event=True)

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertFalse(thread.is_read)
        self.assertTrue(thread.is_new)

    def test_user_hidden_event(self):
        """tracked thread with unread first post and hidden event"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())

        testutils.reply_thread(
            thread,
            posted_on=timezone.now(),
            is_event=True,
            is_hidden=True,
        )

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertFalse(thread.is_read)
        self.assertTrue(thread.is_new)

    def test_user_first_read_post_hidden_event(self):
        """tracked thread with read first post and hidden event"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        testutils.reply_thread(
            thread,
            posted_on=timezone.now(),
            is_event=True,
            is_hidden=True,
        )

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertTrue(thread.is_read)
        self.assertFalse(thread.is_new)

    def test_user_thread_before_cutoff_unread_post(self):
        """non-tracked thread is marked as unread for anonymous users"""
        started_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        thread = testutils.post_thread(self.category, started_on=started_on)

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertTrue(thread.is_read)
        self.assertFalse(thread.is_new)

    def test_user_first_read_post_unapproved_post(self):
        """tracked thread with read first post and unapproved post"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        testutils.reply_thread(
            thread,
            posted_on=timezone.now(),
            is_unapproved=True,
        )

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertTrue(thread.is_read)
        self.assertFalse(thread.is_new)

    def test_user_first_read_post_unapproved_own_post(self):
        """tracked thread with read first post and unapproved own post"""
        thread = testutils.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        testutils.reply_thread(
            thread,
            posted_on=timezone.now(),
            poster=self.user,
            is_unapproved=True,
        )

        threadstracker.make_read_aware(self.user, self.user_acl, thread)
        self.assertFalse(thread.is_read)
        self.assertTrue(thread.is_new)
