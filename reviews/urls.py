from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MovieViewSet, ReviewViewSet, UserViewSet, RegisterView

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # JWT Token endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User registration
    path('auth/register/', RegisterView.as_view(), name='user_register'),
    
    # Include router URLs
    path('', include(router.urls)),
]

