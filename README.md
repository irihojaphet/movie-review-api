# 🎬 Movie Review API – ALX Backend Capstone

A production-ready **Movie Review REST API** built with **Django** and **Django REST Framework** as part of the **ALX Backend with Python and Django Capstone Project**.

## ✨ Features

- ✅ **User Authentication**: JWT-based authentication with access and refresh tokens
- ✅ **User Registration**: Public registration endpoint with validation
- ✅ **Movie Management**: CRUD operations for movies (admin-only for write operations)
- ✅ **Review Management**: Full CRUD for reviews with ownership-based permissions
- ✅ **Search & Filtering**: Filter reviews by movie title and rating
- ✅ **Pagination**: Built-in pagination for all list endpoints
- ✅ **Sorting**: Sort reviews by rating, created date, etc.
- ✅ **One Review Per User Per Movie**: Enforced at both database and API level
- ✅ **Error Handling**: Comprehensive error responses with appropriate HTTP status codes
- ✅ **Logging**: Structured logging for debugging and monitoring

---

## 🚀 Project Status

**Status:** ✅ **Production-Ready**

All core features have been implemented and tested:

- ✅ Django project initialized with proper structure
- ✅ Models implemented using Django ORM with constraints and indexes
- ✅ Migrations created and applied
- ✅ Admin interface configured
- ✅ API endpoints fully implemented (CRUD for movies & reviews)
- ✅ Authentication endpoints (register, login, JWT tokens)
- ✅ Search, filtering, pagination, and sorting implemented
- ✅ Custom permissions for review ownership
- ✅ Error handling and logging configured
- ✅ Environment variables setup for deployment
- ✅ Requirements.txt created

---

## 🧱 Tech Stack

- **Language:** Python 3.x
- **Framework:** Django 6.0, Django REST Framework 3.16+
- **Authentication:** JWT (`djangorestframework-simplejwt`)
- **Database:** SQLite (development), PostgreSQL (production-ready)
- **Deployment:** PythonAnywhere / Heroku ready

---

## 📂 Project Structure

```
movie-review-api/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── archive/
│   └── ml-100k/            # MovieLens dataset for seeding
├── movie_review_api/
│   ├── __init__.py
│   ├── settings.py          # Django settings with JWT config
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
└── reviews/
    ├── __init__.py
    ├── admin.py             # Django admin configuration
    ├── apps.py
    ├── models.py            # Movie and Review models
    ├── serializers.py       # DRF serializers
    ├── views.py             # ViewSets for API endpoints
    ├── urls.py              # API URL routing
    ├── permissions.py       # Custom permissions
    ├── exceptions.py        # Custom exception handler
    ├── frontend_views.py    # Frontend template views
    ├── frontend_urls.py     # Frontend URL routing
    ├── management/
    │   └── commands/
    │       └── seed_data.py # Database seeding command
    ├── templates/
    │   └── reviews/         # HTML templates
    ├── static/
    │   └── reviews/
    │       └── css/         # CSS styles
    ├── migrations/
    └── tests.py
```

---

## ⚙️ How to Run Locally

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository:**

```bash
git clone https://github.com/<your-username>/movie-review-api.git
cd movie-review-api
```

2. **Create and activate a virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables (optional):**

Create a `.env` file in the project root (or set environment variables):

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Apply migrations:**

```bash
python manage.py migrate
```

6. **Create a superuser (optional, for Django admin):**

```bash
python manage.py createsuperuser
```

7. **Run the development server:**

```bash
python manage.py runserver
```

The API will be available at:
- **API Base URL:** `http://127.0.0.1:8000/api/`
- **Django Admin:** `http://127.0.0.1:8000/admin/`

---

## 📡 API Documentation

### Base URL

All API endpoints are prefixed with `/api/`

### Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

---

### 🔐 Authentication Endpoints

#### Register a New User

**POST** `/api/auth/register/`

Register a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "date_joined": "2025-01-15T10:30:00Z",
    "reviews_count": 0
  }
}
```

**Errors:**
- `400 Bad Request` - Validation errors (email already exists, passwords don't match, etc.)

---

#### Login (Obtain JWT Tokens)

**POST** `/api/auth/token/`

Obtain access and refresh tokens.

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials

---

#### Refresh Access Token

**POST** `/api/auth/token/refresh/`

Refresh an expired access token using a refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 🎬 Movie Endpoints

#### List All Movies

**GET** `/api/movies/`

Get a paginated list of all movies.

**Query Parameters:**
- `search` - Search by title, genre, or description (e.g., `?search=inception`)
- `ordering` - Sort by `title`, `release_year`, or `created_at` (e.g., `?ordering=-release_year`)
- `page` - Page number for pagination

**Response:** `200 OK`
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/movies/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Inception",
      "description": "A mind-bending thriller...",
      "genre": "Sci-Fi",
      "release_year": 2010,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

**Permissions:** Public (read-only)

---

#### Get Movie Details

**GET** `/api/movies/{id}/`

Get details of a specific movie.

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Inception",
  "description": "A mind-bending thriller...",
  "genre": "Sci-Fi",
  "release_year": 2010,
  "created_at": "2025-01-15T10:00:00Z"
}
```

**Errors:**
- `404 Not Found` - Movie not found

---

#### Create a Movie

**POST** `/api/movies/`

Create a new movie (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "The Matrix",
  "description": "A computer hacker learns about the true nature of reality...",
  "genre": "Sci-Fi",
  "release_year": 1999
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "title": "The Matrix",
  "description": "A computer hacker learns about the true nature of reality...",
  "genre": "Sci-Fi",
  "release_year": 1999,
  "created_at": "2025-01-15T11:00:00Z"
}
```

**Errors:**
- `403 Forbidden` - Not an admin user
- `400 Bad Request` - Validation errors

---

#### Update a Movie

**PUT/PATCH** `/api/movies/{id}/`

Update movie details (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "The Matrix",
  "description": "Updated description...",
  "genre": "Action",
  "release_year": 1999
}
```

**Response:** `200 OK` (same as GET response)

**Errors:**
- `403 Forbidden` - Not an admin user
- `404 Not Found` - Movie not found

---

#### Delete a Movie

**DELETE** `/api/movies/{id}/`

Delete a movie (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

**Errors:**
- `403 Forbidden` - Not an admin user
- `404 Not Found` - Movie not found

---

#### Get Reviews for a Movie

**GET** `/api/movies/{id}/reviews/`

Get all reviews for a specific movie.

**Query Parameters:**
- `rating` - Filter by rating (1-5) (e.g., `?rating=5`)
- `ordering` - Sort by `rating`, `created_at`, or `updated_at` (e.g., `?ordering=-rating`)
- `page` - Page number for pagination

**Response:** `200 OK`
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/movies/1/reviews/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "movie": "Inception (2010)",
      "movie_id": 1,
      "movie_title": "Inception",
      "user": "johndoe",
      "user_id": 1,
      "rating": 5,
      "content": "Amazing movie!",
      "created_at": "2025-01-15T12:00:00Z",
      "updated_at": "2025-01-15T12:00:00Z"
    }
  ]
}
```

**Permissions:** Public

---

### 📝 Review Endpoints

#### List All Reviews

**GET** `/api/reviews/`

Get a paginated list of all reviews.

**Query Parameters:**
- `movie_title` - Filter by movie title (partial match, case-insensitive) (e.g., `?movie_title=inception`)
- `rating` - Filter by rating (1-5) (e.g., `?rating=5`)
- `search` - Search in movie title or review content (e.g., `?search=amazing`)
- `ordering` - Sort by `rating`, `created_at`, or `updated_at` (e.g., `?ordering=-rating`)
- `page` - Page number for pagination

**Response:** `200 OK`
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/reviews/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "movie": "Inception (2010)",
      "movie_id": 1,
      "movie_title": "Inception",
      "user": "johndoe",
      "user_id": 1,
      "rating": 5,
      "content": "Amazing movie with great visuals!",
      "created_at": "2025-01-15T12:00:00Z",
      "updated_at": "2025-01-15T12:00:00Z"
    }
  ]
}
```

**Permissions:** Public

---

#### Get Review Details

**GET** `/api/reviews/{id}/`

Get details of a specific review.

**Response:** `200 OK`
```json
{
  "id": 1,
  "movie": "Inception (2010)",
  "movie_id": 1,
  "movie_title": "Inception",
  "user": "johndoe",
  "user_id": 1,
  "rating": 5,
  "content": "Amazing movie with great visuals!",
  "created_at": "2025-01-15T12:00:00Z",
  "updated_at": "2025-01-15T12:00:00Z"
}
```

**Errors:**
- `404 Not Found` - Review not found

---

#### Create a Review

**POST** `/api/reviews/`

Create a new review (authenticated users only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "movie_id": 1,
  "rating": 5,
  "content": "This is an amazing movie! Highly recommended."
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "movie": "Inception (2010)",
  "movie_id": 1,
  "movie_title": "Inception",
  "user": "johndoe",
  "user_id": 1,
  "rating": 5,
  "content": "This is an amazing movie! Highly recommended.",
  "created_at": "2025-01-15T13:00:00Z",
  "updated_at": "2025-01-15T13:00:00Z"
}
```

**Errors:**
- `401 Unauthorized` - Not authenticated
- `400 Bad Request` - Validation errors (e.g., already reviewed this movie, invalid rating)
- `404 Not Found` - Movie not found

**Note:** Each user can only create one review per movie. Attempting to create a duplicate review will return a `400 Bad Request` error.

---

#### Update a Review

**PUT/PATCH** `/api/reviews/{id}/`

Update your own review (owner only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "movie_id": 1,
  "rating": 4,
  "content": "Updated review content."
}
```

**Response:** `200 OK` (same as GET response)

**Errors:**
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not the owner of this review
- `404 Not Found` - Review not found
- `400 Bad Request` - Validation errors

---

#### Delete a Review

**DELETE** `/api/reviews/{id}/`

Delete your own review (owner only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

**Errors:**
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not the owner of this review
- `404 Not Found` - Review not found

---

## 🗄 Database Models

### Movie Model

Represents a movie that can be reviewed.

**Fields:**
- `id` (Primary Key)
- `title` (CharField, max_length=255, indexed)
- `description` (TextField, optional)
- `genre` (CharField, max_length=100, optional)
- `release_year` (PositiveIntegerField, optional)
- `created_at` (DateTimeField, auto-generated)

**Key Features:**
- Indexed `title` field for efficient search
- Extensible design for future metadata integration

---

### Review Model

Represents a user's review of a movie.

**Fields:**
- `id` (Primary Key)
- `movie` (ForeignKey → Movie)
- `user` (ForeignKey → User)
- `rating` (PositiveSmallIntegerField, 1-5, validated)
- `content` (TextField)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-updated)

**Constraints:**
- `unique_together = ("movie", "user")` - One review per user per movie (enforced at DB level)
- Indexes on `movie`, `user`, and `rating` for query performance
- Rating validation (1-5) at model and serializer level

---

## 🔒 Permissions & Security

### Permission Classes

- **Public Read Access**: Anyone can view movies and reviews
- **Authenticated Write**: Only authenticated users can create reviews
- **Owner-Only Edit/Delete**: Users can only modify their own reviews
- **Admin-Only Movie Management**: Only staff users can create/update/delete movies

### Authentication

- JWT tokens with 1-hour access token lifetime
- 7-day refresh token lifetime
- Token rotation enabled
- Bearer token authentication

---

## 🚀 Deployment

### Environment Variables

Set the following environment variables in your production environment:

```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_LOG_LEVEL=INFO
```

### PythonAnywhere

1. Upload your project files
2. Set up a virtual environment and install dependencies
3. Configure environment variables in the web app settings
4. Set up static files: `python manage.py collectstatic`
5. Configure WSGI file to point to your Django app

### Heroku

1. Create a `Procfile`:
```
web: gunicorn movie_review_api.wsgi --log-file -
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

3. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

---

## ✅ Capstone Requirements Checklist

- [x] Public GitHub repository set up
- [x] README with project overview and setup instructions
- [x] Use Django ORM for all database interactions
- [x] Define models for Reviews and Users (using Django auth system)
- [x] Database supports multiple reviews per movie from different users
- [x] CRUD for users and reviews via API endpoints
- [x] View reviews for a specific movie
- [x] Search/filter reviews by movie title and rating
- [x] Authentication (login required for create/update/delete)
- [x] Permissions (users can only modify their own reviews)
- [x] Pagination and sorting for review listings
- [x] Error handling with appropriate HTTP status codes and responses
- [x] Logging and basic monitoring
- [ ] Deployment to a live environment (ready for deployment)

---

## 🧪 Testing

### Manual Testing Examples

#### 1. Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password_confirm":"testpass123"}'
```

#### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

#### 3. Create a Review (with token)
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"movie_id":1,"rating":5,"content":"Great movie!"}'
```

#### 4. Filter Reviews by Rating
```bash
curl http://127.0.0.1:8000/api/reviews/?rating=5
```

#### 5. Search Reviews by Movie Title
```bash
curl http://127.0.0.1:8000/api/reviews/?movie_title=inception
```

---

## 📝 Code Quality

- **DRY Principles**: Reusable serializers and permissions
- **Clean Architecture**: Separated concerns (models, views, serializers, permissions)
- **Error Handling**: Custom exception handler for consistent error responses
- **Logging**: Structured logging for debugging and monitoring
- **Type Safety**: Proper use of Django ORM and DRF types
- **Documentation**: Comprehensive docstrings and README

---

## 🤝 Contributing

This project is primarily for learning and assessment as part of the ALX Backend Capstone. However, suggestions and improvements are welcome via issues or pull requests.

---

## 📄 License

This project is created for educational purposes as part of the **ALX Backend Engineering Capstone Project**.

You are free to fork and adapt it for learning, but please avoid submitting it as your own work in any formal academic or training context.

---

## 👨‍💻 Author

Built as part of the ALX Backend with Python & Django Capstone Project.

---

**Last Updated:** January 2025
