# Travel Planner API

A RESTful API for managing travel projects and places. Built with FastAPI, SQLModel, and SQLite.

## Tech Stack

- **FastAPI** — web framework
- **SQLModel** — ORM (built on SQLAlchemy + Pydantic)
- **SQLite** — database
- **httpx** — async HTTP client for Art Institute of Chicago API
- **Docker** — containerization

---

## Getting Started

### Option 1 — Docker (recommended)

```bash
git clone https://github.com/your-username/travel-planner-api.git
cd travel-planner-api
docker compose up --build
```

API will be available at: `http://localhost:8000`

### Option 2 — Local

**Requirements:** Python 3.12+

```bash
git clone https://github.com/your-username/travel-planner-api.git
cd travel-planner-api

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

API will be available at: `http://localhost:8000`

---

## API Documentation

Interactive Swagger UI is available at:

```
http://localhost:8000/docs
```

ReDoc alternative:

```
http://localhost:8000/redoc
```

---

## Environment Variables

No required environment variables for local development — the app uses SQLite out of the box.

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///database.db` | Database connection string |

---

## Endpoints Overview

### Projects

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/projects` | List all projects (supports pagination) |
| `GET` | `/projects/{id}` | Get a single project |
| `POST` | `/projects` | Create a project (optionally with places) |
| `PATCH` | `/projects/{id}` | Update project info |
| `DELETE` | `/projects/{id}` | Delete a project |

### Places

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/projects/{id}/places` | List all places in a project |
| `GET` | `/projects/{id}/places/{place_id}` | Get a single place |
| `POST` | `/projects/{id}/places` | Add a place to a project |
| `PATCH` | `/projects/{id}/places/{place_id}` | Update notes or mark as visited |

---

## Example Requests

### Create a project with places

```bash
curl -X POST http://localhost:8000/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chicago Art Trip",
    "description": "My first art tour",
    "start_date": "2025-06-01",
    "places": [27992, 28560, 111628]
  }'
```

Place IDs must be valid artwork IDs from the [Art Institute of Chicago API](https://api.artic.edu/api/v1/artworks).

### Add a place to an existing project

```bash
curl -X POST http://localhost:8000/projects/1/places \
  -H "Content-Type: application/json" \
  -d '{"external_id": 27992}'
```

### Mark a place as visited

```bash
curl -X PATCH http://localhost:8000/projects/1/places/1 \
  -H "Content-Type: application/json" \
  -d '{"is_visited": true}'
```

### Update notes

```bash
curl -X PATCH http://localhost:8000/projects/1/places/1 \
  -H "Content-Type: application/json" \
  -d '{"notes": "Must see the Sunday on La Grande Jatte"}'
```

### List projects with pagination

```bash
curl "http://localhost:8000/projects?offset=0&limit=10"
```

---

## Business Rules

- A project can contain **1 to 10 places**
- The same place (by `external_id`) **cannot be added twice** to the same project
- A project **cannot be deleted** if any of its places are marked as visited
- Places are validated against the [Art Institute of Chicago API](https://api.artic.edu/docs/) before being stored

---

## Third-Party API

This project uses the **Art Institute of Chicago API** to validate and fetch artwork data.

- Base URL: `https://api.artic.edu/api/v1`
- Docs: [https://api.artic.edu/docs/](https://api.artic.edu/docs/)
- No API key required

Example — fetch a specific artwork:

```
GET https://api.artic.edu/api/v1/artworks/27992
```

---

## Project Structure

```
travel-planner-api/
├── app/
│   ├── api/
│   │   └── endpoints.py       # all route handlers
│   ├── core/
│   │   ├── database.py        # engine, session, create_tables
│   │   └── config.py          # settings and constants
│   ├── models/
│   │   ├── models.py          # SQLModel table definitions
│   │   └── schemas.py         # Pydantic request/response schemas
│   └── services/
│       └── artic.py           # Art Institute API client with caching
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```



Use the Swagger UI at `http://localhost:8000/docs` to explore and test all endpoints interactively.