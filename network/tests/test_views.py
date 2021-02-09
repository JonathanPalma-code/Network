from django.test import TransactionTestCase, Client
from django.urls import reverse
from network.models import User
import json

class TestViews(TransactionTestCase):

    def setUp(self):
        client = Client()
        self.index_url = reverse('index')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        self.user = User.objects.create_user(
            username='Gandalf',
            email='gandlaf@email.com'
        )
        self.user.set_password('secretpass')
        self.user.save()

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')

    def test_register_and_login_POST(self):
        response = self.client.post(self.register_url, {
            'username': self.user.username,
            'email': self.user.email,
            'password': 'secretpass',
            'confirmation': 'secretpass'
        })

        self.assertTrue(response)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(self.login_url, {
            'username': self.user.username, 
            'password': 'secretpass'
        })

        self.assertTrue(response)
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.client.post(self.login_url, {
            'username': self.user.username, 
            'password': 'secretpass'
        })
        self.assertEqual(response.status_code, 302)
        self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_login_unsuccess(self):
        response = self.client.post(self.login_url, {
            'username': self.user.username, 
            'password': 'secret'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')
        
    def test_register_pass_dont_match_POST(self):
        response = self.client.post(self.register_url, {
            'username': self.user.username,
            'email': self.user.email,
            'password': self.user.password,
            'confirmation': 'secret'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')
        self.assertEqual(self.user.username, 'Gandalf')