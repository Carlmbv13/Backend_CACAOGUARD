# CacaoGuard - Black Pod Disease Monitoring System

A Django REST Framework backend for monitoring Black Pod Disease in cacao farms.

## Features

- JWT Authentication (Register, Login, Token Refresh)
- Farm Management (CRUD operations)
- Scan System with automated health score updates
- Alert System triggered by disease detection
- Dashboard Statistics
- Role-based access (Admin, Farmer, Technician)
- CORS enabled for frontend integration

## Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- Simple JWT for authentication
- SQLite3 (development) / PostgreSQL (production ready)
- Django CORS Headers

## Installation

### Prerequisites
- Python 3.10+
- pip
- virtualenv

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cacaoguard-backend.git
cd cacaoguard-backend

Create virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Run migrations:

bash
python manage.py makemigrations
python manage.py migrate
Seed the database:

bash
python manage.py seed_data
Create superuser:

bash
python manage.py createsuperuser
Run development server:

bash
python manage.py runserver
API Endpoints
Authentication
POST /api/auth/register/ - Register new user

POST /api/auth/login/ - Login (returns JWT token)

POST /api/auth/refresh/ - Refresh JWT token

Farms
GET /api/farms/ - List all farms

POST /api/farms/ - Create new farm

GET /api/farms/{id}/ - Get farm details

PUT /api/farms/{id}/ - Update farm

PATCH /api/farms/{id}/ - Partial update

DELETE /api/farms/{id}/ - Delete farm

Scans
GET /api/scans/ - List scans (filter by farm, severity)

POST /api/scans/ - Create new scan (auto-updates farm health)

Alerts
GET /api/alerts/ - List alerts

PATCH /api/alerts/{id}/update_status/ - Update alert status

Dashboard
GET /api/dashboard/stats/ - Get aggregated statistics

Users (Admin only)
GET /api/users/ - List all users

GET /api/users/me/ - Get current user profile

PATCH /api/users/me/ - Update profile