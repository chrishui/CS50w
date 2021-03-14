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

# Auction listing
class Listing(TimeStampMixin):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.IntegerField()
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}, {self.name}: ${self.price}. Description: {self.description}."

# Bids
class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidPrice = models.IntegerField()

    def __str__(self):
        return f"Bid price: ${self.bidPrice}"

# Comments
class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"Comment: {self.comment}"
