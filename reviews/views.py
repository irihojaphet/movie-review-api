import logging
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.db.models import Q

from .models import Movie, Review
from .serializers import (
    MovieSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
    UserSerializer,
    UserDetailSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Movie instances.
    
    - GET /api/movies/ - List all movies (public)
    - POST /api/movies/ - Create a movie (admin only)
    - GET /api/movies/{id}/ - Retrieve a movie (public)
    - PUT/PATCH /api/movies/{id}/ - Update a movie (admin only)
    - DELETE /api/movies/{id}/ - Delete a movie (admin only)
    - GET /api/movies/{id}/reviews/ - Get reviews for a specific movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genre', 'description']
    ordering_fields = ['title', 'release_year', 'created_at']
    ordering = ['title']
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def reviews(self, request, pk=None):
        """
        Get all reviews for a specific movie.
        Supports filtering by rating and sorting.
        """
        movie = self.get_object()
        reviews = Review.objects.filter(movie=movie)
        
        # Filter by rating if provided
        rating = request.query_params.get('rating', None)
        if rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    reviews = reviews.filter(rating=rating)
                else:
                    return Response(
                        {"error": "Rating must be between 1 and 5."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {"error": "Rating must be a valid integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Sorting
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering.lstrip('-') in ['rating', 'created_at', 'updated_at']:
            reviews = reviews.order_by(ordering)
        else:
            reviews = reviews.order_by('-created_at')
        
        # Pagination
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Review instances.
    
    - GET /api/reviews/ - List all reviews (public, with filtering)
    - POST /api/reviews/ - Create a review (authenticated users only)
    - GET /api/reviews/{id}/ - Retrieve a review (public)
    - PUT/PATCH /api/reviews/{id}/ - Update a review (owner only)
    - DELETE /api/reviews/{id}/ - Delete a review (owner only)
    """
    queryset = Review.objects.select_related('movie', 'user').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['movie__title', 'content']
    ordering_fields = ['rating', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializer for create action."""
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_queryset(self):
        """
        Optionally filter reviews by movie title or rating via query parameters.
        """
        queryset = Review.objects.select_related('movie', 'user').all()
        
        # Filter by movie title (case-insensitive partial match)
        movie_title = self.request.query_params.get('movie_title', None)
        if movie_title:
            queryset = queryset.filter(movie__title__icontains=movie_title)
        
        # Filter by rating
        rating = self.request.query_params.get('rating', None)
        if rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    queryset = queryset.filter(rating=rating)
            except ValueError:
                pass  # Ignore invalid rating values
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the user to the current authenticated user."""
        serializer.save(user=self.request.user)
        logger.info(f"Review created by user {self.request.user.username}")


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for user profile viewing.
    
    - GET /api/users/{id}/ - Get user profile (authenticated)
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


# Separate view for registration to ensure AllowAny permission
class RegisterView(APIView):
    """
    User registration endpoint.
    POST /api/auth/register/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"New user registered: {user.username}")
            return Response(
                {
                    "message": "User registered successfully.",
                    "user": UserDetailSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
