# Daily Expense Tracker

A web-based personal finance application built using **Python Flask and PostgreSQL** to manage daily expenses, monitor spending patterns, track monthly budgets, and generate analytical reports.

## Features

### 1. User Authentication
- User registration
- User login
- JWT-based authentication
- Secure password hashing using Werkzeug
- User-specific expense records
- Protected API endpoints

### 2. Expense Management
- Add new expenses
- View all expenses
- View individual expense details
- Edit existing expenses
- Delete expenses
- Categorize expenses
- Filter expenses by date

### 3. Dashboard
- View total expenses
- View selected-period spending
- View transaction count
- Filter expenses using date ranges
- Edit and delete transactions
- Responsive dashboard interface

### 4. Reports and Analytics
- This Week, This Month, and This Year reports
- Custom date-range reports
- Total spending
- Transaction count
- Average expense
- Highest expense
- Previous-period spending comparison
- Category-wise spending analysis
- Spending trend visualization
- Top spending category
- Automated spending insights
- Download PDF reports

### 5. Monthly Budget Tracking
- Set a monthly expense budget
- Track current-month spending
- Calculate budget utilization percentage
- Display remaining budget
- Budget performance grading (A–E)

**Budget performance grades:**

| Grade | Budget Usage |
|---|---|
| A | 60% or less |
| B | Above 60% to 80% |
| C | Above 80% to 100% |
| D | Above 100% to 120% |
| E | Above 120% |

> Note: The monthly budget is currently stored in browser local storage.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL |
| Database Connectivity | psycopg2 |
| Authentication | Flask-JWT-Extended |
| Password Security | Werkzeug |
| Frontend | HTML, CSS, JavaScript |
| Charts and Analytics | Chart.js |
| PDF Generation | jsPDF, jsPDF-AutoTable |
| Environment Configuration | python-dotenv |
| Deployment | Render |
| Production Server | Gunicorn |
| Version Control | Git and GitHub |

## Project Structure

```text
daily_expense_tracker/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── routes/
│   ├── auth_routes.py
│   └── expense_routes.py
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

The application currently uses two main tables.

### 1. Users Table

| Column | Description |
|---|---|
| user_id | Primary key |
| username | User's username |
| email | User's email address |
| password_hash | Hashed password |
| full_name | User's full name |
| is_active | Account status |
| created_date | Account creation timestamp |

### 2. Expenses Table

| Column | Description |
|---|---|
| expense_id | Primary key |
| user_id | Foreign key referencing users |
| expense_date | Expense transaction date |
| category | Expense category |
| description | Expense description |
| amount | Expense amount |
| created_date | Record creation timestamp |

Each expense is associated with a registered user through `user_id`.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

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

Create a `.env` file in the project root directory:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/DAILY_EXPENSE_DB
JWT_SECRET_KEY=YOUR_LONG_RANDOM_SECRET
```

Replace the database credentials and JWT secret with your own values.

**Security Note:** Never upload `.env`, database credentials, or secret keys to GitHub.

### 7. Run the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000/
```

## API Documentation

All protected expense endpoints require a valid JWT access token.

### Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate user and generate JWT |

### Expense Management APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/expenses` | Add a new expense |
| GET | `/api/expenses` | Get logged-in user's expenses |
| GET | `/api/expenses/{expense_id}` | Get individual expense details |
| PUT | `/api/expenses/{expense_id}` | Update an existing expense |
| DELETE | `/api/expenses/{expense_id}` | Delete an expense |

### Authorization Header

Pass the JWT access token in the request header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Deployment on Render

The application can be deployed using Render.

### Deployment Configuration

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

### Environment Variables

Configure the following environment variables in Render:

```text
DATABASE_URL
JWT_SECRET_KEY
```

### Deployment Steps

1. Push the project code to GitHub.
2. Create a new Web Service in Render.
3. Connect your GitHub repository.
4. Configure the build and start commands.
5. Add the required environment variables.
6. Deploy the application.

When automatic deployment is enabled, new commits pushed to the connected branch can trigger deployments.

## Future Enhancements

- Income management
- Borrow and lend management
- Partial repayment tracking
- Monthly and category-wise budget planning
- Recurring expense management
- Excel and CSV report downloads
- Email notifications and reminders
- Advanced financial analytics
- Income versus expense comparison
- Multi-currency support
- Improved mobile responsiveness
- AI-powered spending insights

## Author

**Daily Expense Tracker Project**

Developed using Python, Flask, PostgreSQL, HTML, CSS, and JavaScript.

## License

This project is available for learning and personal development. Add a formal open-source license if you plan to distribute or reuse it publicly.