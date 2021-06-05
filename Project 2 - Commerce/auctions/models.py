from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
  CATEGORIES = [
    ("fashion", "Fashion"),
    ("toys", "Toys"),
    ("electronics", "Electronics"),
    ("home", "Home")
  ]

  title = models.CharField(max_length=64)
  description = models.CharField(max_length=256)
  bid = models.IntegerField()
  image_url = models.CharField(max_length=128, blank=True)
  category = models.CharField(
    max_length=15,
    choices=CATEGORIES,
    default="home"
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")

class Bid(models.Model):
  pass

class Comment(models.Model):
  pass

class Watchlist(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
  item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)