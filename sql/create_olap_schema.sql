-- 1. Date Dimension (Static)
CREATE TABLE dim_date (
    date_sk INT PRIMARY KEY,                     -- Surrogate key (simple integer, fast joins)
    full_date DATE NOT NULL,                     -- Actual calendar date
    day INT,                                     -- Day of month (e.g. 15)
    month INT,                                   -- Month number (1–12)
    month_name NVARCHAR(20),                     -- Month name (e.g. 'January')
    quarter INT,                                 -- Quarter of year (1–4)
    year INT,                                    -- Year (e.g. 2024)
    weekday_name NVARCHAR(20)                    -- Day of week (e.g. 'Monday')
);

-- 2. Customer Dimension (SCD Type 2)
CREATE TABLE dim_customer (
    customer_sk INT IDENTITY(1,1) PRIMARY KEY,   -- Surrogate key for dimension
    customer_id INT NOT NULL,                    -- Business key from OLTP system
    full_name NVARCHAR(200),                     -- Supports long names and Unicode
    email NVARCHAR(200),                         -- Email addresses can vary in length
    phone NVARCHAR(50),                          -- Allows for country codes, dashes, etc.
    city NVARCHAR(100),                          -- City names with Unicode support
    state NVARCHAR(100),                         -- State/region name
    zip_code NVARCHAR(20),                       -- ZIP/postal codes may contain letters
    start_date DATE,                             -- SCD2: version start date
    end_date DATE,                               -- SCD2: version end date
    current_flag CHAR(1)                         -- 'Y' = current version, 'N' = old version
);

-- 3. Product Dimension (SCD Type 1)
CREATE TABLE dim_product (
    product_sk INT IDENTITY(1,1) PRIMARY KEY,    -- Surrogate key
    product_id INT NOT NULL,                     -- OLTP product ID
    product_name NVARCHAR(200),                  -- Product names (Unicode)
    category_name NVARCHAR(100),                 -- Denormalized category name
    brand_name NVARCHAR(100),                    -- Denormalized brand name
    model_year INT,                              -- Numeric year of model
    list_price DECIMAL(10, 2)                    -- Price with 2 decimal precision
);

-- 4. Staff Dimension (SCD Type 2)
CREATE TABLE dim_staff (
    staff_sk INT IDENTITY(1,1) PRIMARY KEY,      -- Surrogate key
    staff_id INT NOT NULL,                       -- OLTP staff ID
    full_name NVARCHAR(200),                     -- Full name
    email NVARCHAR(200),                         -- Email address
    active BIT,                                  -- 0 = inactive, 1 = active
    store_id INT,                                -- OLTP store ID (FK not enforced here)
    manager_id INT,                              -- Self-reference or hierarchy
    start_date DATE,                             -- SCD2 start date
    end_date DATE,                               -- SCD2 end date
    current_flag CHAR(1)                         -- 'Y' = current, 'N' = historical
);

-- 5. Store Dimension (Type 1)
CREATE TABLE dim_store (
    store_sk INT IDENTITY(1,1) PRIMARY KEY,      -- Surrogate key
    store_id INT NOT NULL,                       -- OLTP store ID
    store_name NVARCHAR(200),                    -- Store display name
    city NVARCHAR(100),                          -- City location
    state NVARCHAR(100),                         -- State or province
    zip_code NVARCHAR(20)                        -- ZIP/postal code (flexible format)
);

-- 6. Fact Sales Table
CREATE TABLE fact_sales (
    sales_sk INT IDENTITY(1,1) PRIMARY KEY,      -- Surrogate key for fact row
    order_id INT,                                -- OLTP order ID
    item_id INT,                                 -- OLTP item ID (row-level granularity)
    customer_sk INT,                             -- FK to dim_customer
    product_sk INT,                              -- FK to dim_product
    staff_sk INT,                                -- FK to dim_staff
    store_sk INT,                                -- FK to dim_store
    order_date_sk INT,                           -- FK to dim_date
    quantity INT,                                -- Units sold
    list_price DECIMAL(10,2),                    -- Unit price at time of order
    discount DECIMAL(5,2),                       -- Discount applied (e.g. 0.15 for 15%)
    total_price DECIMAL(10,2),                   -- Calculated field
    FOREIGN KEY (customer_sk) REFERENCES dim_customer(customer_sk),
    FOREIGN KEY (product_sk) REFERENCES dim_product(product_sk),
    FOREIGN KEY (staff_sk) REFERENCES dim_staff(staff_sk),
    FOREIGN KEY (store_sk) REFERENCES dim_store(store_sk),
    FOREIGN KEY (order_date_sk) REFERENCES dim_date(date_sk)
);
