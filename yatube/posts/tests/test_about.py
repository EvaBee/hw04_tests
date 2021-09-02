from http import HTTPStatus

from django.test import Client, TestCase


class CreateFormTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_pages(self):
        urls = {"/about/tech/": HTTPStatus.OK.value,
                "/about/author/": HTTPStatus.OK.value,
                }
        for url, expected_value in urls.items():
            with self.subTest(url):
                response = self.guest_client.get(url, follow=False)
                self.assertEqual(response.status_code, expected_value)
