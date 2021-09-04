from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post, User


class CreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username="AndreyG")
        cls.post = Post.objects.create(
            text="тестовый текст",
            author=cls.author)
        cls.group = Group.objects.create(
            title="test group",
            slug="slug")
        cls.form = PostForm()

    def setUp(self):
        self.un_auth_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_add_post(self):
        form_data = {
            "text": "тестовый текст",
            "group": self.group.slug,
        }
        self.un_auth_client.post(reverse("post_create"),
                                 data=form_data,
                                 follow=True,)
        self.assertTrue(
            Post.objects.filter(text=form_data["text"]).exists())
        self.assertEqual(self.post.text, form_data["text"])

    def test_edit_post(self):
        counter = Post.objects.count()
        form_data = {"text": "text"}
        self.authorized_client.post(
            reverse("post_edit", kwargs={"post_id": self.post.id}),
            data=form_data, follow=True)
        self.assertEqual(Post.objects.count(), counter)
        post = Post.objects.first()
        self.assertTrue(post.text, form_data["text"])
        self.assertTrue(
            Post.objects.filter(
                text=form_data["text"],
            ).exists()
        )
