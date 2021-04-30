from django.contrib import admin

from .models import Post, Profile

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "created_at")
    list_editable = ("user", "content")

class ProfileAdmin(admin.ModelAdmin):
    #filter_horizontal = ('post',)
    list_display = ('id','user')


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
