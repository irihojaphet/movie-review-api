# Database Seeding Guide

This guide explains how to seed your database with the MovieLens 100k dataset for a more interactive demo.

## Quick Start (Demo Mode)

For a quick demo with a reasonable amount of data:

```bash
python manage.py seed_data --demo
```

This will seed:
- 100 movies
- 20 users
- ~500 reviews

Perfect for presentations!

## Full Dataset Seeding

To seed the complete dataset (1682 movies, 100k reviews):

```bash
python manage.py seed_data
```

This will seed:
- All 1682 movies from the dataset
- 50 users (configurable)
- All reviews from the dataset (up to 100,000)

## Options

### Seed Only Movies

```bash
python manage.py seed_data --movies-only
```

### Seed Only Reviews (assumes movies and users exist)

```bash
python manage.py seed_data --reviews-only
```

### Limit Number of Items

```bash
# Seed only 50 movies
python manage.py seed_data --limit 50

# Seed 200 movies and 1000 reviews
python manage.py seed_data --limit 200
```

### Custom Number of Users

```bash
# Create 100 users instead of default 50
python manage.py seed_data --users 100
```

## Examples

### For Presentation/Demo

```bash
# Quick demo with manageable data
python manage.py seed_data --demo
```

### For Full Testing

```bash
# Full dataset
python manage.py seed_data

# Or with more users
python manage.py seed_data --users 100
```

### Incremental Seeding

```bash
# First, seed movies
python manage.py seed_data --movies-only

# Then, seed users
python manage.py seed_data --users-only  # (if you add this option)

# Finally, seed reviews
python manage.py seed_data --reviews-only
```

## What Gets Seeded

### Movies
- Title (from MovieLens dataset)
- Genre (parsed from genre flags)
- Release Year (parsed from release date)
- Description (auto-generated based on genre and year)

### Users
- Username: `user_1`, `user_2`, etc.
- Email: `user1@example.com`, `user2@example.com`, etc.
- Password: `demo123` (same for all demo users)

### Reviews
- Rating (1-5 stars from dataset)
- Content (auto-generated review text)
- Linked to movies and users from dataset

## After Seeding

1. **Test Login**: You can login with any seeded user:
   - Username: `user_1`, `user_2`, etc.
   - Password: `demo123`

2. **Browse Movies**: Go to `/movies/` to see all seeded movies

3. **View Reviews**: Go to `/reviews/` to see all reviews

4. **Filter & Search**: Test the filtering and search features with real data

## Troubleshooting

### Archive folder not found
Make sure the `archive/ml-100k/` folder exists in your project root.

### Encoding errors
The script uses `latin-1` encoding to handle the MovieLens dataset. If you encounter encoding issues, check the file encoding.

### Memory issues with full dataset
If seeding the full dataset causes memory issues, use `--limit` to seed in batches:

```bash
python manage.py seed_data --limit 500
```

### Duplicate reviews
The script checks for existing reviews to avoid duplicates. If you want to re-seed, you may need to clear existing data first.

## Clearing Data (Optional)

If you want to start fresh:

```python
# In Django shell: python manage.py shell
from reviews.models import Movie, Review
from django.contrib.auth import get_user_model

User = get_user_model()

# Delete all reviews
Review.objects.all().delete()

# Delete all movies (optional)
# Movie.objects.all().delete()

# Delete demo users (optional, be careful!)
# User.objects.filter(username__startswith='user_').delete()
```

---

**Happy Seeding! 🎬**

