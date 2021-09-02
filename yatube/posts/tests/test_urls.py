from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class UrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username="Yoname")
        cls.group = Group.objects.create(
            title="test_group",
            slug="test_slug",
            description="какое-то описание",
        )
        cls.post = Post.objects.create(
            text="Тестовая запись",
            author=UrlTest.author,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="test_user")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author = Client()
        self.post_id = UrlTest.post.id
        self.author_client = Client()
        self.author_client.force_login(UrlTest.author)

    def tests_with_no_auth(self):
        urls = {
            "/": HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK.value,
            f'/profile/{self.user}/': HTTPStatus.OK.value,
            f'/posts/{self.post_id}/': HTTPStatus.OK.value,
            '/unexisting_page/': HTTPStatus.NOT_FOUND.value,
            '/create/': HTTPStatus.FOUND.value,
        }
        for url, expected_value in urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, expected_value)

    def test_template_all_users(self):
        templates_url_names = {
            "index.html": "/",
            "posts/group_list.html": f"/group/{self.group.slug}/",
            "profile.html": f"/profile/{self.user}/",
            "posts/post_detail.html": f"/posts/{self.post_id}/"
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_create_auth_user(self):
        response = self.authorized_client.get("/create/")
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_author_edit_post(self):
        response = self.authorized_client.get(
            f"/posts/{self.post.id}/edit/", follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_templates_auth_user(self):
        response = self.authorized_client.get(f"/posts/{self.post_id}/edit/")
        self.assertRedirects(response, reverse(
            "post", kwargs={"post_id": self.post_id}))
