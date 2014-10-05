from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import moderation, testutils
from misago.threads.models import Label, Thread, Post, Event


class ThreadsModerationTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsModerationTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.thread = testutils.post_thread(self.forum)
        Label.objects.clear_cache()

    def tearDown(self):
        super(ThreadsModerationTests, self).tearDown()
        Label.objects.clear_cache()

    def reload_thread(self):
        self.thread = Thread.objects.get(pk=self.thread.pk)

    def test_label_thread(self):
        """label_thread makes thread announcement"""
        label = Label.objects.create(name="Label", slug="label")

        self.assertIsNone(self.thread.label)
        self.assertTrue(moderation.label_thread(self.user, self.thread, label))

        self.reload_thread()
        self.assertEqual(self.thread.label, label)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertEqual(event.icon, "tag")
        self.assertIn("set thread label to", event.message)

    def test_unlabel_thread(self):
        """unlabel_thread removes thread label"""
        label = Label.objects.create(name="Label", slug="label")
        self.assertTrue(moderation.label_thread(self.user, self.thread, label))

        self.reload_thread()
        self.assertTrue(moderation.unlabel_thread(self.user, self.thread))

        self.reload_thread()
        self.assertIsNone(self.thread.label)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertEqual(event.icon, "tag")
        self.assertIn("removed thread label.", event.message)

    def test_announce_thread(self):
        """announce_thread makes thread announcement"""
        self.assertEqual(self.thread.weight, 0)
        self.assertTrue(moderation.announce_thread(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 2)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertEqual(event.icon, "star")
        self.assertIn("changed thread to announcement.", event.message)

    def test_announce_invalid_thread(self):
        """announce_thread returns false for already announced thread"""
        self.thread.weight = 2

        self.assertFalse(moderation.announce_thread(self.user, self.thread))
        self.assertEqual(self.thread.weight, 2)

    def test_pin_thread(self):
        """pin_thread makes thread pinned"""
        self.assertEqual(self.thread.weight, 0)
        self.assertTrue(moderation.pin_thread(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 1)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertEqual(event.icon, "bookmark")
        self.assertIn("pinned thread.", event.message)

    def test_pin_invalid_thread(self):
        """pin_thread returns false for already pinned thread"""
        self.thread.weight = 1

        self.assertFalse(moderation.pin_thread(self.user, self.thread))
        self.assertEqual(self.thread.weight, 1)

    def test_reset_thread(self):
        """reset_thread defaults thread weight"""
        moderation.pin_thread(self.user, self.thread)

        self.assertEqual(self.thread.weight, 1)
        self.assertTrue(moderation.reset_thread(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 0)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("unpinned thread.", event.message)
        self.assertEqual(event.icon, "circle")

    def test_reset_invalid_thread(self):
        """reset_thread returns false for already default thread"""
        self.assertFalse(moderation.reset_thread(self.user, self.thread))
        self.assertEqual(self.thread.weight, 0)

    def test_approve_thread(self):
        """approve_thread approves moderated thread"""
        thread = testutils.post_thread(self.forum, is_moderated=True)

        self.assertTrue(thread.is_moderated)
        self.assertTrue(thread.first_post.is_moderated)
        self.assertTrue(moderation.approve_thread(self.user, thread))

        self.reload_thread()
        self.assertFalse(thread.is_moderated)
        self.assertFalse(thread.first_post.is_moderated)
        self.assertTrue(thread.has_events)
        event = thread.event_set.last()

        self.assertIn("approved thread.", event.message)
        self.assertEqual(event.icon, "check")

    def test_close_thread(self):
        """close_thread closes thread"""
        self.assertFalse(self.thread.is_closed)
        self.assertTrue(moderation.close_thread(self.user, self.thread))

        self.reload_thread()
        self.assertTrue(self.thread.is_closed)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("closed thread.", event.message)
        self.assertEqual(event.icon, "lock")

    def test_close_invalid_thread(self):
        """close_thread fails gracefully for opened thread"""
        moderation.close_thread(self.user, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_closed)
        self.assertFalse(moderation.close_thread(self.user, self.thread))

    def test_open_thread(self):
        """open_thread closes thread"""
        moderation.close_thread(self.user, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_closed)
        self.assertTrue(moderation.open_thread(self.user, self.thread))

        self.reload_thread()
        self.assertFalse(self.thread.is_closed)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("opened thread.", event.message)
        self.assertEqual(event.icon, "unlock-alt")

    def test_open_invalid_thread(self):
        """open_thread fails gracefully for opened thread"""
        self.assertFalse(self.thread.is_closed)
        self.assertFalse(moderation.open_thread(self.user, self.thread))

    def test_hide_thread(self):
        """hide_thread hides thread"""
        self.assertFalse(self.thread.is_hidden)
        self.assertTrue(moderation.hide_thread(self.user, self.thread))

        self.reload_thread()
        self.assertTrue(self.thread.is_hidden)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("hid thread.", event.message)
        self.assertEqual(event.icon, "eye-slash")

    def test_unhide_thread(self):
        """unhide_thread unhides thread"""
        moderation.hide_thread(self.user, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_hidden)
        self.assertTrue(moderation.unhide_thread(self.user, self.thread))

        self.reload_thread()
        self.assertFalse(self.thread.is_hidden)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("made thread visible.", event.message)
        self.assertEqual(event.icon, "eye")

    def test_delete_thread(self):
        """delete_thread deletes thread"""
        self.assertTrue(moderation.delete_thread(self.user, self.thread))
        with self.assertRaises(Thread.DoesNotExist):
            self.reload_thread()
