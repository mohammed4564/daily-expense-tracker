# Daily Expense Tracker

A web-based application built with **Python Flask and PostgreSQL** to manage daily expenses, track spending, and generate reports with analytics.

## Features

### User Authentication
- User registration
- User login
- JWT-based authentication
- Secure password hashing
- User-specific expense records

### Expense Management
- Add new expenses
- View all expenses
- View individual expense details
- Edit existing expenses
- Delete expenses
- Categorize expenses
- Filter expenses by date

### Dashboard
- View total expenses
- View selected-period spending
- View transaction count
- Filter expenses using date ranges
- Edit and delete transactions

### Reports and Analytics
- This Week, This Month, and This Year reports
- Custom date-range reports
- Total spending
- Transaction count
- Average expense
- Highest expense
- Previous-period comparison
- Monthly budget tracking
- Budget performance grade (A–E)
- Category-wise spending chart
- Spending trend chart
- Top spending category
- Spending insights
- Download PDF reports

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL |
| Database Connectivity | psycopg2 |
| Authentication | JWT |
| Password Security | Werkzeug |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| PDF Generation | jsPDF, jsPDF-AutoTable |
| Deployment | Render |
| Version Control | Git and GitHub |
| Production Server | Gunicorn |

## Project Structure

```text
daily_expense_tracker/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── utils/
│   └── db_connect.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_expense.html
│   ├── edit_expense.html
│   └── reports.html
│
└── static/
    └── css/
        └── style.css
```

## Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE DAILY_EXPENSE_DB;
```

The application uses two main tables:

**1. users**
- user_id
- username
- email
- password_hash
- full_name
- is_active
- created_date

**2. expenses**
- expense_id
- user_id
- expense_date
- category
- description
- amount
- created_date

Each expense is associated with a registered user through `user_id`.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project

```bash
cd daily_expense_tracker
```

### 3. Create a virtual environment

```bash
python -m venv expense_venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\expense_venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/DAILY_EXPENSE_DB
JWT_SECRET_KEY=YOUR_LONG_RANDOM_SECRET
```

Replace the database username, password, and secret with your own values.

**Important:** Never upload `.env` or database credentials to GitHub.

### 7. Run the application

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000/
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate user and generate JWT |

### Expense Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/expenses` | Add an expense |
| GET | `/api/expenses` | Get logged-in user's expenses |
| GET | `/api/expenses/{expense_id}` | Get expense details |
| PUT | `/api/expenses/{expense_id}` | Update an expense |
| DELETE | `/api/expenses/{expense_id}` | Delete an expense |

Protected expense endpoints require a JWT access token in the Authorization header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Deployment

The application is deployed using Render.

Deployment configuration:

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

Configure these environment variables in Render:

```text
DATABASE_URL
JWT_SECRET_KEY
```

Connect the GitHub repository to Render. New commits can trigger automatic deployments when auto-deploy is enabled.

## Reports and Budget Tracking

The reports module provides spending analysis for different periods.

Budget performance grades:

| Grade | Budget Usage |
|---|---|
| A | 60% or less |
| B | Above 60% to 80% |
| C | Above 80% to 100% |
| D | Above 100% to 120% |
| E | Above 120% |

The monthly budget is currently stored in browser local storage.

## Future Enhancements

- Recurring expense management
- Monthly and yearly budget planning
- Excel report downloads
- Email notifications
- Advanced spending analytics
- Multi-currency support
- Improved mobile responsiveness

## Author

**Daily Expense Tracker Project**

Built using Python Flask, PostgreSQL, HTML, CSS, and JavaScript.

## License

This project is available for learning and personal development. Add a formal license if you plan to distribute it publicly.