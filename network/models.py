from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=75, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'location': self.location,
            'birth date': self.dateValid()
        }

    def dateValid(self):
        if self.birth_date:
            return self.birth_date.strftime('%b %#d %Y')

    def __str__(self):
        return f'{self.user.username}'

class Follower(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def serialize(self):
        return {
            'id': self.id,
            'profile': self.profile.user.username
        }

    def __str__(self):
        return f'{self.profile.user.username}'

class Following(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')

    def serialize(self):
        return {
            'id': self.id,
            'profile': self.profile.user.username
        }
    
    def __str__(self):
        return f'{self.profile.user.username}'

class Post(models.Model):
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    original_poster = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_profile')
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    def total_likes(self):
        return self.likes.count()

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%b %#d %Y, %#I:%M %p'),
            'original_poster': self.original_poster.user.username,
            'likes': self.total_likes()
        }

    def __str__(self, n_characters = 50):
        slice_content = slice(n_characters)
        return f'{self.content[slice_content]}'

class Comment(models.Model):
    content = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_owner')

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%b %#d %Y, %#I:%M %p'),
            'post': self.post.content,
            'commenter': self.commenter.user.username
        }

    def __str__(self):
        return f'{self.commenter.user.username} commented "{self.content}" to post id nr. {self.post.id}'