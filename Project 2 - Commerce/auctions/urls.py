from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create_listing"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist_add, name="watchlist_add"),
    path("bid/<str:item>", views.bid, name="bid")
]
