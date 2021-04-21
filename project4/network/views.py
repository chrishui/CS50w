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
            })

        # If submitted form is Invalid
        else:
            return render(request, "network/index.html", {
                "form": form,
            })

    #posts = Post.objects.all()
    # Get request
    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": Post.objects.all(),
        # Need to add all posts
    })
