from django.contrib import admin

from .models import Post, Profile, Like

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "created_at")
    list_editable = ("user", "content")

class ProfileAdmin(admin.ModelAdmin):
    #filter_horizontal = ('post',)
    list_display = ('id','user')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Like, LikeAdmin)
