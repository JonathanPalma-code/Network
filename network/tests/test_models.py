from django.test import TransactionTestCase
from network.models import User, Profile, Follower, Following, Post, Comment, Like
from datetime import date, datetime

class TestModels(TransactionTestCase):

    @classmethod
    def setUpClass(self):
        self.user1 = User.objects.create(
            username='Legolas',
            email='legolas@email.com'
        )
        self.user2 = User.objects.create(
            username='Sauron',
            email='sauron@email.com'
        )
        self.user3 = User.objects.create(
            username='Frodo',
            email='frodo@email.com'
        )
        self.user1.set_password('secretpass')
        self.user1.save()
        self.user2.set_password('secretpass')
        self.user2.save()
        self.user3.set_password('secretpass')
        self.user3.save()
        
        self.profile1 = Profile.objects.create(
            user=self.user1,
            location='Middle Earth',
            birth_date=date(1799, 3, 10)
        )
        self.profile2 = Profile.objects.create(
            user=self.user2,
            location='Middle Earth',
            birth_date=date(1739, 3, 10)
        )
        self.profile3 = Profile.objects.create(
            user=self.user3,
            location='Middle Earth',
            birth_date=date(1990, 3, 10)
        )
        self.follower = Follower.objects.create(profile=self.profile2)
        self.following = Following.objects.create(profile=self.profile3)
    
        self.post = Post.objects.create(
            content='This is my first post.',
            timestamp=datetime.now,
            original_poster=self.profile2
        )

        self.comment = Comment.objects.create(
            content='Nice!',
            timestamp=datetime.now,
            post=self.post,
            commenter=self.profile3
        )

        self.like = Like.objects.create(
            post=self.post,
            like_owner=self.profile1
        )

    def test_profile_serialize(self):
        self.assertEqual(self.profile1.serialize(), {
            'id': 1,
            'user': self.profile1.user.username,
            'location': self.profile1.location,
            'birth date': self.profile1.birth_date.strftime('%b %#d %Y')
        })

    def test_profile__str__(self):
        self.assertEqual(self.profile1.__str__(), self.profile1.user.username)

    def test_follower_serialize(self):
        self.assertEqual(self.follower.serialize(), {
            'id': 1,
            'profile': self.profile2.user.username
        })

    def test_follower__str__(self):
        self.assertEqual(self.follower.__str__(), self.profile2.user.username)

    def test_following_serialize(self):
        self.assertEqual(self.following.serialize(), {
            'id': 1,
            'profile': self.profile3.user.username
        })

    def test_following__str__(self):
        self.assertEqual(self.following.__str__(), 'Frodo')

    def test_post_serialize(self):
        self.assertEqual(self.post.serialize(), {
            'id': 1,
            'content': 'This is my first post.',
            'timestamp': self.post.timestamp.strftime('%b %#d %Y, %#I:%M %p'),
            'original_poster': self.post.original_poster.user.username
        })

    def test_post__str__(self):
        self.assertEqual(self.post.__str__(5), 'This ')

    def test_comment_serialize(self):
        self.assertEqual(self.comment.serialize(), {
            'id': 1,
            'content': 'Nice!',
            'timestamp': self.comment.timestamp.strftime('%b %#d %Y, %#I:%M %p'),
            'post': self.comment.post.content,
            'commenter': 'Frodo'
        })

    def test_comment__str__(self):
        self.assertEqual(self.comment.__str__(), 'Frodo commented "Nice!" to post id nr. 1')
    
    def test_like_serialize(self):
        self.assertEqual(self.like.serialize(), {
            'id': 1,
            'post': self.post.content,
            'like_owner': self.profile1.user.username
        })

    def test_like__str__(self):
        self.assertEqual(self.like.__str__(), 'Legolas liked "This is my first post."')
