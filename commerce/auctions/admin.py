from django.contrib import admin

from .models import Listing, Bid, Comment

import datetime

# Register your models here.

# Admin interfaces
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "category", "image")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "bidPrice")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "comment")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
