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
    #liked_count = models.IntegerField()

    def __str__(self):
        return f"{self.id}, {self.user}: ${self.content}."

# Profile
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, blank=True, related_name="following")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")

    def __str__(self):
        return f"{self.user}'s following / followers"

# Like / Unlike
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")

    def __str__(self):
        return f"{self.post}"
