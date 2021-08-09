from django.test import TestCase

from ..models import Post, Group, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        author = User.objects.create_user(username="TEST_USR")
        cls.Post = Post.objects.create(
            text="тестовыйпостна1",
            author=author,
        )
        cls.Group = Group.objects.create(
            title="test"
        )

    def test_object_name_is_title_field(self):
        group = PostModelTest.Group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_object_name_title_have_15_symbols(self):
        post = PostModelTest.Post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post.text))
