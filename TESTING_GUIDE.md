# Testing Guide for Movie Review API

This guide will help you test the application for your presentation video.

## Quick Start

1. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

2. **Run migrations (if needed):**
   ```bash
   python manage.py migrate
   ```

3. **Seed the database with demo data (RECOMMENDED for presentations):**
   ```bash
   python manage.py seed_data --demo
   ```
   This will create 100 movies, 20 users, and ~500 reviews from the MovieLens dataset.
   
   **Alternative:** For full dataset (1682 movies, 100k reviews):
   ```bash
   python manage.py seed_data
   ```
   See `SEEDING_GUIDE.md` for more options.

4. **Create a superuser (for admin access - optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Open in browser:**
   - Frontend: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`
   - API: `http://127.0.0.1:8000/api/`

## Testing Flow for Presentation

### 1. Home Page
- ✅ Navigate to `http://127.0.0.1:8000/`
- ✅ See the welcome page with features listed
- ✅ Notice "Register" and "Login" buttons

### 2. User Registration
- ✅ Click "Register" or go to `/register/`
- ✅ Fill in:
  - Username: `testuser`
  - Email: `test@example.com`
  - Password: `testpass123`
  - Confirm Password: `testpass123`
- ✅ Submit and see success message
- ✅ Should redirect to login page

### 3. User Login
- ✅ Go to `/login/`
- ✅ Enter credentials (use a seeded user if you ran seed_data):
  - Username: `user_1` (for seeded users) or `testuser` (if you registered)
  - Password: `demo123` (for seeded users) or `testpass123` (if you registered)
- ✅ Submit and see success message
- ✅ Should redirect to home page
- ✅ Notice navigation now shows "Logged in" and "Logout"

### 4. Browse Seeded Movies
- ✅ If you ran `seed_data`, you should already have movies!
- ✅ Go to `/movies/` to see the seeded movies
- ✅ You can also create additional movies via Admin:
  - Go to `/admin/`
  - Login with superuser credentials
  - Click "Movies" → "Add Movie"
  - Create custom movies if needed

### 5. Browse Movies
- ✅ Go to `/movies/`
- ✅ See list of movies you created
- ✅ Try searching: Type "Inception" in search box
- ✅ Click "View Details" on a movie

### 6. View Movie Details
- ✅ On movie detail page, see:
  - Movie title, genre, year, description
  - Reviews section (empty initially)
- ✅ Notice "Write a Review" form is visible (since you're logged in)

### 7. Create a Review
- ✅ On movie detail page, fill in review form:
  - Rating: 5 (use the number input or stars)
  - Content: "This is an amazing movie! Highly recommended."
- ✅ Submit review
- ✅ See success message
- ✅ Review appears in the reviews list
- ✅ Try filtering by rating (select "5 Stars" from dropdown)

### 8. Create Another Review
- ✅ Go to `/reviews/create/`
- ✅ Select a movie from dropdown
- ✅ Enter rating and content
- ✅ Submit
- ✅ Should redirect to movie detail page

### 9. View All Reviews
- ✅ Go to `/reviews/`
- ✅ See all reviews
- ✅ Try filtering:
  - Filter by movie title: Type "Inception"
  - Filter by rating: Select "5 Stars"
- ✅ Try both filters together

### 10. Test Pagination
- ✅ If you have more than 10 reviews, see pagination controls
- ✅ Click "Next" and "Previous" buttons

### 11. Test Search
- ✅ On movies page, search for "Matrix"
- ✅ On reviews page, search for "amazing"

### 12. Test Authentication
- ✅ Click "Logout" in navigation
- ✅ Try to create a review (should prompt to login)
- ✅ Go to `/reviews/create/` (should work, but API will reject)
- ✅ Login again with a seeded user:
  - Username: `user_1` (or any `user_N` up to the number you seeded)
  - Password: `demo123`

### 13. Test One Review Per User Per Movie
- ✅ Try to create another review for the same movie you already reviewed
- ✅ Should see error: "You have already reviewed this movie"

## Key Features to Highlight in Video

1. **User Registration & Authentication**
   - Show registration form
   - Show login
   - Show JWT token stored in browser

2. **Movie Management**
   - Browse movies
   - Search movies
   - View movie details

3. **Review Management**
   - Create reviews (authenticated)
   - View all reviews
   - Filter by movie title
   - Filter by rating
   - View reviews for specific movie

4. **API Features**
   - Show that frontend uses REST API
   - Mention pagination
   - Mention search and filtering
   - Mention authentication required for creating reviews

## Common Issues & Solutions

### Issue: Static files not loading
**Solution:** Make sure `STATIC_URL` and `STATICFILES_DIRS` are configured correctly in settings.py

### Issue: API calls failing
**Solution:** 
- Check browser console for errors
- Make sure server is running
- Check that API endpoints are accessible at `/api/`

### Issue: Can't create reviews
**Solution:**
- Make sure you're logged in (check localStorage for authToken)
- Check browser console for API errors
- Verify token is being sent in Authorization header

### Issue: Movies not showing
**Solution:**
- Create movies via admin panel first
- Check browser console for API errors

## Tips for Presentation Video

1. **Start with Home Page** - Show the clean UI
2. **Register a User** - Show the registration flow
3. **Login** - Show authentication working
4. **Browse Movies** - Show the movie list and search
5. **View Movie Details** - Show movie info and reviews
6. **Create a Review** - Show the review creation form
7. **Filter Reviews** - Show filtering by rating and movie title
8. **Show API in Action** - Open browser DevTools → Network tab to show API calls
9. **Mention Key Features** - JWT auth, filtering, pagination, one review per user per movie

## Browser DevTools Tips

To show API calls in your video:
1. Open DevTools (F12)
2. Go to Network tab
3. Filter by "Fetch/XHR"
4. Create a review or browse movies
5. Click on API calls to show request/response

This demonstrates that your frontend is using the REST API!

---

**Good luck with your presentation! 🎬**

