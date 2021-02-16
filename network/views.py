import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post, Profile
from .forms import AddPostForm

def index(request):

    # Authenticate users can add post
    if request.user.is_authenticated:
        return render(request, 'network/index.html', {
            'add_post_form': AddPostForm()
        })
    return render(request, 'network/index.html')

@login_required
def add_post(request):

    # Add a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get data from the form?
    data = json.loads(request.body)

    likes = []

    content = data.get("content", "")

    # Add data to API
    post = Post(
        content=content,
        original_poster=Profile.objects.get(user=request.user)
    )
    post.save()
    for like in likes:
        post.likes.add(like)
    post.save()

    return JsonResponse({"message": "Post sent successfully"}, status=201)

def post(request, post_id):
        
    # Query for requested post
    profile = Profile.objects.get(user=request.user)
    try:
        post = Post.objects.get(original_poster=profile, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # GET Data in Json format (serialize method in models.py)
    if request.method == "GET":
        return JsonResponse(post.serialize())

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def nav_bar(request, nav_bar):

    # Filter emails returned based on mailbox
    if nav_bar == "all_posts":
        posts = Post.objects.all()
    elif nav_bar == "follower":
        pass
    else:
        return JsonResponse({"error": "Invalid Link."}, status=400)

    # Return emails in reverse chronologial order
    posts = posts.order_by("-timestamp")
    return JsonResponse([post.serialize() for post in posts], safe=False)

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
