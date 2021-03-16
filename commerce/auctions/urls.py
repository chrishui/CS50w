from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.createListing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/<int:listing_id>", views.watchlist, name='watchlist'),
    path("user_watchlist", views.userWatchlist, name='userWatchlist'),
    path("placebid/<int:listing_id>", views.bid, name='placebid'),
    path("comments/<int:listing_id>", views.comments, name='comments')

]