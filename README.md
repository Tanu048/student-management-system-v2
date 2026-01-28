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
Backend:       FastAPI (async web framework)
Validation:    Pydantic (data models)
Storage:       JSON (file-based persistence)
Testing:       pytest + pytest-mock
Logging:       Python logging module
Python:        3.10+
```

**No external database needed for this demo.** 

---

## 📦 Getting Started

### Prerequisites
- Python 3.10 or higher
- `pip` (Python package manager)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

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

```
┌─────────────────────────────────────────┐
│          FastAPI (main.py)              │
│      HTTP Request Handling              │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│     StudentManager (services/)          │
│     Core Business Logic                 │
│    Duplicate checking                   │
│    Data transformations                 │
│    Percentage calculations              │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│      Student Model (models/)            │
│    Data Structure & Validation          │
│    Type hints                           │
│    Percentage property                  │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│    StudentJson (storage_handler/)       │
│     Persistent Data Layer               │
│    Atomic file writes                   │
│    Error recovery                       │
└─────────────────────────────────────────┘
```
---

## 📁 Project Structure

```
student-management-system-v2/
│
├── main.py                    # FastAPI app + endpoints
├── models/
│   └── student.py            # Student data model
│
├── services/
│   └── manager.py            # Business logic
│
├── storage_handler/
│   └── json_handler.py       # Data persistence (JSON read/write)
│
├── ui/
│   └── cli.py                # Command-line interface
│
├── student_logging/
│   ├── student_log.py        # Logging setup
│   └── students.log          # Application logs
│
├── data/
│   └── students.json         # Student records (auto-created)
│
├── testing/
│   ├── test_main.py          # API endpoint tests
│   ├── test_manager.py       # Business logic tests
│   ├── test_validators.py    # Validation tests
│   └── test_json_handler.py  # Storage tests
│
├── validators.py             # Input validation
├── requirements.txt          # Dependencies
└── README.md                 # This file
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