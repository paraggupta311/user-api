Django User API with Filtering, Sorting, and Pagination

This project is a Django REST Framework (DRF) API for managing user data. It supports:
    - Full CRUD for users.
    - Filtering by name (first name or last name).
    - Sorting by any field (e.g., ?sort=-age).
    - Pagination with page and limit query parameters.
    - Unit testing with detailed logging.

Features
    - DRF-based API for User model
    - Supports GET /api/users/ with:
        - ?name=... to filter users by first or last name.
        - ?sort=... for ascending/descending sort.
        - ?page=... and ?limit=... for pagination.

Tech Stack
    - Python 3.8+
    - Django 4.x
    - Django REST Framework
    - SQLite (default)
    - Pytest/unittest for testing

Installation & Setup
    1) CLone the Repository
            - https://github.com/paraggupta311/user-api.git
            - cd user-api

    2) Install Dependencies
            - pip install -r requirements.txt
    
    3) Apply Migrations
        - python manage.py makemigrations
        - python manage.py migrate

    4) Create a Superuser (Admin)
        - python manage.py createsuperuser

    5) Run the Development Server
        - python manage.py runserver

Access the API at: http://127.0.0.1:8000/api/users

API Usage
Endpoint: /api/users/

Query Param	                    Description
name	                        Filter by first or last name (?name=jam)
sort	                        Sort by any field, use - for descending (?sort=-age)
page	                        Page number for pagination
limit	                        Number of results per page

Example
GET /api/users/?name=jam&sort=-age&page=1&limit=5

Running Tests
python manage.py test


