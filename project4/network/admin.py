from django.contrib import admin

from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content")
    list_editable = ("user", "content")

admin.site.register(Post, PostAdmin)
