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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    image = models.URLField()

    def __str__(self):
        return f"{self.id}, {self.name}: ${self.price}."

# Bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidPrice = models.IntegerField()
    bidCount = models.IntegerField()

    def __str__(self):
        return f"Bid price: ${self.bidPrice}"

# Comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"Comment: {self.comment}"

# Watchlist
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.listing}"
