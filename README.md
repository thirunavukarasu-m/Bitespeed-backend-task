# 🔄 Bitespeed Backend Task – Identity Reconciliation

A Flask-based backend system for **identity reconciliation**, allowing deduplication and linking of contacts using phone numbers and emails. It provides both API endpoints and an admin dashboard to view reconciled contacts.

---

## 🔗 Deployment URLs

| Environment    | URL                                                                                                  |
| -------------- | ----------------------------------------------------|
|   |
| **Production** | [https://bitespeed-backend-task-gvq5.onrender.com](https://bitespeed-backend-task-gvq5.onrender.com) |

---

### 🔀 Branching Strategy

This project follows real-world professional development practices:

* **`main`** – Stable production branch deployed to Render Production
* **`development`** – Integration branch where feature branches are merged and tested before production release
* **Feature branches** – Each feature is developed in its own branch (e.g., `feature/admin-login-page`, `feature/identity-endpoint`)
* **Hotfix / Release branches** – Temporary branches like `push-to-prod/05-07-2025` used for final production merges or patches

All feature branches go through a Pull Request and review before merging into `development` and then `main`.

Example Pull Requests:

* Added `/identify` endpoint
* Created login and contact view pages
* Setup production deployment requirements


## 🧩 Features

* ✅ `/identify` API to manage and reconcile contact information
* ✅ Auto-linking based on `email` and `phoneNumber`
* ✅ Admin login to view all contacts
* ✅ Contacts page shows all entries from the database
* ✅ PostgreSQL integration via SQLAlchemy
* ✅ Deployed on Render (Free Tier)

---

## 🏠 Pages Overview

### 📍 Home Page

**URL:** `/`
A simple landing page for the application that introduces the backend task and guides the user.

---

### 🔐 Admin Login

**URL:** `/admin`
Enter admin credentials to view the reconciled contacts.

* **Username:** `admin`
* **Password:** `bitespeed`

---

### 📋 Contacts Page

**URL:** `/contacts`
After successful login, you will be redirected here to view all the contacts stored in the PostgreSQL database. This includes primary and secondary contacts with their linked metadata.

---

## 📡 API

### POST `/identify`

Reconciles identity based on provided `email` and/or `phoneNumber`.

#### Request Body

```json
{
  "email": "john@example.com",
  "phoneNumber": "1234567890"
}
```

#### Response

```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["john@example.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": [2, 3]
  }
}
```

---

## 🗄️ Tech Stack

* **Backend:** Python, Flask
* **ORM:** SQLAlchemy
* **Database:** PostgreSQL (Hosted on Render)
* **Frontend:** HTML/CSS (with custom design matching Bitespeed branding)
* **Deployment:** [Render.com](https://render.com)

---

## 🚀 How to Run Locally

1. **Clone the repo**

   ```bash
   git clone https://github.com/YOUR_USERNAME/bitespeed-backend-task.git
   cd bitespeed-backend-task
   ```

2. **Set up environment**
   Create a `.env` file:

   ```env
   FLASK_ENV=uat
   SECRET_KEY=super_secret
   SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/bitespeed
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=bitespeed
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   python3 app.py
   ```

---

## 📦 Deployment on Render

* Add the following **start command** in Render:

  ```
  gunicorn app:app
  ```

* Ensure the following environment variables are set in Render:

  * `SECRET_KEY`
  * `SQLALCHEMY_DATABASE_URI`
  * `ADMIN_USERNAME`
  * `ADMIN_PASSWORD`

---

## Acknowledgment

This project was built as part of the Bitespeed Backend Engineering task to demonstrate identity resolution using contacts.

