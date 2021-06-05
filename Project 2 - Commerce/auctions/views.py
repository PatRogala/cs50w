from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import AuctionListing, User, Watchlist


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
    "listings": listings })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def create_listing(request):
  if request.method == "POST":
    form = request.POST
    user = User.objects.get(username=request.user)
    listing = AuctionListing(
      title=form['title'],
      description=form['description'],
      bid=form['starting_bid'],
      image_url=form['image'],
      category=form['category'],
      user=user
    )
    if not listing.save():
      return HttpResponseRedirect(reverse("create_listing"))
    return HttpResponseRedirect(reverse("index"))
  else:
    return render(request, "auctions/createlisting.html")

def listing(request, id):
  listing = AuctionListing.objects.get(id=id)
  return render(request, "auctions/listing.html", {
    "listing": listing,
    'user': request.user,
    "status": listing.id in request.user.watchlist.all().values_list('item_id', flat=True),
  })

def watchlist_add(request):
  item = AuctionListing.objects.get(id=request.GET['watchlist_item'])
  user = User.objects.get(username=request.GET['user'])
  if not Watchlist.objects.filter(user=user, item=item):
    i = Watchlist(user=user, item=item)
    i.save()
  else:
    Watchlist.objects.filter(user=user, item=item).all().delete()
  print(Watchlist.objects.all())
  return HttpResponseRedirect(reverse('listing', kwargs={'id': item.id}))

def bid(request, item):
  pass