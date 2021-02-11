from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile
from .forms import AddPostForm

def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        profile = Profile.objects.get(user=user)
        if request.method == 'POST':
            form = AddPostForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                post = Post.objects.create(content=content, original_poster=profile)
                post.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'network/index.html', {
                    'add_post_form': form
                })
        return render(request, 'network/index.html', {
            'add_post_form': AddPostForm()
        })
    return render(request, 'network/index.html', )

def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'network/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'network/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'network/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile.objects.create(user=user, location='', birth_date=None)
            profile.save()
        except IntegrityError:
            return render(request, 'network/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'network/register.html')
