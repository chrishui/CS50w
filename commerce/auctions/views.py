from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User
from .models import *

import operator

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

@login_required
def createListing(request):
    # Post request
    if request.method == "POST":
        form = ListingForm(request.POST)
        user = request.user

        # If submitted form is valid
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]

            # Create new entry for Listing
            newEntry = Listing.objects.create(user=user, name=name, description=description, price=price, category=category, image=image)
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

# Individual listing view
class BidForm(forms.Form):
    price = forms.IntegerField(label='Submit bid ($):')

@login_required
def listing(request, listing_id):
    # Requested listing
    listing = Listing.objects.get(pk=listing_id)
    # Watchlist
    watchlist_check = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    # Check for submitted listing bids
    bid_check = Bid.objects.filter(listing=listing).exists()
    if bid_check == True:
        currentBid = Bid.objects.get(listing=listing)
        currentPrice = currentBid.bidPrice
        bidCount = currentBid.bidCount
        highestBidder = currentBid.user
    # If no bids for listing, show listing's original price
    else:
        currentPrice = listing.price
        bidCount = 0

    # Get request
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist_check": watchlist_check,
        "currentPrice": currentPrice,
        "bidForm": BidForm(),
        "bidCount": bidCount,
        "highestBidder": highestBidder,
    })

# Watchlist
@login_required
def watchlist(request, listing_id):
    if request.method == "POST":
        # Accessing the listing item
        listing = Listing.objects.get(pk=listing_id)

        # Finding logged in user
        user = request.user

        # Check if listing already in Watchlist
        already_exists = Watchlist.objects.filter(user=user, listing=listing).exists()

        # If already exists, remove from watchlist
        if already_exists:
            Watchlist.objects.filter(user=user, listing=listing).delete()

        # Else, create new entry for watchlist
        else:
            newEntry = Watchlist.objects.create(user=user, listing=listing)
            newEntry.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

# User's saved watchlist
@login_required
def userWatchlist(request):
    user = request.user
    # Get listings IDs in user's watchlist
    userWatchlist_IDs = Watchlist.objects.filter(user=user).values('listing_id')
    listings = Listing.objects.filter(id__in=userWatchlist_IDs)
    #userlistings = Listing.watchlist.objects.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })

# Bid
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        # User's submitted bid
        bidForm = BidForm(request.POST)
        if bidForm.is_valid():
            bid = bidForm.cleaned_data["price"]

            # Check for submitted listing bids
            bid_check = Bid.objects.filter(listing=listing).exists()

            # If there are no bids on listing
            if bid_check == False:
                # If bid is less than listing Price
                if bid < listing.price:
                    return render(request, "auctions/error.html", {
                        "message": "Bid must be higher than current price!"
                    })
                # Create new bid instance
                else:
                    newEntry = Bid.objects.create(user=user, listing=listing, bidPrice=bid, bidCount=1)
                    newEntry.save()

            # If listing has been previously bid
            else:
                currentBid = Bid.objects.get(listing=listing)
                currentPrice = currentBid.bidPrice

                # If bid is less than current price / highest bid
                if bid < currentPrice:
                    return render(request, "auctions/error.html", {
                        "message": "Bid must be higher than current price!"
                    })

                # Else, update bidPrice in model instance
                else:
                    bidCount = Bid.objects.get(listing=listing).bidCount
                    Bid.objects.filter(listing=listing).update(bidPrice=bid, user=user, bidCount=bidCount+1)

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
