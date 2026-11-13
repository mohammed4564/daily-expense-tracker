# Daily Expense Tracker

A web-based personal finance management application built using **Python Flask and PostgreSQL**. It helps users manage daily expenses, track income, maintain borrowing and lending records, monitor monthly budgets, and generate financial reports.

## Features

### 1. User Authentication
- User registration with Terms & Conditions acceptance
- User login
- JWT-based authentication
- Access token and refresh token support
- Secure password hashing using Werkzeug
- Change password functionality
- User-specific financial records
- Protected API endpoints

### 2. Expense Management
- Add new expenses
- View all expenses
- View individual expense details
- Edit existing expenses
- Delete expenses
- Categorize expenses
- Filter expenses by date
- User-specific expense tracking

### 3. Income Management
- Add new income records
- View all income transactions
- View individual income details
- Edit existing income records
- Delete income records
- Categorize income
- Filter income by date
- Track income from different sources

### 4. Borrow / Lend Management
- Record borrowed amounts
- Record lent amounts
- Maintain person-wise transaction records
- Store transaction dates and due dates
- Add transaction descriptions
- Track transaction status:
  - Active
  - Completed
  - Cancelled
- Edit and delete borrow/lend records
- View borrowing and lending history

### 5. Financial Dashboard
- View total expenses
- View total income
- Track available balance
- Monitor financial transactions
- View selected-period spending
- Filter records using date ranges
- Access Expenses, Income, Borrow / Lend and Reports modules

### 6. Reports and Analytics
- This Week, This Month and This Year reports
- Custom date-range reports
- Total spending
- Transaction count
- Average expense
- Highest expense
- Previous-period comparison
- Category-wise spending analysis
- Spending trend visualization
- Top spending category
- Automated spending insights
- Download PDF expense reports

### 7. Monthly Budget Tracking
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

> **Note:** Monthly budget information is currently stored in browser local storage.

### 8. Registration Terms & Conditions
- Display Terms & Conditions during registration
- Require user acceptance before registration
- Record acceptance status
- Store acceptance timestamp
- Maintain a Terms & Conditions version

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
│   ├── expense_routes.py
│   ├── income_routes.py
│   └── borrow_lend_routes.py
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
│   ├── income.html
│   ├── borrow_lend.html
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

The application uses the following main tables.

### 1. Users

| Column | Description |
|---|---|
| user_id | Primary key |
| username | User's username |
| email | User's email |
| password_hash | Hashed password |
| full_name | User's full name |
| is_active | Account status |
| terms_accepted | Terms acceptance status |
| terms_accepted_at | Acceptance timestamp |
| terms_version | Accepted terms version |
| created_date | Account creation timestamp |

### 2. Expenses

| Column | Description |
|---|---|
| expense_id | Primary key |
| user_id | Foreign key referencing users |
| expense_date | Expense transaction date |
| category | Expense category |
| description | Expense description |
| amount | Expense amount |
| created_date | Record creation timestamp |

### 3. Income

| Column | Description |
|---|---|
| income_id | Primary key |
| user_id | Foreign key referencing users |
| income_date | Income transaction date |
| category | Income category |
| description | Income description |
| amount | Income amount |
| created_date | Record creation timestamp |

### 4. Borrow / Lend

| Column | Description |
|---|---|
| transaction_id | Primary key |
| user_id | Foreign key referencing users |
| transaction_type | BORROWED or LENT |
| person_name | Person involved in transaction |
| amount | Transaction amount |
| transaction_date | Transaction date |
| due_date | Expected repayment date |
| description | Transaction description |
| status | ACTIVE, COMPLETED or CANCELLED |
| created_date | Record creation timestamp |

All financial records are associated with their respective users through `user_id`.

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

**Windows PowerShell:**

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

Replace the database credentials and JWT secret with your own values.

**Security:** Never upload `.env`, database credentials, or secret keys to GitHub.

### 7. Run the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000/
```

## API Endpoints

All protected financial APIs require a valid JWT access token.

### Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate user and generate access and refresh tokens |
| PUT | `/api/auth/change-password` | Change account password |
| POST | `/api/auth/refresh` | Generate a new access token using a refresh token |

### Expense Management APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/expenses` | Add an expense |
| GET | `/api/expenses` | Get logged-in user's expenses |
| GET | `/api/expenses/{expense_id}` | Get expense details |
| PUT | `/api/expenses/{expense_id}` | Update an expense |
| DELETE | `/api/expenses/{expense_id}` | Delete an expense |

### Income Management APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/income` | Add income |
| GET | `/api/income` | Get logged-in user's income records |
| GET | `/api/income/{income_id}` | Get income details |
| PUT | `/api/income/{income_id}` | Update income |
| DELETE | `/api/income/{income_id}` | Delete income |

### Borrow / Lend Management APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/borrow-lend` | Create a borrow/lend record |
| GET | `/api/borrow-lend` | Get borrow/lend records |
| GET | `/api/borrow-lend/{transaction_id}` | Get transaction details |
| PUT | `/api/borrow-lend/{transaction_id}` | Update a transaction |
| DELETE | `/api/borrow-lend/{transaction_id}` | Delete a transaction |

### Authorization Header

For protected API requests:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

For the refresh endpoint, send the refresh token using the authentication mechanism configured by the backend.

## Deployment on Render

The application can be deployed using Render.

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

Configure the following environment variables in Render:

```text
DATABASE_URL
JWT_SECRET_KEY
```

Connect your GitHub repository to Render. New commits can trigger automatic deployments when auto-deploy is enabled.

## Future Enhancements

- Partial borrow/lend repayment tracking
- Recurring income and expense management
- Category-wise budget planning
- Excel and CSV report downloads
- Email notifications and reminders
- Advanced financial analytics
- Income versus expense comparison
- Multi-currency support
- AI-powered spending insights
- Improved mobile responsiveness
- Persistent database-based budget management
- Login history and account security monitoring

## Author

**Daily Expense Tracker Project**

Developed using Python, Flask, PostgreSQL, HTML, CSS and JavaScript.

## License

This project is available for learning and personal development. Add a formal open-source license if you plan to distribute it publicly.
