from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scraping", views.reddit_scraper, name="scraping"),
    path("forumlibre", views.fl_redirect, name="forumlibre"),
]
