from django.urls import path
from . import frontend_views

urlpatterns = [
    path('', frontend_views.home_view, name='home'),
    path('register/', frontend_views.register_view, name='register'),
    path('login/', frontend_views.login_view, name='login'),
    path('logout/', frontend_views.logout_view, name='logout'),
    path('movies/', frontend_views.movies_list_view, name='movies_list'),
    path('movies/<int:movie_id>/', frontend_views.movie_detail_view, name='movie_detail'),
    path('reviews/', frontend_views.reviews_list_view, name='reviews_list'),
    path('reviews/create/', frontend_views.create_review_view, name='create_review'),
]

