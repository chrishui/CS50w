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
