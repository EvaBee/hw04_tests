from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Post, User


class CreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username="AndreyG")
        cls.post = Post.objects.create(
            text="текст",
            author=cls.author,
        )

        cls.form = PostForm()

    def setUp(self):
        self.un_auth_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_add_post(self):
        counter = Post.objects.count()
        form_data = {
            "text": "Тестовый текст",
            "group": "group"
        }

        self.un_auth_client.post(reverse("post_create"),
                                 data=form_data,
                                 follow=True,)
        self.assertEqual(Post.objects.count(), counter)

        self.assertTrue(
            Post.objects.all().exists())
        self.assertEqual(Post.objects.count(), counter)

    def test_edit_post(self):
        counter = Post.objects.count()
        form_data = {'text': 'text'}
        response = self.authorized_client.post(
            reverse('post_edit', kwargs={"post_id": self.post.id}),
            data=form_data)
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), counter)
