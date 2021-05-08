import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

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

# Index / all posts
def index(request):
    # Create new post, POST request
    if request.method == "POST":
        user = request.user
        content = request.POST["content"]
        if content != "":
            Post.objects.create(user=user, content=content, likes=0)

    # Display newest posts first
    posts_chronological = Post.objects.order_by('-created_at')

    # Paginator, limit to 10 entries per page
    paginator = Paginator(posts_chronological, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get request
    return render(request, "network/index.html", {
        "page_obj": page_obj,
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

    # Display target user's number of ...
    # following users:
    following_count = Profile.objects.filter(user=target_user).values('following').count()
    # followers:
    followers_count = Profile.objects.filter(user=target_user).values('followers').count()

    # Get request
    return render(request, "network/profile.html", {
        "posts": posts_chronological,
        "profile": target_user,
        "following_check": following_check,
        "following_count": following_count,
        "followers_count": followers_count,
    })

# Follow/unfollow
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

        # Else, follow target user
        else:
            user_profile.following.add(target_user)
            targetuser_profile.followers.add(user)

        return HttpResponseRedirect(reverse("profile", args=(target_user.id,)))

# Following users' posts
@login_required
def following(request):
    # Logged in user
    user = request.user

    # Obtain logged in user's following users' posts
    following_users = Profile.objects.filter(user=user).values_list('following')
    following_posts = []
    for profile in following_users:
        posts = Post.objects.filter(user=profile)
        for post in posts:
            following_posts.insert(0,post)

    return render(request, "network/following.html", {
        "posts": following_posts,
    })

# API routes
# Edit posts
@csrf_exempt
@login_required
def edit(request, post_id):
    post = Post.objects.get(id=post_id)

    # Update post's content
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # Request must be PUT
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)

# Like/unlike posts
@csrf_exempt
@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    if request.method == "POST":

        already_exists = Like.objects.filter(user=user, post=post).exists()

        # If user has previously liked the post, then unlike
        if already_exists:
            liked = Like.objects.get(user=user, post=post)
            liked.delete()
            post.likes -= 1
            like_count = post.likes
            post.save()
            return JsonResponse({
            "message": "Unliked",
            "like_count": like_count
            }, status=201)
        # If user has not liked the post, then like
        else:
            like = Like.objects.create(user=user, post=post)
            like.save()
            # Update like count
            post.likes += 1
            like_count = post.likes
            post.save()
            return JsonResponse({
            "message": "Liked",
            "like_count": like_count
            }, status=201)
