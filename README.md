# LSA Service Booking API

Django REST Framework project implementing:

- Parent, LSA_Profile and Booking_Request models
- POST /api/v1/bookings/
- GET /api/v1/lsas/search/?skill=Autism
- Mock external verification using requests
- Exception handling and logging
- Automated tests with pytest
- GitHub Actions CI

## Setup

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## POST booking

```json
{
  "parent": 1,
  "lsa": 1,
  "service_date": "2026-08-15",
  "service_time": "10:30:00",
  "notes": "Child requires learning support."
}
```

## Search LSA

GET:
`/api/v1/lsas/search/?skill=Autism`

## Tests

```bash
pytest
```

The LSA search performs filtering at the database level. For related booking data,
use Django `select_related("parent", "lsa")` to avoid N+1 queries.
