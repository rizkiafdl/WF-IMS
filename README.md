# WF-IMS — Wood Fuel Integrated Management System

ERP for wood pellet manufacturing: Procurement → Production → Sales.

**Stack:** Python 3.12 · Flask · SQLAlchemy · SQLite · Jinja2

---

## Quick Start

### 1. Clone & enter the project

```bash
cd project-lms
```

### 2. Create virtual environment

```bash
uv venv --python 3.12
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Initialize the database

```bash
flask db upgrade
```

### 5. Seed the admin user

```bash
flask seed-admin
```

Credentials: `admin@wfims.com` / `admin123`

### 6. Run the dev server

```bash
flask run
```

Open [http://localhost:5000](http://localhost:5000) and log in.

---

## Project Structure

```
project-lms/
├── run.py                  # Entry point
├── config.py               # App config (dev)
├── requirements.txt
│
├── app/
│   ├── __init__.py         # App factory (create_app)
│   ├── extensions.py       # db, login_manager, migrate
│   ├── utils.py            # Shared helpers (gen_doc_number)
│   ├── models/             # SQLAlchemy models
│   ├── blueprints/         # One blueprint per module
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── master/
│   │   ├── procurement/
│   │   ├── production/
│   │   ├── sales/
│   │   └── inventory/
│   └── templates/          # Jinja2 templates
│
├── static/
│   ├── css/                # tokens → base → layout → components → main
│   └── js/
│
└── instance/
    └── wfims.db            # SQLite database (auto-created)
```

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `flask run` | Start dev server on port 5000 |
| `flask run --debug` | Start with auto-reload |
| `flask db migrate -m "msg"` | Generate new migration |
| `flask db upgrade` | Apply migrations to DB |
| `flask seed-admin` | Create default admin user |
| `flask shell` | Interactive Python shell with app context |

---

## Default Login

| Field | Value |
|-------|-------|
| Email | `admin@wfims.com` |
| Password | `admin123` |

> Change this immediately in any non-local environment.

---

## Build Status

| Phase | Module | Status |
|-------|--------|--------|
| 1 | Foundation | ✅ Done |
| 2 | Database Models | ✅ Done |
| 3 | CSS Design System | ✅ Done |
| 4 | Base Templates | ✅ Done |
| 5 | Auth | ✅ Done |
| 6 | Dashboard | ✅ Done |
| 7 | Master Data | ✅ Done |
| 8 | Procurement | ✅ Done |
| 9 | Production | 🔲 Pending |
| 10 | Sales | 🔲 Pending |
| 11 | Inventory | 🔲 Pending |
| 12 | Wire-up & Verify | 🔲 Pending |
