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

# Listing info
def listingInfo(request):
    no_activeListings = len(Listing.objects.filter(status=True))
    no_inactiveListings = len(Listing.objects.filter(status=False))
    try:
        user = request.user
        no_userWatchlist = len(Watchlist.objects.filter(user=user))
    except:
        no_userWatchlist = None
    return no_activeListings, no_inactiveListings, no_userWatchlist

# Main page (Active listings)
def index(request):
    # Populate layout banners
    info = listingInfo(request)
    no_activeListings, no_inactiveListings, no_userWatchlist = info[0], info[1], info[2]
    return render(request, "auctions/index.html" , {
        "listings": Listing.objects.filter(status=True),
        "no_activeListings": no_activeListings,
        "no_inactiveListings": no_inactiveListings,
        "no_userWatchlist": no_userWatchlist,

    })

# Inactive listings
def inactive(request):
    # Populate layout banners
    info = listingInfo(request)
    no_activeListings, no_inactiveListings, no_userWatchlist = info[0], info[1], info[2]
    return render(request, "auctions/inactive.html", {
        "listings": Listing.objects.filter(status=False),
        "no_activeListings": no_activeListings,
        "no_inactiveListings": no_inactiveListings,
        "no_userWatchlist": no_userWatchlist,
    })

# Login
def login_view(request):
    # Populate layout banners
    info = listingInfo(request)
    no_activeListings, no_inactiveListings, no_userWatchlist = info[0], info[1], info[2]

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
        return render(request, "auctions/login.html", {
            "no_activeListings": no_activeListings,
            "no_inactiveListings": no_inactiveListings,
            "no_userWatchlist": no_userWatchlist,
        })

# Logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Register
def register(request):
    # Layout banners
    info = listingInfo(request)
    no_activeListings, no_inactiveListings, no_userWatchlist = info[0], info[1], info[2]

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
        return render(request, "auctions/register.html", {
            "no_activeListings": no_activeListings,
            "no_inactiveListings": no_inactiveListings,
            "no_userWatchlist": no_userWatchlist,
        })

# Create Listing
CATEGORIES = (("Fashion","Fashion"), ("Toys", "Toys"), ("Electronics", "Electronics"), ("Home", "Home"), ("Misc.", "Misc."),)
# Listing forms
class ListingForm(forms.Form):
    name = forms.CharField(label='Listing name:', max_length = 64)
    description = forms.CharField(label='Description:', widget=forms.Textarea, max_length = 64)
    price = forms.IntegerField(label='Price($):')
    category = forms.ChoiceField(label='Category:', required=False, choices=CATEGORIES)
    image = forms.URLField(label='Image (URL):', required=False)

@login_required
def createListing(request):
    # Layout banners
    info = listingInfo(request)
    no_activeListings, no_inactiveListings, no_userWatchlist = info[0], info[1], info[2]

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
                "message": "Listing created!",
                "no_activeListings": no_activeListings,
                "no_inactiveListings": no_inactiveListings,
                "no_userWatchlist": no_userWatchlist,
            })

        # If submitted form is Invalid
        else:
            return render(request, "auctions/createListing.html", {
                "forms": form
            })

    # Get request
    return render(request, "auctions/createListing.html", {
        "forms": ListingForm(),
        "no_activeListings": no_activeListings,
        "no_inactiveListings": no_inactiveListings,
        "no_userWatchlist": no_userWatchlist,
    })

# Individual listing view
class BidForm(forms.Form):
    price = forms.IntegerField(label='Submit bid ($):')
class CommentForm(forms.Form):
    comment = forms.CharField(label='Add comment:', widget=forms.Textarea, max_length=64)

@login_required
def listing(request, listing_id):
    # Layout banners
    info = listingInfo(request)
    no_activeListings, no_inactiveListings, no_userWatchlist = info[0], info[1], info[2]

    # Requested listing
    listing = Listing.objects.get(pk=listing_id)
    # Watchlist
    watchlist_check = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    # Bids - Check for submitted listing bids
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
        highestBidder = None

    # Administrative - listing status
    user = request.user
    status = Listing.objects.get(pk=listing_id).status
    listingCreator = Listing.objects.get(pk=listing_id).user

    # Get request
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist_check": watchlist_check,
        "currentPrice": currentPrice,
        "bidForm": BidForm(),
        "bidCount": bidCount,
        "highestBidder": highestBidder,
        "commentForm": CommentForm(),
        "comments": Comment.objects.filter(listing=listing),
        "status": status,
        "listingCreator": listingCreator,
        "no_activeListings": no_activeListings,
        "no_inactiveListings": no_inactiveListings,
        "no_userWatchlist": no_userWatchlist,
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
    # Layout banners
    info = listingInfo(request)
    no_activeListings, no_inactiveListings, no_userWatchlist = info[0], info[1], info[2]

    user = request.user
    # Get listings IDs in user's watchlist
    userWatchlist_IDs = Watchlist.objects.filter(user=user).values('listing_id')
    listings = Listing.objects.filter(id__in=userWatchlist_IDs)
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "no_activeListings": no_activeListings,
        "no_inactiveListings": no_inactiveListings,
        "no_userWatchlist": no_userWatchlist,
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

# Comments
@login_required
def comments(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        # User's submitted comment
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.cleaned_data["comment"]
            # Create a new comment instance
            newEntry = Comment.objects.create(user=user, listing=listing, comment=comment)
            newEntry.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

# Close auction
@login_required
def closeAuction(request, listing_id):
    if request.method=="POST":
        Listing.objects.filter(pk=listing_id).update(status=False)

        return HttpResponseRedirect(reverse("inactive"))

# Categories
class CategoryForm(forms.Form):
    category = forms.ChoiceField(label='Category:', required=False, choices=CATEGORIES)

def categories(request):
    # Layout banners
    info = listingInfo(request)
    no_activeListings, no_inactiveListings, no_userWatchlist = info[0], info[1], info[2]

    if request.method=="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            listings = Listing.objects.filter(category=category)
            return render(request, "auctions/categories.html", {
                "category": category,
                "listings": listings,
                "no_activeListings": no_activeListings,
                "no_inactiveListings": no_inactiveListings,
                "no_userWatchlist": no_userWatchlist,
            })

    else:
        return render(request, "auctions/selectCategories.html", {
            "form": CategoryForm(),
            "no_activeListings": no_activeListings,
            "no_inactiveListings": no_inactiveListings,
            "no_userWatchlist": no_userWatchlist,
        })
