from django.contrib import admin
from .models import User, Profile, Post, Comment

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location', 'birth_date')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'timestamp', 'original_poster')

admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
