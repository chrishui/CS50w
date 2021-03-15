from django.contrib import admin

from .models import Listing, Bid, Comment, Watchlist

import datetime

# Register your models here.

# Admin interfaces
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "description", "price", "category", "image")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "bidPrice", "bidCount")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "comment")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
