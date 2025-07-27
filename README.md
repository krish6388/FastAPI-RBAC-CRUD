# 🗂️ Project Management Backend (FastAPI + PostgreSQL)

This is a backend project built with **FastAPI**, **SQLModel**, and **PostgreSQL**, implementing secure user registration and login with **JWT authentication** and **role-based access control**.

> This project was developed as part of a technical assessment to demonstrate secure REST API design, RBAC implementation, and clean database modeling with PostgreSQL.

---

## 🚀 Features

- 🔐 User Registration & Login (JWT-based)
- 🧾 Role-based Authorization (`admin`, `employee`)
- 🧰 Projects CRUD:
  - `POST /projects/` (admin only)
  - `GET /projects/` (all users)
  - `DELETE /projects/{id}` (admin only)
- 🧼 Password hashing (bcrypt)
- 🧪 API tested using Swagger UI (`/docs`)
- 🗃️ PostgreSQL + SQLModel with async support

---

## 🛠️ Tech Stack

- **FastAPI**
- **SQLModel** (async)
- **PostgreSQL**
- **Pydantic**
- **Python 3.11+**
- **bcrypt**
- **JWT (PyJWT)**

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/krish6388/FastAPI-RBAC-CRUD.git
cd FastAPI-RBAC-CRUD

### 2. Create virtual environment

python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up Environment Variables

DATABASE_URL=postgresql+asyncpg://postgres:<your_password>@localhost:5432/<your_db>
JWT_SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

▶️ Run the App

uvicorn main:app --reload

🧪 API Endpoints
Auth
POST /register → Register user (admin/employee)

POST /login → Get access token

Projects
POST /projects/ → Create project (admin only)

GET /projects/ → List all projects (all roles)

DELETE /projects/{id} → Delete project (admin only)
