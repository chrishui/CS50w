from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User
from .models import *

# Main page
def index(request):
    return render(request, "auctions/index.html" , {
        "listings": Listing.objects.all()
    })

# Login
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

# Logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# Create Listing
CATEGORIES = (("Fashion","Fashion"), ("Toys", "Toys"), ("Electronics", "Electronics"), ("Home", "Home"), ("Misc.", "Misc."),)
# Forms
class ListingForm(forms.Form):
    name = forms.CharField(label='Listing name:', max_length = 64)
    description = forms.CharField(label='Description:', widget=forms.Textarea, max_length = 64)
    price = forms.IntegerField(label='Price($):')
    category = forms.ChoiceField(label='Category:', required=False, choices=CATEGORIES)
    image = forms.URLField(label='Image (URL):', required=False)

def createListing(request):
    # Post request
    if request.method == "POST":
        form = ListingForm(request.POST)

        # If submitted form is valid
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]

            # Create new entry for Listing
            newEntry = Listing(name=name, description=description, price=price, category=category, image=image)
            newEntry.save()

            # Return createListing page with message confirmation
            return render(request, "auctions/createListing.html", {
                "forms": ListingForm(),
                "message": "Listing created!"
            })

        # If submitted form is Invalid
        else:
            return render(request, "auctions/createListing.html", {
                "forms": form
            })

    # Get request
    return render(request, "auctions/createListing.html", {
        "forms": ListingForm()
    })
