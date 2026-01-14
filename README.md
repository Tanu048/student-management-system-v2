# Student Management System v2

A Python-based CLI application for managing student records with persistent JSON storage.

## Features
- Add, update, delete, and search student records
- Calculate student performance percentages
- View all student records with organized display
- Persistent data storage using JSON

## Tech Stack
- Python 3.8+
- JSON for data persistence
- argparse/match-case for CLI

## Installation
1. Clone the repository
2. cd student-management-system-v2
3. python -m ui.cli

## Project Structure
- `models/` - Student data model
- `services/` - Business logic (Manager class)
- `storing/` - JSON file operations
- `ui/` - Command-line interface
- `data/` - Student data (JSON)

## Usage
Run: `python -m ui.cli`

## Future Improvements
- Database integration (SQLite/PostgreSQL)
- Web interface (Flask/Django)
- User authentication
- Advanced search filters
