# 🎓Student Management System v2 

*A Modular, Persistent, CLI-Driven Student Record Manager built with Python*

A cleanly architected **command-line application** for managing student records with **data persistence, validation, logging, and structured business logic**.
Designed to demonstrate **backend fundamentals**, **OOP discipline**, and **real-world file handling** — not just CRUD.

> Built with separation of concerns in mind: models, services, storage, logging, and UI are fully decoupled.


---

## Quick Navigation

* [🎯 Project Overview](#-project-overview)
* [✨ Key Features](#-key-features)
* [🔧 Tech Stack & Requirements](#-tech-stack--requirements)
* [📦 Installation & Setup](#-installation--setup)
* [🧑‍💻 Usage (CLI Flow)](#-usage-cli-flow)
* [🧱 Architecture](#-architecture)
* [📁 Project Structure](#-project-structure)
* [📊 Data Persistence](#-data-persistence)
* [✅ Validation & Error Handling](#-validation--error-handling)
* [🪵 Logging & Auditing](#-logging--auditing)
* [🧪 Testing Strategy](#-testing-strategy)
* [🚧 Known Limitations (Intentional)](#-known-limitations-intentional)
* [🔮 Future Enhancements](#-future-enhancements)

---

## 🎯 Project Overview

**Student Management System v2** allows administrators to manage student data directly from the terminal while ensuring:

* Persistent storage using JSON
* Strong input validation
* Clean object-oriented design
* Atomic file writes (data safety)
* Structured logging for auditability

This project is intentionally **framework-free** to emphasize **core Python engineering skills**.

---

## ✨ Key Features

###  Core Functionality

*  Add new student records
*  View all students (clean formatted output)
*  Search students by **roll number** or **name**
*  Delete student records
*  Calculate and store percentage scores

###  Engineering Highlights

*  Modular architecture (models / services / storage / UI)
*  Atomic JSON persistence (prevents data corruption)
*  Timestamped student creation records
*  Centralized logging system
*  Test-ready design (tests added manually)

---

## 🔧 Tech Stack & Requirements

###  Core Requirements (Mandatory)

* **Python 3.10+**
* OS: Windows / Linux / macOS
* Basic terminal access

###  Libraries Used

| Purpose          | Tool                        |
| ---------------- | --------------------------- |
| File Handling    | `json`, `pathlib`           |
| Logging          | `logging`                   |
| Date & Time      | `datetime`                  |
| CLI Flow Control | `match-case` (Python 3.10+) |

> ❗ No external dependencies — everything runs on standard Python.

---

## 📦 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Tanu048/student-management-system-v2
# Navigate into project
cd student-management-system-v2

# Run the CLI application
python -m ui.cli
```

Create a student if file does not exist primerily 

---

## 🧑‍💻 Usage (CLI Flow)

```text
1. Add Student
2. View All Students
3. Search Student
4. Delete Student
5. Calculate Percentage
6. Exit
```

### Example Actions

* Add students with validation
* Search by class + roll number
* Compute average percentage from marks
* Persist data even after program exit

---

## 🧱 Architecture

```
┌──────────────────────────────┐
│           CLI (UI)           │
│        ui/cli.py             │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│      Business Logic Layer    │
│     services/manager.py      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│        Data Model            │
│     models/student.py        │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│     Persistent Storage       │
│ storage_handler/json_handler │
└──────────────────────────────┘
```

Each layer has **one responsibility** — no tight coupling, no shortcuts.

---

## 📁 Project Structure

```
student-management-system-v2/
│
├── models/
│   └── student.py          # Student data model
│
├── services/
│   └── manager.py          # Core business logic
│
├── storage_handler/
│   └── json_handler.py     # Atomic JSON read/write
│
├── ui/
│   └── cli.py              # Command-line interface
│
├── student_logging/
│   ├── student_log.py      # Logging configuration
│   └── students.log        # Log output
│
├── data/
│   └── students.json       # Persistent student records
│
├── .gitignore
└── README.md
```

---

## 📊 Data Persistence

* Student records are stored in a JSON file
* Records use a composite key (`standard-rollNumber`)
* Writes are atomic to avoid file corruption
* Missing or invalid files fail safely

---

## ✅ Validation & Error Handling

* Validation is enforced in the service layer
* Empty, invalid, or duplicate inputs are rejected
* All error cases are handled gracefully without crashing the application

---

## 🪵 Logging & Auditing

All major actions are logged with timestamps:

* Program start / exit
* Student creation
* Deletions
* Searches
* Errors & invalid inputs

Logs are written to:

```
student_logging/students.log
```

---

## 🧪 Testing Strategy

>  **Tests are intentionally added manually** to preserve full control and learning clarity.

* Designed to be compatible with:

  * `unittest`
  * `pytest`
* Business logic is isolated → easy unit testing
* JSON handler supports test-safe temporary files

**Recommended Test Areas**

* Student validation
* Duplicate prevention
* Percentage calculation
* JSON read/write integrity

---

## 🚧 Known Limitations (Intentional)

* CLI-only (no GUI)
* JSON storage (no database yet)
* Single-user environment 

These are deliberate to keep the focus on engineering fundamentals.

---

## 🔮 Future Enhancements

* Database-backed persistence (SQLite / PostgreSQL)
* REST API layer
* Automated test suite
* Web or terminal-based UI
* Authentication and access control

---

## ⭐ Final Note

This project is built to **think like a backend engineer**, not just finish a task.
If you value **clean architecture, correctness, and control**, this repo is for you.

---
