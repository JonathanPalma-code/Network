from django.test import TransactionTestCase, Client
from django.contrib.auth import authenticate
from django.urls import reverse
from network.models import User, Profile, Post
from django.contrib import auth
from django.db import IntegrityError

from network.forms import AddPostForm

class TestViews(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        client = Client()
        cls.index_url = reverse('index')
        cls.register_url = reverse('register')
        cls.login_url = reverse('login')
        cls.logout_url = reverse('logout')

    def test_index_no_form_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_index_add_post_form_GET(self):
        response = self.client.post(self.register_url, {
            'username': 'Gandalf',
            'email': 'gandalf@email.com',
            'password': 'secretpass',
            'confirmation': 'secretpass'
        })
        user = authenticate(username='Gandalf', password='secretpass')
        response = self.client.get(self.index_url, {'add_post_form': AddPostForm})

        self.assertTrue(user.is_authenticated)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_index_add_post_form_POST(self):
        self.client.post(self.register_url, {
            'username': 'Gandalf',
            'email': 'gandalf@email.com',
            'password': 'secretpass',
            'confirmation': 'secretpass'
        })
        user = auth.get_user(self.client)
        response = self.client.post(self.index_url, {
            'content': 'This is my first post',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")
        self.assertEqual(Profile.objects.last().user.username, Post.objects.last().original_poster.user.username)

    def test_index_add_post_form_invalid_POST(self):
        self.client.post(self.register_url, {
            'username': 'Gandalf',
            'email': 'gandalf@email.com',
            'password': 'secretpass',
            'confirmation': 'secretpass'
        })
        response = self.client.post(self.index_url, {
            'content': '',
        })

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
            'username': 'Gandalf',
            'email': 'gandalf@email.com',
            'password': 'secretpass',
            'confirmation': 'secretpass'
        })

        self.assertTrue(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profile.objects.last().user.username, 'Gandalf')
        
        self.client.post(self.logout_url)
        response = self.client.post(self.login_url, {
            'username': 'Gandalf', 
            'password': 'secretpass'
        })
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        response = self.client.post(self.register_url, {
            'username': 'Gandalf',
            'email': 'gandalf@email.com',
            'password': 'secretpass',
            'confirmation': 'secretpass'
        })

        self.assertEqual(response.status_code, 302)
        self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_login_unsuccess(self):
        response = self.client.post(self.login_url, {
            'username': 'Gandalf', 
            'password': 'secret'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')
        
    def test_register_pass_dont_match_POST(self):
        response = self.client.post(self.register_url, {
            'username': 'Gandalf',
            'email': 'gandalf@email.com',
            'password': 'secretpass',
            'confirmation': 'secret'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')

    def test_reguster_user_with_username_taken(self):
        self.client.post(self.register_url, {
            'username': 'Gandalf',
            'email': 'gandalf@email.com',
            'password': 'secretpass',
            'confirmation': 'secretpass'
        })
        self.client.post(self.logout_url)

        with self.assertRaises(IntegrityError) as context:
            response = self.client.post(self.register_url, {
                'username': 'Gandalf',
                'email': 'gandalfthegrey@email.com',
                'password': 'secretpass',
                'confirmation': 'secretpass'
            })
            User.objects.create(username='Gandalf', email='gandalfthegrey@email.com',
            password='secretwhite')

        self.assertTrue('UNIQUE constraint failed' in str(context.exception))
        self.assertTemplateUsed(response, 'network/register.html')
