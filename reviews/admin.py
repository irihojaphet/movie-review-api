from django.contrib import admin
from .models import Movie, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "genre", "release_year", "created_at")
    search_fields = ("title", "genre")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("movie__title", "user__username")
