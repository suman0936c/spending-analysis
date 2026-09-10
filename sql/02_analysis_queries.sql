-- Run after importing data/expense_data.csv into personal_expense_analysis.expenses.
USE personal_expense_analysis;

-- 1. Data-quality checks
SELECT
    COUNT(*) AS transaction_count,
    MIN(expense_date) AS analysis_start_date,
    MAX(expense_date) AS analysis_end_date,
    SUM(amount) AS total_spend
FROM expenses;

SELECT *
FROM expenses
WHERE amount <= 0
   OR expense_date IS NULL
   OR category IS NULL
   OR payment_mode IS NULL;

-- 2. KPI summary
WITH daily_spend AS (
    SELECT expense_date, SUM(amount) AS daily_total
    FROM expenses
    GROUP BY expense_date
)
SELECT
    SUM(daily_total) AS total_monthly_spend,
    ROUND(AVG(daily_total), 2) AS average_daily_spend,
    MAX(daily_total) AS highest_daily_spend
FROM daily_spend;

-- 3. Category contribution
SELECT
    category,
    SUM(amount) AS total_spend,
    ROUND(100 * SUM(amount) / SUM(SUM(amount)) OVER (), 1) AS spend_share_pct
FROM expenses
GROUP BY category
ORDER BY total_spend DESC;

-- 4. Payment-mode preference
SELECT
    payment_mode,
    SUM(amount) AS total_spend,
    ROUND(100 * SUM(amount) / SUM(SUM(amount)) OVER (), 1) AS spend_share_pct
FROM expenses
GROUP BY payment_mode
ORDER BY total_spend DESC;

-- 5. Daily trend with cumulative spend
WITH daily_spend AS (
    SELECT expense_date, SUM(amount) AS daily_total
    FROM expenses
    GROUP BY expense_date
)
SELECT
    expense_date,
    daily_total,
    SUM(daily_total) OVER (ORDER BY expense_date) AS cumulative_spend
FROM daily_spend
ORDER BY expense_date;

-- 6. Highest-spend days and variance from daily average
WITH daily_spend AS (
    SELECT expense_date, SUM(amount) AS daily_total
    FROM expenses
    GROUP BY expense_date
), baseline AS (
    SELECT AVG(daily_total) AS average_daily_spend
    FROM daily_spend
)
SELECT
    d.expense_date,
    d.daily_total,
    ROUND(d.daily_total - b.average_daily_spend, 2) AS variance_from_average
FROM daily_spend d
CROSS JOIN baseline b
ORDER BY d.daily_total DESC
LIMIT 5;

-- 7. Weekday vs. weekend spending
SELECT
    day_type,
    COUNT(DISTINCT expense_date) AS active_days,
    SUM(amount) AS total_spend,
    ROUND(SUM(amount) / COUNT(DISTINCT expense_date), 2) AS average_spend_per_day
FROM expenses
GROUP BY day_type
ORDER BY total_spend DESC;

-- 8. Weekly spending trend (week starts Monday)
SELECT
    DATE_SUB(expense_date, INTERVAL WEEKDAY(expense_date) DAY) AS week_start,
    SUM(amount) AS weekly_spend
FROM expenses
GROUP BY DATE_SUB(expense_date, INTERVAL WEEKDAY(expense_date) DAY)
ORDER BY week_start;

-- 9. Food spending breakdown
SELECT
    description,
    SUM(amount) AS total_spend
FROM expenses
WHERE category = 'Food'
GROUP BY description
ORDER BY total_spend DESC;

-- 10. Discretionary-spending review
SELECT
    category,
    SUM(amount) AS total_spend
FROM expenses
WHERE category IN ('Entertainment', 'Shopping', 'Others')
GROUP BY category
ORDER BY total_spend DESC;
