from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Post, Group

User = get_user_model()


class PostViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(title='Тест',
                                          slug='test-slug',
                                          description='Тестовый текст')
        self.user = User.objects.create_user(username='Guest')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(text='Тестовый текст',
                                        group=self.group,
                                        author=self.user)

    def test_views_templates(self):
        templates_pages = {
            reverse('index'): 'index.html',
            reverse('group_posts', kwargs={'slug': self.group.slug}):
                'posts/group.html',
            reverse('new_post'): 'posts/create_or_update_post.html',
        }
        for reverse_name, template in templates_pages.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.context['page'].object_list[0], self.post)

    def test_group_correct_context(self):
        response = self.authorized_client.get(reverse(
            'group_posts',
            kwargs={'slug': self.group.slug})
        )
        self.assertEqual(response.context['group'], self.group)
        self.assertEqual(response.context['page'].object_list[0], self.post)

    def test_new_post_correct_context(self):
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {'text': forms.fields.CharField,
                       'group': forms.fields.ChoiceField}
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_correct_context(self):
        response = self.authorized_client.get(reverse(
            'post_edit',
            kwargs={
                'username': self.user,
                'post_id': self.post.pk}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_id_correct_context(self):
        response = self.authorized_client.get(
            reverse('post', kwargs={'username': self.user.username,
                                    'post_id': self.post.pk}))
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['post'], self.post)

    def test_first_page_contains_ten_records(self):
        for _ in range(12):
            Post.objects.create(text='Тестовый текст', author=self.user)
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)
        response = self.guest_client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)
