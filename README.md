# 🏔️ Everest Equity - Backend

> A Django REST Framework API for managing investments, contributions, proposals, voting, and meetings for an investment club.

---

## 🚀 Features

- 🔐 User registration and JWT authentication
- 💸 Contribution tracking with filtering & CSV export
- 📈 Investment management with admin-only manual updates
- 🗳️ Proposal creation and voting system
- 🗓️ Meeting scheduling (admin-only)
- 📚 Educational investment resources endpoint

---

## ⚙️ Setup & Installation

### ✅ Prerequisites

- Python 3.10+
- pip
- virtualenv _(recommended)_

### 📦 Installation Steps

1. **Clone the repository**:

   ```bash
   git clone git@github.com:MindRisers-Technologies/Everest_equity-backend.git
   cd equity_everest
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

---

## 🌐 API Endpoints

| Endpoint                          | Method   | Description                         | Permission            |
| --------------------------------- | -------- | ----------------------------------- | --------------------- |
| `/api/register/`                  | POST     | Register new user                   | 🔐 Admin only         |
| `/api/login/`                     | POST     | Obtain JWT token                    | 🌍 Public             |
| `/api/logout/`                    | POST     | Logout (blacklist token)            | 🔒 Authenticated      |
| `/api/contributions/`             | GET/POST | List/create contributions           | 👤 Member (GET, POST) |
| `/api/contributions/export/`      | GET      | Export contributions as CSV         | 🔒 Authenticated      |
| `/api/investments/`               | GET/POST | List/create investments             | 🛡️ Admin or ReadOnly  |
| `/api/investments/manual-update/` | POST     | Update investment value manually    | 🛡️ Admin/SuperAdmin   |
| `/api/proposals/`                 | GET/POST | List/create proposals               | 👤 Authenticated      |
| `/api/proposals/<id>/vote/`       | POST     | Vote on a proposal                  | 👤 Authenticated      |
| `/api/meetings/`                  | GET/POST | List/schedule meetings              | 🛡️ Admin can schedule |
| `/api/educational-resources/`     | GET      | List investment resources           | 👤 Authenticated      |
| `/api/dashboard/`                 | GET      | Summary of contributions, portfolio | 👤 Authenticated      |

---

## 🔐 Permissions

- **Admin/SuperAdmin**: Full access to all endpoints and admin features.
- **Member**: Can view and submit contributions/proposals.
- **Unauthenticated users**: Can only access login. Registration is admin-controlled.

---

## 📚 Educational Resources

- 🌐 [SEBON Official Website](https://www.sebon.gov.np)
- 🌐 [ShareSansar](https://www.sharesansar.com)
- 🌐 [Investment Guide - Basics](https://www.investmentguide.com/basics)
# Investment-Club
