from django.contrib import admin

from .models import Listing, Bid, Comment

import datetime

# Register your models here.

# Admin interfaces
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "category")

class BidAdmin(admin.ModelAdmin):
    filter_horizontal = ("item",)

class CommentAdmin(admin.ModelAdmin):
    filter_horizontal = ("item",)

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
