from django.contrib.auth.models import AbstractUser
from django.db import models


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

class Bid(models.Model):
  pass

class Comment(models.Model):
  pass