"""
Django management command to seed the database with MovieLens 100k dataset.

Usage:
    python manage.py seed_data [--movies-only] [--reviews-only] [--limit N]
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from reviews.models import Movie, Review
from datetime import datetime
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with MovieLens 100k dataset'

    def add_arguments(self, parser):
        parser.add_argument(
            '--movies-only',
            action='store_true',
            help='Only seed movies, skip users and reviews',
        )
        parser.add_argument(
            '--reviews-only',
            action='store_true',
            help='Only seed reviews (assumes movies and users exist)',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit the number of movies/reviews to seed (for testing)',
        )
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of users to create (default: 50)',
        )
        parser.add_argument(
            '--demo',
            action='store_true',
            help='Demo mode: seed 100 movies and 500 reviews (quick for presentations)',
        )

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        archive_dir = os.path.join(base_dir, 'archive', 'ml-100k')
        
        if not os.path.exists(archive_dir):
            self.stdout.write(self.style.ERROR(f'Archive directory not found: {archive_dir}'))
            return

        movies_only = options['movies_only']
        reviews_only = options['reviews_only']
        limit = options.get('limit')
        num_users = options.get('users', 50)
        demo_mode = options.get('demo', False)

        # Demo mode: quick seed for presentations
        if demo_mode:
            limit = 100  # 100 movies
            num_users = 20  # 20 users
            self.stdout.write(self.style.SUCCESS('🎬 Starting DEMO mode seeding (100 movies, 20 users, ~500 reviews)...'))
        else:
            self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        if not reviews_only:
            # Seed movies
            self.seed_movies(archive_dir, limit)
        
        if not movies_only and not reviews_only:
            # Seed users
            self.seed_users(archive_dir, num_users)
        
        if not movies_only:
            # Seed reviews (limit reviews in demo mode)
            review_limit = 500 if demo_mode else limit
            self.seed_reviews(archive_dir, review_limit)

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding completed!'))

    def seed_movies(self, archive_dir, limit=None):
        """Seed movies from u.item file."""
        self.stdout.write('\n📽️  Seeding movies...')
        
        movies_file = os.path.join(archive_dir, 'u.item')
        if not os.path.exists(movies_file):
            self.stdout.write(self.style.ERROR(f'Movies file not found: {movies_file}'))
            return

        genre_file = os.path.join(archive_dir, 'u.genre')
        genres = []
        if os.path.exists(genre_file):
            with open(genre_file, 'r', encoding='latin-1') as f:
                for line in f:
                    if line.strip():
                        genre_name = line.split('|')[0].strip()
                        genres.append(genre_name)

        movies_created = 0
        movies_updated = 0
        
        with open(movies_file, 'r', encoding='latin-1') as f:
            for idx, line in enumerate(f):
                if limit and idx >= limit:
                    break
                
                if not line.strip():
                    continue
                
                parts = line.strip().split('|')
                if len(parts) < 2:
                    continue
                
                try:
                    movie_id = int(parts[0])
                    title = parts[1].strip()
                    
                    # Parse release date
                    release_date_str = parts[2].strip() if len(parts) > 2 else ''
                    release_year = None
                    if release_date_str:
                        try:
                            # Format: 01-Jan-1995
                            date_obj = datetime.strptime(release_date_str, '%d-%b-%Y')
                            release_year = date_obj.year
                        except:
                            # Try to extract year from string
                            import re
                            year_match = re.search(r'\d{4}', release_date_str)
                            if year_match:
                                release_year = int(year_match.group())
                    
                    # Parse genres (last 19 fields)
                    movie_genres = []
                    if len(parts) >= 6:
                        genre_flags = parts[5:24]  # 19 genre flags
                        for i, flag in enumerate(genre_flags):
                            if flag == '1' and i < len(genres):
                                movie_genres.append(genres[i])
                    
                    # Get description (could be empty, use title as fallback)
                    description = f"A {', '.join(movie_genres) if movie_genres else 'movie'} from {release_year if release_year else 'unknown year'}."
                    
                    # Create or update movie (by title to avoid ID conflicts)
                    movie, created = Movie.objects.get_or_create(
                        title=title,
                        defaults={
                            'genre': ', '.join(movie_genres[:3]) if movie_genres else '',  # Limit to 3 genres
                            'release_year': release_year,
                            'description': description,
                        }
                    )
                    
                    # Update if exists but missing data
                    if not created:
                        if not movie.genre and movie_genres:
                            movie.genre = ', '.join(movie_genres[:3])
                        if not movie.release_year and release_year:
                            movie.release_year = release_year
                        if not movie.description:
                            movie.description = description
                        movie.save()
                    
                    if created:
                        movies_created += 1
                    else:
                        movies_updated += 1
                    
                    if (movies_created + movies_updated) % 100 == 0:
                        self.stdout.write(f'  Processed {movies_created + movies_updated} movies...')
                
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Error processing movie line {idx + 1}: {e}'))
                    continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Movies: {movies_created} created, {movies_updated} updated'
            )
        )

    def seed_users(self, archive_dir, num_users=50):
        """Seed users from u.user file."""
        self.stdout.write(f'\n👥 Seeding {num_users} users...')
        
        users_file = os.path.join(archive_dir, 'u.user')
        if not os.path.exists(users_file):
            self.stdout.write(self.style.ERROR(f'Users file not found: {users_file}'))
            return

        users_created = 0
        user_data = []
        
        with open(users_file, 'r', encoding='latin-1') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    user_data.append({
                        'age': int(parts[1]) if parts[1].isdigit() else 25,
                        'gender': parts[2],
                        'occupation': parts[3] if len(parts) > 3 else 'other',
                    })
        
        # Limit to num_users
        user_data = user_data[:num_users]
        
        with transaction.atomic():
            for idx, user_info in enumerate(user_data):
                try:
                    username = f"user_{idx + 1}"
                    email = f"user{idx + 1}@example.com"
                    
                    # Check if user already exists
                    if User.objects.filter(username=username).exists():
                        continue
                    
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='demo123',  # Simple password for demo
                    )
                    users_created += 1
                    
                    if users_created % 10 == 0:
                        self.stdout.write(f'  Created {users_created} users...')
                
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Error creating user {idx + 1}: {e}'))
                    continue
        
        self.stdout.write(self.style.SUCCESS(f'✅ Users: {users_created} created'))

    def seed_reviews(self, archive_dir, limit=None):
        """Seed reviews from u.data file."""
        self.stdout.write('\n⭐ Seeding reviews...')
        
        reviews_file = os.path.join(archive_dir, 'u.data')
        if not os.path.exists(reviews_file):
            self.stdout.write(self.style.ERROR(f'Reviews file not found: {reviews_file}'))
            return

        # Get all movies and users
        movies_list = list(Movie.objects.all())
        users = list(User.objects.all())
        
        if not movies_list:
            self.stdout.write(self.style.ERROR('No movies found. Please seed movies first.'))
            return
        
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please seed users first.'))
            return

        reviews_created = 0
        reviews_skipped = 0
        
        # Create a mapping from MovieLens movie IDs to our Movie objects
        # We'll read the u.item file to map ML IDs to titles, then find our movies
        ml_movie_map = {}
        movies_file = os.path.join(archive_dir, 'u.item')
        if os.path.exists(movies_file):
            with open(movies_file, 'r', encoding='latin-1') as f:
                for line in f:
                    if not line.strip():
                        continue
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        try:
                            ml_id = int(parts[0])
                            title = parts[1].strip()
                            # Find matching movie in our database
                            for movie in movies_list:
                                if movie.title == title:
                                    ml_movie_map[ml_id] = movie
                                    break
                        except:
                            continue
        
        # Create a mapping from MovieLens user IDs to our User objects
        user_mapping = {}
        for idx, user in enumerate(users):
            # Map MovieLens user IDs (1-based) to our users using modulo
            ml_user_id = (idx % len(users)) + 1
            if ml_user_id not in user_mapping:
                user_mapping[ml_user_id] = user
        
        # Sample review content templates
        review_templates = [
            "Great movie! Highly recommended.",
            "One of my favorites. Excellent storytelling.",
            "Really enjoyed this one. Worth watching.",
            "Good movie, but could be better.",
            "Not my cup of tea, but well made.",
            "Amazing cinematography and acting.",
            "Solid film with good performances.",
            "Entertaining and engaging throughout.",
            "Decent movie, nothing special.",
            "Could have been better, but still enjoyable.",
        ]
        
        with transaction.atomic():
            with open(reviews_file, 'r', encoding='latin-1') as f:
                for idx, line in enumerate(f):
                    if limit and reviews_created >= limit:
                        break
                    
                    if not line.strip():
                        continue
                    
                    parts = line.strip().split()
                    if len(parts) < 3:
                        continue
                    
                    try:
                        ml_user_id = int(parts[0])
                        ml_movie_id = int(parts[1])
                        rating = int(parts[2])
                        
                        # Validate rating
                        if rating < 1 or rating > 5:
                            continue
                        
                        # Get movie and user using mappings
                        movie = ml_movie_map.get(ml_movie_id)
                        user = user_mapping.get(ml_user_id)
                        
                        if not movie or not user:
                            reviews_skipped += 1
                            continue
                        
                        # Check if review already exists
                        if Review.objects.filter(movie=movie, user=user).exists():
                            reviews_skipped += 1
                            continue
                        
                        # Create review with sample content
                        review_content = random.choice(review_templates)
                        if rating >= 4:
                            review_content = f"⭐ {review_content}"
                        elif rating <= 2:
                            review_content = f"⚠️ {review_content}"
                        
                        Review.objects.create(
                            movie=movie,
                            user=user,
                            rating=rating,
                            content=review_content,
                        )
                        
                        reviews_created += 1
                        
                        if reviews_created % 500 == 0:
                            self.stdout.write(f'  Created {reviews_created} reviews...')
                    
                    except Exception as e:
                        reviews_skipped += 1
                        continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Reviews: {reviews_created} created, {reviews_skipped} skipped'
            )
        )

