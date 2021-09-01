from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(title="Тест",
                                          slug="test-slug",
                                          description="Тестовый текст")
        self.user = User.objects.create_user(username="Guest")
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(text="Тестовый текст",
                                        group=self.group,
                                        author=self.user)

    def test_views_templates(self):
        cache.clear()
        templates_pages = {
            "index.html": reverse("index"),
            "posts/create_post.html": reverse("post_create"),
            "posts/group_list.html": (
                reverse("group_posts", kwargs={"slug": self.group.slug})
            ),
        }
        for template, reverse_name in templates_pages.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        cache.clear()
        responses = self.guest_client.get(reverse("index"))
        self.assertEqual(responses.context["page_obj"][0], self.post)

    def test_group_correct_context(self):
        response = self.authorized_client.get(reverse(
            "group_posts",
            kwargs={"slug": self.group.slug})
        )
        self.assertEqual(response.context["group"], self.group)
        self.assertEqual(response.context["page_obj"][0], self.post)

    def test_new_post_correct_context(self):
        response = self.authorized_client.get(reverse("post_create"))
        form_fields = {"text": forms.fields.CharField,
                       "group": forms.fields.ChoiceField}
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_correct_context(self):
        response = self.authorized_client.get(reverse(
            "post_edit",
            kwargs={"post_id": self.post.pk}))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_id_correct_context(self):
        response = self.authorized_client.get(
            reverse("post", kwargs={"post_id": self.post.pk}))
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(response.context["post"], self.post)

    def test_first_page_contains_ten_records(self):
        cache.clear()
        for _ in range(13):
            Post.objects.create(text="Тестовый текст", author=self.user)
        response = self.guest_client.get(reverse("index"))
        self.assertEqual(len(response.context.get("page_obj").object_list), 10)
        response = self.guest_client.get(reverse("index") + "?page=2")
        self.assertEqual(len(response.context.get("page_obj").object_list), 4)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title="testGroup",
            slug="test-slug2",
        )
        cls.author = User.objects.create_user(username="TEST_USR")
        for _ in range(13):
            Post.objects.create(
                text="TestText", author=cls.author, group=cls.group,)

    def setUp(self):
        self.client = Client()

    def test_first_page_contains_ten_records(self):
        cache.clear()
        response = self.client.get(reverse("index"))
        self.assertEqual(len(response.context.get("page_obj").object_list), 10)

    def test_second_page_contains_three_records(self):
        response = self.client.get(reverse("index") + "?page=2")
        self.assertEqual(len(response.context.get("page_obj").object_list), 3)

    def test_group_contains_ten_records(self):
        response = self.client.get(
            reverse("group_posts", kwargs={"slug": "test-slug2"}))
        self.assertEqual(len(response.context.get("page_obj").object_list), 10)

    def test_profile_contains_ten_records(self):
        response = self.client.get(
            reverse("profile", kwargs={"username": f"{self.author}"}))
        self.assertEqual(len(response.context.get("page_obj").object_list), 10)
