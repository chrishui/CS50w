from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # <str:str> passed to views.py to enable checking of valid entry
    path('wiki/<str:title>', views.entry, name="entry"),
    # Search
    path("search", views.search, name="searchRef"),
    # Create new page
    path("newPage", views.newPage, name="newPageRef"),
    # Edit page
    path("editPage/<str:title>", views.editPage, name="editRef"),
    # Random page
    path("randomPage", views.randomPage, name="randomPageRef"),
]
