-- Personal Expense and Spending Behavior Analysis
-- MySQL 8.0+

CREATE DATABASE IF NOT EXISTS personal_expense_analysis;
USE personal_expense_analysis;

DROP TABLE IF EXISTS expenses;

CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_type ENUM('weekday', 'weekend') NOT NULL,
    category VARCHAR(30) NOT NULL,
    description VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_mode VARCHAR(20) NOT NULL,
    CONSTRAINT chk_positive_amount CHECK (amount > 0)
);

CREATE INDEX idx_expenses_date ON expenses (expense_date);
CREATE INDEX idx_expenses_category ON expenses (category);
CREATE INDEX idx_expenses_day_type ON expenses (day_type);

