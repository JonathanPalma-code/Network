from datetime import datetime
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

        cls.user_data = {
            'username': 'Gandalf',
            'email': 'gandalf@email.com',
            'password': 'secretpass',
            'confirmation': 'secretpass'  
        }

        cls.user_data_2 = { 
            'username': 'Legolas',
            'email': 'legolas@email.com',
            'password': 'elfpass',
            'confirmation': 'elfpass'

        }

    # ! TEST LIKE / UNLIKE IN POST

    def test_like_in_post(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)

        response = self.client.post('/add_post', {
            'content': 'This is my first post',
        }, content_type='application/json')

        profile = Profile.objects.get(user=user)
        post = Post.objects.get(original_poster=profile, content='This is my first post') 

        response = self.client.put(f'/post/{post.id}', {
            'likes': 'Gandalf'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.put(f'/post/{post.id}', {
            'likes': ''
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    # ! TEST UPDATE POST

    def test_update_post(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)
        response = self.client.post('/add_post', {
            'content': 'This is my first post'
        }, content_type='application/json')

        profile = Profile.objects.get(user=user)
        post = Post.objects.get(original_poster=profile, content='This is my first post') 

        response = self.client.put(f'/post/{post.id}', {
            'content': 'This is my second post'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Post updated successfully"})

    # ! TEST DISPLAY PROFILES/PROFILE

    def test_display_all_profiles_GET(self):
        response = self.client.get('/profiles')

        self.assertEqual(response.status_code, 200)

    def test_display_post_GET(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)
        profile = Profile.objects.get(user=user)
        response = self.client.get(f'/profile/{profile.user}')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, profile.serialize())

    def test_display_error_profile_GET(self):
        response = self.client.get('/profile/harry')

        self.assertEqual(response.status_code, 404)

    def test_error_profile_POST(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)
        profile = Profile.objects.get(user=user)
        response = self.client.post(f'/profile/{profile.user}')

        self.assertJSONEqual(str(response.status_code), 400)

    # ! TEST FOLLOW USER

    def test_follow_user(self):
        self.client.post(self.register_url, self.user_data)
        user_followed = auth.get_user(self.client)
        self.client.logout()
        self.client.post(self.register_url, self.user_data_2)
        user = auth.get_user(self.client)
        profile = Profile.objects.get(user=user)
        response = self.client.put(f'/profile/{profile.user}', {
            'following': [str(user_followed)]
            }, content_type='application/json')

        self.assertJSONEqual(str(response.status_code), 200)
        self.assertJSONEqual(response.content, {"message": "Profile has been added successfully"})

    def test_unfollow_user(self):
        self.client.post(self.register_url, self.user_data)
        user_followed = auth.get_user(self.client)
        self.client.logout()
        self.client.post(self.register_url, self.user_data_2)
        user = auth.get_user(self.client)
        profile = Profile.objects.get(user=user)
        self.client.put(f'/profile/{profile.user}', {
            'following': [str(user_followed)]
            }, content_type='application/json')
        response = self.client.put(f'/profile/{profile.user}', {
            'following': [str(user_followed)]
            }, content_type='application/json')

        self.assertJSONEqual(str(response.status_code), 200)
        self.assertJSONEqual(response.content, {"message": "Profile has been deleted successfully"})

    # ! TEST Display FOLLOWING USERS POSTS

    def test_following_users_posts(self):
        self.client.post(self.register_url, self.user_data)
        user_followed = auth.get_user(self.client)
        profile_followed = Profile.objects.get(user=user_followed)
        self.client.post('/add_post', {
            "content": "This is my first post",
        }, content_type='application/json')
        self.client.logout()
        self.client.post(self.register_url, self.user_data_2)
        user = auth.get_user(self.client)
        profile = Profile.objects.get(user=user)
        self.client.put(f'/profile/{profile.user}', {
            'following': [str(user_followed)]
            }, content_type='application/json')
        
        response = self.client.get('/following_posts')

        self.assertJSONEqual(str(response.status_code), 200)

    # ! TEST DISPLAY POSTS/POST AND ADD POSTS

    def test_index_no_user_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_index_with_user_add_post_form_GET(self):
        self.client.post(self.register_url, self.user_data)
        user = authenticate(username='Gandalf', password='secretpass')
        response = self.client.get(self.index_url, {'add_post_form': AddPostForm})

        self.assertTrue(user.is_authenticated)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_index_add_post_form_POST_API(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)
        response = self.client.post('/add_post', {
            'content': 'This is my first post'
        }, content_type='application/json')

        post = Post.objects.get(content='This is my first post')           

        self.assertEqual(response.status_code, 201)
        self.assertEqual(post.total_likes(), 0)
        self.assertEqual(Profile.objects.last().user.username, Post.objects.last().original_poster.user.username)

    def test_index_access_denied_POST_through_URL_GET_API(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.get('/add_post', {
            'content': 'This is my first post',
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_GET_display_1_post_JSON(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)
        self.client.post('/add_post', {
            "content": "This is my first post",
        }, content_type='application/json')

        profile = Profile.objects.get(user=user)
        post = Post.objects.get(id=2, original_poster=profile)

        response = self.client.get(f'/post/{post.id}')
        
        self.assertTrue(response.status_code, 200)
        self.assertJSONEqual(response.content, post.serialize())

    def test_GET_JSON_response_Post_doesnt_exist(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)
        response = self.client.get(f'/post/20')

        self.assertJSONEqual(str(response.status_code), 404)

    def test_POST_display_1_post_JSON(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)
        self.client.post('/add_post', {
            "content": "This is my first post",
        }, content_type='application/json')
        profile = Profile.objects.get(user=user)
        post = Post.objects.get(content='This is my first post', original_poster=profile)
        response = self.client.post(f'/post/{post.id}')

        self.assertJSONNotEqual(str(response.status_code), 200)

    def test_GET_display_posts(self):
        self.client.post(self.register_url, self.user_data)
        user = auth.get_user(self.client)
        self.client.post('/add_post', {
            "content": "This is my first post",
        }, content_type='application/json')
        response = self.client.get('/all_posts')

        self.assertJSONEqual(str(response.status_code), 200)

    def test_GET_url_doesnt_exist(self):
        response = self.client.get('/url_dont_exist')

        self.assertJSONEqual(str(response.status_code), 400)

 
    # ! ---- TEST USER AUTHENTICATION ----

    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')

    def test_register_and_login_POST(self):
        response = self.client.post(self.register_url, self.user_data)

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
        response = self.client.post(self.register_url, self.user_data)

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

    def test_register_user_with_username_taken(self):
        self.client.post(self.register_url, self.user_data)
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
