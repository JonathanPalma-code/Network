from django.contrib import admin
from .models import User, Profile, Follower, Following, Post, Comment, Like 

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location', 'birth_date', 'photo')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'timestamp', 'orignal_poster')

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Follower)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
