WITH DateGenerator AS (
    SELECT CAST('2000-01-01' AS DATE) AS full_date  -- Starting date
    UNION ALL
    SELECT DATEADD(DAY, 1, full_date)              -- Add one day to the previous date
    FROM DateGenerator
    WHERE full_date < '2050-12-31'                 -- Ending date
)
-- Insert Date Dimension Data
INSERT INTO dim_date (date_sk, full_date, day, month, month_name, quarter, year, weekday_name)
SELECT
    -- Surrogate key: YYYYMMDD format
    CAST(CONVERT(VARCHAR(4), YEAR(full_date)) +
         RIGHT('00' + CONVERT(VARCHAR(2), MONTH(full_date)), 2) +
         RIGHT('00' + CONVERT(VARCHAR(2), DAY(full_date)), 2) AS INT) AS date_sk,
    full_date,
    DAY(full_date) AS day,
    MONTH(full_date) AS month,
    DATENAME(MONTH, full_date) AS month_name,
    DATEPART(QUARTER, full_date) AS quarter,
    YEAR(full_date) AS year,
    DATENAME(WEEKDAY, full_date) AS weekday_name
FROM DateGenerator
OPTION (MAXRECURSION 0);  -- Removes recursion limit
