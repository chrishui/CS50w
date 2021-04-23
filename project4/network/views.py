from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User
from .models import *

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # Create user profile, to track following/followers
            profile = Profile.objects.create(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# Create Post
class PostForm(forms.Form):
    content = forms.CharField(label='', max_length=64, widget=forms.Textarea)

# Index / all posts
def index(request):
    # Display posts chronologically (newest first)
    posts_chronological = []
    for object in Post.objects.all():
        posts_chronological.insert(0,object)

    # Create new post (Note: requres user to be authenticated)
    if request.method == "POST":
        form = PostForm(request.POST)
        user = request.user

        # Check if submitted form is valid
        if form.is_valid():
            content = form.cleaned_data["content"]

            # Create a new post instance
            newEntry = Post.objects.create(user=user, content=content)
            newEntry.save()

            # Return index page with message confirmation (?)
            return render(request, "network/index.html", {
                "form": PostForm(),
                "message": "Post created!",
                "posts": posts_chronological,
            })

        # If submitted form is Invalid
        else:
            return render(request, "network/index.html", {
                "form": form,
            })

    # Get request
    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": posts_chronological,
    })

# Profile
def profile(request, user_id):
    # Get User object from user id
    target_user = User.objects.get(id=user_id)

    # Logged in user
    user = request.user

    # Display posts chronologically (newest first), posted by user
    posts_chronological = []
    for object in Post.objects.filter(user=target_user):
        posts_chronological.insert(0,object)

    # Check whether target user is followed/not followed by user
    following_check = Profile.objects.filter(user=user, following=target_user).exists()

    # Get request
    return render(request, "network/profile.html", {
        "posts": posts_chronological,
        "profile": target_user,
        "following_check": following_check,
    })

# follow/unfollow
def follow(request, user_id):
    if request.method == "POST":
        # Get target user's User object from user id
        target_user = User.objects.get(id=user_id)
        targetuser_profile = Profile.objects.get(user=target_user)

        # Logged in user
        user = request.user
        user_profile = Profile.objects.get(user=user)

        # Check if logged in user is already following target user
        already_exist = Profile.objects.filter(user=user, following=target_user).exists()

        # If already exist, remove from following
        if already_exist:
            user_profile.following.remove(target_user)
            targetuser_profile.followers.remove(user)
            # also need to add follower (TODO)

        # Else, follow target user
        else:
            user_profile.following.add(target_user)
            targetuser_profile.followers.add(user)
            # also need to add follower (TODO)

        return HttpResponseRedirect(reverse("profile", args=(target_user.id,)))
