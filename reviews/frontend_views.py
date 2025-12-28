"""
Frontend views for rendering HTML templates that interact with the REST API.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods


def home_view(request):
    """Home page with overview."""
    return render(request, 'reviews/home.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration page."""
    return render(request, 'reviews/register.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login page."""
    return render(request, 'reviews/login.html')


def logout_view(request):
    """Logout user (clear session, token handled by JS)."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def movies_list_view(request):
    """List all movies."""
    return render(request, 'reviews/movies_list.html')


def movie_detail_view(request, movie_id):
    """Movie detail page with reviews."""
    return render(request, 'reviews/movie_detail.html', {'movie_id': movie_id})


def reviews_list_view(request):
    """List all reviews with filtering."""
    return render(request, 'reviews/reviews_list.html')


def create_review_view(request):
    """Create a new review."""
    return render(request, 'reviews/create_review.html')

