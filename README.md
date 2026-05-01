# Role-Based Access Control (RBAC) - Healthcare System

> **Internship Milestone Project**  
> This repository contains a backend implementation of a Role-Based Access Control system developed during the early stages of my second internship. The focus of this project was to master secure user authentication and permission-based routing.

## 📌 Project Overview
In a healthcare environment, data privacy is critical. This project implements a system where different users—**Admins, Doctors, and Patients**—have strictly defined access levels to various API endpoints using FastAPI and SQLAlchemy.

## 🛠️ Tech Stack
*   **Framework:** FastAPI
*   **Database:** PostgreSQL (with SQLAlchemy ORM)
*   **Migrations:** Alembic
*   **Security:** JWT (JSON Web Tokens) & Bcrypt (Password Hashing)
*   **Environment Management:** Python-Dotenv

## 🚀 Key Features
*   **Secure Authentication:** User registration and login with encrypted passwords and JWT token generation.
*   **Custom RBAC Middleware:** A reusable `role_required` dependency that prevents unauthorized users from accessing sensitive routes.
*   **Relational Database Design:** 
    *   **Users:** Base table for all accounts.
    *   **DoctorDetails:** Specific metadata for medical staff.
    *   **Appointments:** Relational mapping between doctors and patients.
*   **Database Versioning:** Full integration with Alembic for tracking schema changes.

## 📂 Project Structure
```text
├── alembic/           # Migration scripts
├── alembic.ini        # Alembic configuration
├── main.py            # FastAPI application logic and RBAC implementation
├── .env               # Environment variables (Database URL, Secret Key)
└── requirements.txt   # Project dependencies
