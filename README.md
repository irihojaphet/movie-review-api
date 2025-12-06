
# 🎬 Movie Review API – ALX Backend Capstone

This is a **Movie Review REST API** built with **Django** and **Django REST Framework** as part of the **ALX Backend with Python and Django Capstone Project**.

The API will allow users to:
- Create accounts and authenticate
- Create, read, update, and delete movie reviews
- View reviews for specific movies
- Search and filter reviews by movie title and rating
- (Later) Add pagination, sorting, and optional advanced features like likes and recommendations

---

## 🚀 Project Status (Part 3 – Start Building)

**Current progress:**

- ✅ Public GitHub repository created  
- ✅ Django project initialized: `movie_review_api`  
- ✅ Main app created: `reviews`  
- ✅ Django REST Framework and JWT package installed  
- ✅ Models implemented using Django ORM:
  - `Movie` model
  - `Review` model (linked to `User` and `Movie`, with rating validation)
- ✅ Migrations created and applied
- ✅ Admin configured for `Movie` and `Review`
- ⏳ API endpoints (CRUD for reviews & movies) – in progress  
- ⏳ Authentication endpoints (register, login, JWT) – planned  
- ⏳ Search, filtering, pagination – planned  

This repository is part of the **ALX BE Capstone Part 3 – Start Building** milestone.

---

## 🧱 Tech Stack

- **Language:** Python 3.x  
- **Framework:** Django, Django REST Framework  
- **Auth:** Django authentication + JWT (`djangorestframework-simplejwt`)  
- **Database:** SQLite (development), later PostgreSQL (production)  
- **Deployment target:** PythonAnywhere / Heroku  

---

## 📂 Project Structure


movie-review-api/
├─ manage.py
├─ README.md
├─ requirements.txt
├─ movie_review_api/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
└─ reviews/
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ migrations/
   ├─ models.py
   ├─ tests.py
   └─ views.py



## 🗄 Models (Django ORM)

### Movie

The `Movie` model represents a movie that can be reviewed.

Fields:

* `title` (string, indexed)
* `description` (text, optional)
* `genre` (string, optional)
* `release_year` (integer, optional)
* `created_at` (DateTime, auto timestamp)

Key points:

* Indexed `title` to support search by movie title.
* Designed to be extendable with more metadata later (e.g., external APIs like OMDB/TMDB).

### Review

The `Review` model represents a user’s review of a movie.

Fields:

* `movie` (ForeignKey → `Movie`, many reviews per movie)
* `user` (ForeignKey → Django’s built-in `auth.User`)
* `rating` (integer, 1–5, validated)
* `content` (text – the review content)
* `created_at` (DateTime, auto timestamp)
* `updated_at` (DateTime, auto timestamp)

Constraints and indexes:

* `unique_together = ("movie", "user")` → one review per user per movie.
* Indexes on `movie`, `user`, and `rating` for better query performance.
* Rating field is validated to ensure values are between 1 and 5.

This design satisfies the capstone requirements to:

* Allow multiple users to review the same movie.
* Store rating and review content with validation.
* Use Django ORM for database interactions.

---

## ⚙️ How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/movie-review-api.git
cd movie-review-api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/macOS:
# source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser (optional, for Django admin):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

Then open:

* Django Admin: `http://127.0.0.1:8000/admin/`

---

## 📡 Planned API Endpoints (High-Level Design)

> These endpoints are planned as part of the capstone and will be implemented progressively.

### Authentication

* `POST /api/auth/register/`
  Register a new user account.

* `POST /api/auth/login/`
  Obtain JWT access and refresh tokens.

### Movies

* `GET /api/movies/`
  List all movies, with optional filters/search by title.

* `POST /api/movies/`
  Create a new movie (admin only).

* `GET /api/movies/<id>/`
  Retrieve details of a single movie.

* `PUT /api/movies/<id>/`
  Update movie details (admin only).

* `DELETE /api/movies/<id>/`
  Delete a movie (admin only).

* `GET /api/movies/<id>/reviews/`
  List all reviews for a given movie.

### Reviews

* `POST /api/reviews/`
  Create a review (authenticated users only).
  Enforces one review per user per movie.

* `GET /api/reviews/<id>/`
  Retrieve a single review.

* `PUT /api/reviews/<id>/`
  Update the authenticated user’s own review.

* `DELETE /api/reviews/<id>/`
  Delete the authenticated user’s own review.

### Search, Filtering, and Pagination (Planned)

* Filter reviews by:

  * Movie title
  * Rating (e.g., only 4-star and 5-star reviews)
* Paginate review listings for performance.
* Sort by rating or created date.

---

## ✅ Capstone Requirements Checklist (High Level)

This project is designed to meet the ALX Backend Capstone criteria:

* [x] Public GitHub repository set up
* [x] README with project overview and setup instructions
* [x] Use Django ORM for all database interactions
* [x] Define models for Reviews and Users (using Django auth system)
* [x] Database supports multiple reviews per movie from different users
* [ ] CRUD for users and reviews via API endpoints
* [ ] View reviews for a specific movie
* [ ] Search/filter reviews by movie title and rating
* [ ] Authentication (login required for create/update/delete)
* [ ] Permissions (users can only modify their own reviews)
* [ ] Pagination and sorting for review listings
* [ ] Deployment to a live environment (PythonAnywhere / Heroku)
* [ ] Error handling with appropriate HTTP status codes and responses
* [ ] Logging and basic monitoring (planned)

---

## 🧪 Tests

Automated tests (unit tests and API tests) will be added later to cover:

* Model behavior and constraints
* API endpoints (CRUD operations)
* Authentication and permissions
* Filtering, search, and pagination

---

## 🤝 Contributing

This project is primarily for learning and assessment as part of the ALX Backend Capstone.
However, suggestions and improvements are welcome via issues or pull requests.

---

## 📄 License

This project is created for educational purposes as part of the **ALX Backend Engineering Capstone Project**.

You are free to fork and adapt it for learning, but please avoid submitting it as your own work in any formal academic or training context.


