# 🎓 Student Management System v2

**Production-Grade REST API + CLI for Student Record Management**

A cleanly architected backend system demonstrating **production engineering fundamentals**: proper API design, data validation, testing, logging, and error handling—without unnecessary complexity.

> Built to show I understand how to build **reliable systems**, not just make things work.

---

## 📋 Quick Navigation

- [What This Project Shows](#-what-this-project-shows)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [How to Use](#-how-to-use)
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
| **Testing** | 20+ tests covering happy paths, edge cases, and error scenarios |
| **Logging** | Structured logging for auditing and debugging |
| **Clean Code** | Separation of concerns (models → services → API → storage) |
| **Input Validation** | Both CLI and API validate before processing |

---

## 🔧 Tech Stack

```
Framework:        FastAPI 0.128.0        (REST API)
Database:         PostgreSQL 15+         (Persistent storage)
ORM:              SQLAlchemy 2.0.46      (Object-relational mapping)
Validation:       Pydantic 2.12.5        (Type checking)
CLI:              Python match-case      (Built-in 3.10+)
Testing:          pytest 9.0.2           (Unit & integration tests)
Mocking:          pytest-mock 3.15.1     (Test isolation)
Logging:          Python logging         (Structured logs)
Python:           3.10+
```

---

## 📦 Getting Started

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 15+ (running locally or remote)
- pip (Python package manager)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```bash
# Create database
createdb student_management_database

# Initialize tables (from Python)
python -c "from storage_handler.db_handler.db_handler import StudentDB; StudentDB.make_relation()"
```

# Run the API
uvicorn main:app --reload
```

API available at: http://localhost:8000/docs
---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/add_students` | Add a new student |
| GET | `/view_students` | View all students |
| GET | `/students/search/by_roll?std=X&roll=Y` | Search by roll number |
| GET | `/students/search/by_name?name=X` | Search by name |
| GET | `/percent_student?std=X&roll=Y` | Get student percentage |
| DELETE | `/delete_students?std=X&roll=Y` | Delete student |
```
---

## 💻 How to Use

### Option 1: Using FastAPI Swagger UI (Easiest)

1. Run: `uvicorn main:app --reload`
2. Open: http://localhost:8000/docs
3. Click any endpoint → Click "Try it out" → Fill in data → Click "Execute"

### Option 2: Using cURL

```bash
# Add a student
curl -X POST http://localhost:8000/add_students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Asha",
    "std": "10",
    "roll": "1",
    "marks": [85, 90, 78, 88, 92]
  }'

# View all students
curl http://localhost:8000/view_students

# Search by roll
curl "http://localhost:8000/students/search/by_roll?std=10&roll=1"

# Get percentage
curl "http://localhost:8000/percent_student?std=10&roll=1"

# Delete student
curl -X DELETE "http://localhost:8000/delete_students?std=10&roll=1"
```

### Option 3: CLI Interface

```bash
python -m ui.cli
```

Interactive menu-driven interface for non-technical users.

---

## 🏗️ Architecture

### Layered Design

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
│  - Cache management                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│        Student Model (models/student.py)                    │
│     Domain Object & Data Structure                          │
│  - Properties (@percentage)                                 │
│  - Serialization (to_dict)                                  │
│  - Timestamps                                               │
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
│        Persistent Student Records                           │
└─────────────────────────────────────────────────────────────┘
```
---

## 📁 Project Structure
```
student-management-system-v2/
│
├── main.py                          # FastAPI app & REST endpoints
│
├── models/
│   ├── __init__.py
│   └── student.py                   # Student domain model
│
├── services/
│   ├── __init__.py
│   └── manager.py                   # Business logic orchestration
│
├── storage_handler/
│   ├── __init__.py
│   ├── json_handler.py              # Legacy JSON persistence (deprecated)
│   └── db_handler/
│       ├── __init__.py
│       ├── db_handler.py            # PostgreSQL connection & queries
│       ├── db_mapper.py             # Domain ↔ Database mapping
│       └── db_model.py              # SQLAlchemy schema definitions
│
├── ui/
│   ├── __init__.py
│   └── cli.py                       # Command-line interface
│
├── student_logging/
│   ├── __init__.py
│   ├── student_log.py               # Logging configuration
│   └── students.log                 # Application logs
│
├── testing/
│   ├── __init__.py
│   ├── test_main.py                 # API endpoint tests
│   ├── test_manager.py              # Business logic tests
│   ├── test_validators.py           # Input validation tests
│   └── test_json_handler.py         # Storage layer tests
│
├── validators.py                    # Input validation functions
├── requirements.txt                 # Project dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest testing/test_main.py -v
```

### Generate Coverage Report

```bash
pytest --cov=. --cov-report=html
```

Then open `htmlcov/index.html` in browser.

---

## 🐛 Known Limitations (Intentional)

- **JSON storage** - Fine for demo, needs PostgreSQL for production
- **Single instance** - No clustering/load balancing
- **No authentication** - Anyone can access all endpoints
- **No rate limiting** - Could be abused with many requests

These are deliberate to keep focus on engineering fundamentals.

---

## 📄 License
MIT License - Feel free to use for learning purposes.

---

**Last Updated:** January 25, 2026
**Status:** ✅ Production Ready (JSON version)
**Next Version:** PostgreSQL + Docker + CI/CD (Feb 2026)