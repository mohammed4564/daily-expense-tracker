
-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expenses table
CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    expense_date DATE NOT NULL,
    category VARCHAR(100) NOT NULL,
    description VARCHAR(250),
    amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_expenses_users
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Index for faster user-wise expense retrieval
CREATE INDEX idx_expenses_user_date
ON expenses(user_id, expense_date);
