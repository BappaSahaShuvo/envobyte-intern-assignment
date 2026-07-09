# 📇 Monica CRM - Contact Module API 

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.2-092E20)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192)

## 📌 Project Overview
This repository contains the backend API implementation for the Envobyte Intern Assignment. While the original Monica CRM is a monolithic application built with Laravel/PHP, this project was developed as a **standalone, scalable REST API** using **Python and Django REST Framework**, as approved by the hiring team. 

The API successfully extends a base Contact module with custom fields, filtering, aggregation, and JWT-secured endpoints while adhering to standard RESTful conventions.

## 🚀 Implementation Approach
Instead of forking the original repository and mixing Python with PHP, I engineered a clean-slate Django API that strictly replicates the database schemas and endpoint requirements outlined in the project brief. 

**Key Features Implemented:**
* **Database Expansion:** Added `is_favorite` (boolean) and `personal_note` (text) to the Contact model.
* **Advanced Filtering:** Built robust querying to support `?is_favorite=True` and `?search=keyword` without duplicating query logic.
* **Optimized Aggregation:** Implemented the `/stats` endpoint using database-level aggregation (Django's `Count` and `Q` objects) to ensure efficient performance without loading records into memory.
* **Security:** Integrated JSON Web Tokens (JWT) for secure authentication.
* **Automated Testing:** Wrote comprehensive unit/feature tests for API stability.

---

## 🛠️ Tech Stack
* **Framework:** Django & Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Authentication:** djangorestframework-simplejwt
* **Data Seeding:** Faker
* **Filtering:** django-filter

---

## ⚙️ Setup & Installation Instructions

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/envobyte-intern-assignment-api.git](https://github.com/your-username/envobyte-intern-assignment-api.git)
cd envobyte-intern-assignment-api
