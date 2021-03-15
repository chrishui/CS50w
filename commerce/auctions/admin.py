from django.contrib import admin

from .models import Listing, Bid, Comment, Watchlist

import datetime

# Register your models here.

# Admin interfaces
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "category", "image")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bidPrice")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "comment")

class WatchlistAdmin(admin.ModelAdmin):
    #filter_horizontal = ("listing",)
    list_display = ("id", "user", "listing")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
