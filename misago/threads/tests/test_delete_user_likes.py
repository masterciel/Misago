from django.test import RequestFactory

from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase, create_test_user

from misago.threads import testutils
from misago.threads.api.postendpoints.patch_post import patch_is_liked
from misago.threads.models import Post


class DeleteUserLikesTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def get_request(self, user=None):
        request = self.factory.get("/customer/details")
        request.user = user or self.user
        request.user_ip = "127.0.0.1"

        return request

    def test_anonymize_user_likes(self):
        """post's last like is anonymized by user.anonymize_data"""
        category = Category.objects.get(slug="first-category")
        thread = testutils.post_thread(category)
        post = testutils.reply_thread(thread)
        post.acl = {"can_like": True}

        user = create_test_user("OtherUser", "otheruser@example.com")

        patch_is_liked(self.get_request(self.user), post, 1)
        patch_is_liked(self.get_request(user), post, 1)

        user.delete_content()

        last_likes = Post.objects.get(pk=post.pk).last_likes
        self.assertEqual(
            last_likes, [{"id": self.user.id, "username": self.user.username}]
        )
