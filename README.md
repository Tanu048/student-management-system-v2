# 🎓 Student Management System v2

**Production-Grade REST API + CLI for Student Record Management**

A cleanly architected backend system demonstrating **production engineering fundamentals**: proper API design, data validation, testing, logging, and error handling—without unnecessary complexity.

> Built to show I understand how to build **reliable systems**, not just make things work.

🔗 **Live Demo:** [https://student-management-system-js6u.onrender.com](https://student-management-system-js6u.onrender.com)  
📖 **API Docs:** [https://student-management-system-js6u.onrender.com/docs](https://student-management-system-js6u.onrender.com/docs)

---

## 📋 Quick Navigation

- [What This Project Shows](#-what-this-project-shows)
- [Tech Stack](#-tech-stack)
- [Live Demo](#-live-demo)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Architecture](#-architecture)
- [Testing](#-testing)

---

## 🎯 What This Project Shows

This isn't just a student database. It demonstrates:

| Skill | What You'll See |
|-------|-----------------|
| **API Design** | RESTful endpoints with proper HTTP status codes (200, 400, 404, 409) |
| **Data Validation** | Type hints + Pydantic models + custom validators |
| **Error Handling** | Graceful failures, meaningful error messages, no print statements |
| **Auth & RBAC** | JWT authentication with role-based access control (admin / viewer) |
| **Testing** | 20+ tests covering happy paths, edge cases, and error scenarios |
| **Logging** | Structured logging for auditing and debugging |
| **Clean Code** | Separation of concerns (models → services → API → storage) |

---

## 🔧 Tech Stack

```
Framework:        FastAPI 0.128.0        (REST API)
Database:         PostgreSQL 15+         (Persistent storage)
ORM:              SQLAlchemy 2.0.46      (Object-relational mapping)
Validation:       Pydantic 2.12.5        (Type checking)
Auth:             PyJWT + pwdlib         (JWT tokens + password hashing)
CLI:              Python match-case      (Built-in 3.10+)
Testing:          pytest 9.0.2           (Unit & integration tests)
Mocking:          pytest-mock 3.15.1     (Test isolation)
Logging:          Python logging         (Structured logs)
Containerization: Docker + Docker Compose
Deployment:       Render
Python:           3.10+
```

---

## 🚀 Live Demo

The API is deployed and live on Render.

| | Link |
|---|---|
| **Frontend** | [https://student-management-system-js6u.onrender.com](https://student-management-system-js6u.onrender.com) |
| **Swagger UI** | [https://student-management-system-js6u.onrender.com/docs](https://student-management-system-js6u.onrender.com/docs) |

**To try it out:**
1. Go to the frontend link above
2. Register a viewer account (no key needed)
3. Login and explore — view students, search, get percentages
4. To test admin features, register with `role: admin` and the admin key

> ⚠️ Render free tier spins down after inactivity — first request may take ~30 seconds to wake up.

---

## 📦 Getting Started

### Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/student_management_database
SECRET_KEY=your-secret-key
ALGORITHM=HS256
EXPIRE_MINUTES=60
ADMIN_REGISTRATION_KEY=your-admin-key

# For Docker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=student_management_database
```

### Option 1 — Local Development (Without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database
createdb student_management_database

# Run the API
uvicorn main:app --reload
```

API available at: http://localhost:8000

### Option 2 — Run with Docker

```bash
# Build and start
docker-compose up --build

# Stop
docker-compose down
```

---

## 🔌 API Endpoints

| Method | Endpoint | Role Required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | Public | Register a new user |
| POST | `/auth/login` | Public | Login and get JWT token |
| GET | `/auth/is_auth` | Any | Verify token / get current user |
| GET | `/student/view_students` | admin, viewer | View all students |
| GET | `/student/search_by_roll?std=X&roll=Y` | admin, viewer | Search by roll number |
| GET | `/student/search_by_name?name=X` | admin, viewer | Search by name |
| GET | `/student/percent_student?std=X&roll=Y` | admin, viewer | Get student percentage |
| POST | `/admin/add_students` | admin | Add a new student |
| DELETE | `/admin/delete_students?std=X&roll=Y` | admin | Delete a student |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI (main.py)                        │
│              REST API Endpoint Handling                     │
│         Input validation (Pydantic models)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              StudentManager (services/)                     │
│           Business Logic & Orchestration                    │
│  - Duplicate prevention                                     │
│  - Data transformation                                      │
│  - Percentage calculations                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│        Database Layer (storage_handler/)                    │
│  - StudentDB: Connection & transactions                     │
│  - db_mapper: Domain ↔ Database conversion                  │
│  - db_model: SQLAlchemy schema                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│            PostgreSQL Database                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
student-management-system-v2/
│
├── main.py                          # FastAPI app entry point
├── routers/
│   ├── auth.py                      # Register, login, token endpoints
│   ├── admin.py                     # Add/delete students (admin only)
│   └── student.py                   # View/search students (admin + viewer)
├── schemas/
│   ├── admin.py                     # Auth Pydantic models
│   └── student.py                   # Student Pydantic models
├── models/
│   └── student.py                   # Student domain model
├── services/
│   └── manager.py                   # Business logic orchestration
├── storage_handler/
│   └── db_handler/
│       ├── db_handler.py            # PostgreSQL connection & queries
│       ├── db_mapper.py             # Domain ↔ Database mapping
│       └── db_model.py              # SQLAlchemy schema definitions
├── templates/
│   ├── base.html                    # Shared base template
│   ├── home.html                    # Landing page
│   ├── login.html                   # Login page
│   ├── register.html                # Register page
│   └── dashboard.html               # Main dashboard
├── static/
│   ├── style.css                    # Styles
│   └── script.js                    # Frontend logic
├── student_logging/
│   └── student_log.py               # Logging configuration
├── testing/
│   ├── test_main.py                 # API endpoint tests
│   ├── test_manager.py              # Business logic tests
│   ├── test_validators.py           # Input validation tests
│   └── test_json_handler.py         # Storage layer tests
├── ui/
│   └── cli.py                       # CLI interface
├── validators.py                    # Input validation functions
├── requirements.txt
├── docker-compose.yaml
└── Dockerfile
```

---

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run specific file
pytest testing/test_main.py -v

# Coverage report
pytest --cov=. --cov-report=html
```

Then open `htmlcov/index.html` in browser.

---

## 📄 License

MIT License — feel free to use for learning purposes.

---

**Last Updated:** March 2026  
**Next Version:** CI/CD pipeline