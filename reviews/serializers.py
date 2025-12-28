from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Movie, Review

User = get_user_model()


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model."""
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'genre', 'release_year', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    movie = serializers.StringRelatedField(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True
    )
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'movie', 'movie_id', 'movie_title',
            'user', 'user_id', 'rating', 'content',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'user_id', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        """Ensure rating is between 1 and 5."""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate(self, attrs):
        """Validate that user can only create one review per movie."""
        movie = attrs.get('movie')
        user = self.context['request'].user
        
        # Only check for duplicates on create (not update)
        if self.instance is None and movie and user.is_authenticated:
            if Review.objects.filter(movie=movie, user=user).exists():
                raise serializers.ValidationError(
                    {"movie": "You have already reviewed this movie."}
                )
        
        return attrs


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating reviews (accepts movie_id)."""
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True
    )
    
    class Meta:
        model = Review
        fields = ['movie_id', 'rating', 'content']
    
    def validate_rating(self, value):
        """Ensure rating is between 1 and 5."""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (registration)."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, attrs):
        """Ensure passwords match."""
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        
        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password."""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for User detail view (read-only, no password)."""
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'reviews_count']
        read_only_fields = ['id', 'username', 'email', 'date_joined', 'reviews_count']
    
    def get_reviews_count(self, obj):
        """Return the number of reviews by this user."""
        return obj.reviews.count()

