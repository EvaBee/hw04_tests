from django.test import Client, TestCase


class CreateFormTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_pages(self):
        urls = {'/about/tech/': 200,
                '/about/author/': 200,
                }
        for url, expected_status in urls.items():
            with self.subTest(url):
                response = self.guest_client.get(url, follow=False)
                self.assertEqual(response.status_code, expected_status)

