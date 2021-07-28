from django.test import TestCase, Client
from ..models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class UrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        Group.objects.create(
            title='test title',
            slug='test-slug'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='AndreyG')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage_NON_auth(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200, 'err001')

    def test_homepage_auth(self):
        response = self.authorized_client.get('/')
        self.assertEqual(response.status_code, 200, 'err002')

    def test_template_index(self):
        response = self.authorized_client.get('/')
        self.assertTemplateUsed(response, 'index.html', 'err03')

    def test_group_page_auth(self):
        response = self.authorized_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200, 'err004')

    def test_group_page_NON_auth(self):
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200, 'err005')

    def test_template_group(self):
        response = self.authorized_client.get('/group/test-slug/')
        self.assertTemplateUsed(response, 'posts/group.html', 'err06')

    def test_auth_user_add_post(self):
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200, 'err01')

    def test_template_add_post(self):
        response = self.authorized_client.get('/new/')
        self.assertTemplateUsed(response,
                                'posts/create_or_update_post.html', 'err02')

    def test_NOT_auth_usr_add_post(self):
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 302, 'err03')
