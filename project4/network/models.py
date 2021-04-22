from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass

# Time stamp
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Post
class Post(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.id}, {self.user}: ${self.content}."

# Profile
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, blank=True)
    following = models.ManyToManyField(User, blank=True, related_name="following")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")

    # post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE, related_name="user_posts")
    # following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="following")
    # followers = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="followers")

    #post = models.ManyToManyField(Post, blank=True, related_name="user_posts")

    def __str__(self):
        return f"{self.user}'s profile"
