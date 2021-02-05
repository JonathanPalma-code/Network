from django.test import SimpleTestCase
from django.urls import reverse, resolve
from network.views import index, login_view, logout_view, register

class TestUrls(SimpleTestCase):

    def test_list_url_index_is_resolved(self):
        url = reverse('index')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, index)

    def test_list_url_login_is_resolved(self):
        url = reverse('login')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, login_view)

    def test_list_url_logout_is_resolved(self):
        url = reverse('logout')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, logout_view)

    def test_list_url_register_is_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)
        