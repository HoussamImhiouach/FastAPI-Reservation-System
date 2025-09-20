# FastAPI Reservation System

A minimal reservation API built with **FastAPI** + **SQLAlchemy** + **MySQL**, allowing you to manage **clients**, **rooms**, and **reservations**.

- **Tech**: FastAPI, SQLAlchemy ORM, MySQL (PyMySQL driver)
- **Endpoints**: Create/read clients, rooms, and reservations
- **Focus**: Clean CRUD patterns, relational integrity, simple deploy

---

## 📑 Table of contents
- [Architecture](#architecture)
- [DB schema (ER)](#db-schema-er)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
  - [1) Prerequisites](#1-prerequisites)
  - [2) Create the database](#2-create-the-database)
  - [3) Configure environment](#3-configure-environment)
  - [4) Install & run](#4-install--run)
- [API reference](#api-reference)
  - [POST /clients](#post-clients)
  - [POST /rooms](#post-rooms)
  - [POST /reservations](#post-reservations)
  - [GET /clients](#get-clients)
  - [GET /rooms](#get-rooms)
  - [GET /reservations](#get-reservations)
- [Troubleshooting](#troubleshooting)
- [Future improvements](#future-improvements)
- [License](#license)

---

## ⚙️ Architecture

- **FastAPI** handles routing and input validation.
- **SQLAlchemy** manages the ORM layer and session lifecycle.
- **MySQL** stores data across three tables with foreign-key relations.

Core files:
- `main.py` – FastAPI app, routes, DB session dependency
- `database.py` – engine/session/base setup
- `models.py` – SQLAlchemy models
- `reservation_db.sql` – schema DDL (MySQL)

---

## 🗄️ DB schema (ER)

```
Client (clients)                   Room (rooms)                   Reservation (reservations)
------------------                 --------------                 --------------------------
id : INT PK                        id : INT PK                    id : INT PK
name : VARCHAR(100)                number : VARCHAR(50) UNIQUE    client_id : INT FK -> clients.id
email : VARCHAR(100) UNIQUE        type : VARCHAR(50)             room_id : INT FK -> rooms.id
                                   price : DECIMAL(10,2)          date : DATE
```

Constraints:
- `reservations.client_id` references `clients.id`
- `reservations.room_id` references `rooms.id`
- `clients.email` and `rooms.number` are **unique**

---

## 📂 Project structure

```
FastAPI-Reservation-System/
├─ database.py          # Engine, SessionLocal, Base (SQLAlchemy)
├─ main.py              # FastAPI app + endpoints
├─ models.py            # ORM models: Client, Room, Reservation
├─ reservation_db.sql   # MySQL DDL script to create schema
├─ README.md
└─ .gitignore
```

---

## 🚀 Getting started

### 1) Prerequisites
- Python **3.11+**
- MySQL server
- Git

Install dependencies (suggested `requirements.txt`):
```
fastapi
uvicorn
sqlalchemy
pymysql
python-dotenv
```

---

### 2) Create the database

Run this SQL (in MySQL Workbench / CLI):

```sql
CREATE DATABASE reservation_db;
USE reservation_db;

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(50),
    price DECIMAL(10, 2)
);

CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    room_id INT NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);
```

---

### 3) Configure environment

In `database.py` the connection string is:

```python
DATABASE_URL = "mysql+pymysql://root:@localhost/reservation_db"
```

Update with your own username/password as needed.  
(For production: move this into a `.env` file and load it.)

---

### 4) Install & run

```bash
# 1) Install deps
pip install -r requirements.txt

# 2) Start the API (reload for dev)
uvicorn main:app --reload
```

Interactive docs:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**:     http://127.0.0.1:8000/redoc

---

## 📡 API reference

> Endpoints accept **query parameters** (e.g., `?name=...&email=...`).  
> You can test in Swagger UI or with `curl`.

---

### POST `/clients/`
Create a new client.

**Params**
- `name` (str, required)
- `email` (str, required, unique)

```bash
curl -X POST "http://127.0.0.1:8000/clients/?name=Alice&email=alice@example.com"
```

---

### POST `/rooms/`
Create a new room.

**Params**
- `number` (str, required, unique)
- `room_type` (str, optional)
- `price` (float, optional)

```bash
curl -X POST "http://127.0.0.1:8000/rooms/?number=101&room_type=double&price=149.99"
```

---

### POST `/reservations/`
Create a reservation (client and room must exist).

**Params**
- `client_id` (int, required)
- `room_id` (int, required)
- `date` (str, required — format `YYYY-MM-DD`)

```bash
curl -X POST "http://127.0.0.1:8000/reservations/?client_id=1&room_id=1&date=2025-09-20"
```

---

### GET `/clients/`
List clients.

```bash
curl "http://127.0.0.1:8000/clients/"
```

---

### GET `/rooms/`
List rooms.

```bash
curl "http://127.0.0.1:8000/rooms/"
```

---

### GET `/reservations/`
List reservations.

```bash
curl "http://127.0.0.1:8000/reservations/"
```

---

## 🔧 Troubleshooting

- **Access denied to MySQL** → Check your `DATABASE_URL` user/password.  
- **Tables not created** → Make sure `reservation_db` exists.  
- **Date parsing errors** → Use format `YYYY-MM-DD`.  
- **Port already in use** → Run with `--port 8001`.

---

## 🔮 Future improvements

- Use Pydantic models for request bodies & responses.  
- Return created objects instead of plain messages.  
- Add uniqueness checks + error handling.  
- Add filtering & pagination.  
- Add authentication/roles.  
- Manage DB migrations with Alembic.  
- Dockerize app with MySQL container.  
- Write unit tests with pytest & FastAPI TestClient.

---

## 📜 License
MIT (or your choice).
